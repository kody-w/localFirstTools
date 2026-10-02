#!/usr/bin/env python3
"""Plan and explicitly run bounded, caller-approved capability qualifications.

No daemon, model service, network, publishing, identity minting, or shell.
Permissions are admission controls for trusted local code, not an OS sandbox.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import subprocess
import sys

if __package__:
    from . import autocomplete_frames as frames
    from . import capability_contracts as contracts
else:
    import autocomplete_frames as frames
    import capability_contracts as contracts


REQUEST_SCHEMA = "localfirst-capability-requests/v1"
POLICY_SCHEMA = "localfirst-capability-policy/v1"
STATE_SCHEMA = "localfirst-capability-job-state/v1"
ENTRYPOINT = "scripts/capability_package.py"
MAX_INPUTS = 1000
REQUEST_FIELDS = {
    "id", "capability_id", "source_repo", "source_commit", "repository",
    "workflow", "paths", "trigger", "requested_model",
}
MANIFEST_FIELDS = {
    "id", "version", "title", "job", "entrypoint", "artifacts", "contract",
    "checks", "failure_cases", "reuses", "visibility",
}
LIMITATIONS = [
    "The supplied policy is caller approval, not authenticated authorization or an OS sandbox.",
    "No network, publishing, deployment, merge, or model service is provided.",
    "requested_model is host-supplied metadata; model_execution is not_invoked.",
    "Priority orders qualification work, not novelty, correctness, or user value.",
    "A completed job means qualification and its recorded replay passed, not universal correctness.",
    "UTC and unsigned RAPP receipts do not establish trusted time, authorship, or first invention.",
    "Idempotency and concurrency apply within the explicitly selected state directory.",
    "Each explicit run attempts a job at most once; interrupted work requires operator recovery.",
    "timeout_seconds caps each qualification and replay command separately; Git probes are bounded to ten seconds.",
]
require = contracts.require


def safe_error(error):
    try:
        return frames.public_text(str(error), 1024)
    except (ValueError, TypeError):
        return type(error).__name__ + ": operation rejected; inspect retained evidence locally"


def relative(root, value, *, source=False):
    if source:
        require(isinstance(value, str) and 0 < len(value) <= 512, "invalid source_repo")
        require("\\" not in value and ":" not in value and not value.startswith("/"),
                "source_repo must be a relative local repository")
        if value != ".":
            parts = value.split("/")
            require(all(part and part != "." for part in parts), "noncanonical source_repo")
            seen_name = False
            for part in parts:
                require(part != ".." or not seen_name, "source_repo traversal must be a leading prefix")
                seen_name = seen_name or part != ".."
            require(seen_name, "source_repo must name a repository")
        frames.public_text(value, 512)
    else:
        frames.relative_path(value)
        # Apply the recorder's sensitive-directory guard to directories as well.
        frames.artifact_path(value + "/guard.json")
    path = Path(root) / value
    frames.no_symlinks(path)
    return Path(os.path.abspath(path))


def json_input(root, name):
    path = relative(root, name)
    require(path.suffix == ".json", "inputs and outputs must be JSON files")
    raw = frames.read_bytes(path, contracts.MAX_JSON_BYTES)
    value = contracts.load_json(path)
    require(contracts.digest(raw) == contracts.digest(frames.read_bytes(path, contracts.MAX_JSON_BYTES)),
            "input changed while reading")
    return value, {"path": name, "sha256": contracts.digest(raw)}


def policy_input(root, name):
    policy, pin = json_input(root, name)
    require(set(policy) == {
        "schema", "allowed_capabilities", "permissions", "max_jobs", "max_parallel",
        "max_attempts", "timeout_seconds", "visibility",
    } and policy["schema"] == POLICY_SCHEMA, "invalid policy contract")
    allowed = policy["allowed_capabilities"]
    require(isinstance(allowed, list) and len(allowed) <= MAX_INPUTS, "invalid allowed_capabilities")
    for value in allowed:
        contracts.sha256(value)
    require(len(set(allowed)) == len(allowed), "duplicate policy manifest pins")
    permissions = policy["permissions"]
    require(isinstance(permissions, list) and all(isinstance(value, str) for value in permissions)
            and len(set(permissions)) == len(permissions) and set(permissions) <= contracts.PERMISSIONS,
            "invalid policy permissions")
    for key, maximum in (("max_jobs", 10), ("max_parallel", 10), ("max_attempts", 3),
                         ("timeout_seconds", 300)):
        require(type(policy[key]) is int and 1 <= policy[key] <= maximum, "invalid policy bound: " + key)
    require(policy["visibility"] in {"private", "public"}, "invalid policy visibility")
    return policy, pin


def git(root, *args):
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith("GIT_")}
    environment.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
    result = subprocess.run(
        ["git", "-C", str(root), *args], stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, env=environment,
    )
    require(result.returncode == 0, "source repository, commit, or selected paths could not be verified")
    return result.stdout


def source_context(root, request):
    source = relative(root, request["source_repo"], source=True)
    require(source.is_dir(), "source repository does not exist")
    require(git(source, "rev-parse", "--show-prefix").strip() == b"",
            "source_repo must be a Git worktree root")
    commit = request["source_commit"]
    require(git(source, "cat-file", "-t", commit).strip() == b"commit",
            "source_commit must exist as a Git commit")
    tree = git(source, "rev-parse", commit + "^{tree}").decode("ascii").strip()
    contracts.committed_ref(tree)
    entries = git(source, "ls-tree", "-z", commit, "--", *request["paths"]).split(b"\0")
    found = set()
    for entry in filter(None, entries):
        metadata, name = entry.split(b"\t", 1)
        mode, kind, _ = metadata.split()
        require(mode in {b"100644", b"100755"} and kind == b"blob",
                "selected source paths must be regular committed files, not symlinks or directories")
        found.add(name.decode("utf-8"))
    require(found == set(request["paths"]), "a selected source path is missing at the pinned commit")
    return tree


def request_value(value):
    require(isinstance(value, dict) and set(value) == REQUEST_FIELDS, "invalid request fields")
    result = dict(value)
    for key in ("id", "capability_id", "workflow"):
        contracts.identifier(result[key])
    contracts.committed_ref(result["source_commit"])
    require(isinstance(result["repository"], str) and
            re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*",
                         result["repository"]), "repository must be owner/repo")
    result["repository"] = result["repository"].lower()
    paths = result["paths"]
    require(isinstance(paths, list) and 1 <= len(paths) <= 24, "select 1-24 explicit source paths")
    for name in paths:
        frames.artifact_path(name)
    result["paths"] = sorted(set(paths))
    trigger = result["trigger"]
    require(isinstance(trigger, dict) and set(trigger) == {"kind", "key"}
            and trigger["kind"] in {"manual", "repository-change", "model-upgrade", "failure"},
            "invalid event trigger")
    frames.public_text(trigger["key"], 512)
    frames.public_text(result["requested_model"], 160)
    return result


def job_key(request, manifest_sha, policy_sha):
    identity = {key: request[key] for key in (
        "source_commit", "repository", "workflow", "paths", "trigger", "requested_model",
    )}
    identity.update(manifest_sha256=manifest_sha, policy_sha256=policy_sha)
    return contracts.digest(contracts.json_bytes(identity))


def candidates(root, registry_name, requests_name, policy_name):
    policy, policy_pin = policy_input(root, policy_name)
    registry, registry_pin = json_input(root, registry_name)
    requests, requests_pin = json_input(root, requests_name)
    require(registry.get("schema") == contracts.REGISTRY_SCHEMA, "unsupported registry schema")
    assets = registry.get("assets")
    require(isinstance(assets, list) and len(assets) <= MAX_INPUTS, "invalid registry assets")
    by_id = {}
    for asset in assets:
        require(isinstance(asset, dict), "invalid registry asset")
        identity = contracts.identifier(asset.get("id"))
        require(identity not in by_id, "duplicate capability identity in registry")
        by_id[identity] = asset
    require(requests.get("schema") == REQUEST_SCHEMA and isinstance(requests.get("requests"), list)
            and len(requests["requests"]) <= MAX_INPUTS, "invalid requests document")
    ids = [request.get("id") if isinstance(request, dict) else None for request in requests["requests"]]
    require(all(isinstance(value, str) for value in ids) and len(set(ids)) == len(ids),
            "requests require unique string identifiers")
    loaded = {}

    def asset_manifest(identity, stack=()):
        require(identity not in stack, "capability dependency cycle")
        require(len(stack) < 64, "capability dependency depth exceeds 64")
        if identity in loaded:
            return loaded[identity]
        asset = by_id.get(identity)
        require(asset is not None, "capability or pinned dependency is absent from registry")
        require(MANIFEST_FIELDS | {"manifest_path", "manifest_sha256", "status"} <= set(asset),
                "incomplete registry asset")
        contracts.sha256(asset["manifest_sha256"])
        require(asset["manifest_sha256"] in policy["allowed_capabilities"],
                "manifest is not approved by caller policy")
        manifest_path = relative(root, asset["manifest_path"])
        manifest, sha = contracts.load_manifest(manifest_path, root)
        require(sha == asset["manifest_sha256"], "registry manifest digest drift")
        require(all(asset[key] == manifest[key] for key in MANIFEST_FIELDS),
                "registry fields do not match the pinned manifest")
        require(asset["status"] in {"built", "proven", "reused"}, "unsupported asset status")
        require(set(manifest["contract"]["permissions"]) <= set(policy["permissions"]),
                "capability permissions exceed caller policy")
        require(policy["visibility"] != "public" or manifest["visibility"] == "public",
                "private capability cannot enter public evidence")
        require(all(check["timeout_seconds"] <= policy["timeout_seconds"] for check in manifest["checks"]),
                "capability check timeout exceeds caller policy")
        for check in manifest["checks"]:
            frames.check_argv(check["argv"])
        require(len(manifest["artifacts"]) + 3 <= frames.MAX_ARTIFACTS,
                "manifest plus qualification artifacts exceed recorder capacity")
        for dependency in manifest["reuses"]:
            other, _ = asset_manifest(dependency["id"], (*stack, identity))
            require(other["manifest_sha256"] == dependency["manifest_sha256"], "dependency pin drift")
        loaded[identity] = (asset, manifest)
        return loaded[identity]

    def dependency_pins(identity):
        found = {}

        def visit(selected):
            if selected in found:
                return
            asset, manifest = loaded[selected]
            found[selected] = {
                "id": selected, "path": asset["manifest_path"], "sha256": asset["manifest_sha256"],
            }
            for dependency in manifest["reuses"]:
                visit(dependency["id"])

        visit(identity)
        return [found[key] for key in sorted(found)]

    jobs, blocked, seen = [], [], set()
    for value in requests["requests"]:
        request_id = value["id"]
        try:
            request = request_value(value)
            asset, manifest = asset_manifest(request["capability_id"])
            require(set(policy["permissions"]) == contracts.PERMISSIONS,
                    "qualification requires repository.read, artifact.write, and process.execute")
            require(manifest["entrypoint"] == ENTRYPOINT,
                    "blocked host-work-order: no executor for this capability entrypoint")
            source_context(root, request)
            identity = job_key(request, asset["manifest_sha256"], policy_pin["sha256"])
            if identity in seen:
                blocked.append({"request_id": request_id, "reason": "duplicate idempotency key"})
                continue
            seen.add(identity)
            kind = request["trigger"]["kind"]
            priority, reason = {
                "failure": (0, "Failure-triggered qualification; reproduction is still required."),
                "model-upgrade": (1, "Requalify the existing package before proposing a new build; model not invoked."),
                "repository-change": (2, "Requalify changed pinned source inputs with the existing package."),
                "manual": (3, "Qualify this explicitly requested repository context by reusing the existing package."),
            }[kind]
            if kind == "manual" and isinstance(asset.get("uses"), list):
                for use in asset["uses"]:
                    context = use.get("context", use) if isinstance(use, dict) else {}
                    if isinstance(context, dict) and context.get("repository") == request["repository"] \
                            and context.get("workflow") == request["workflow"]:
                        priority = 4
                        reason = "Recheck a previously evidenced context after failure, upgrade, changed-input, and unseen-context work."
                        break
            job = {
                **{key: request[key] for key in REQUEST_FIELDS - {"id"}},
                "id": identity, "request_id": request_id, "manifest_path": asset["manifest_path"],
                "manifest_sha256": asset["manifest_sha256"], "priority": priority, "reason": reason,
                "evidence_manifests": dependency_pins(request["capability_id"]),
            }
            attestation_paths(root, job)
            jobs.append(job)
        except (ValueError, OSError, TypeError, KeyError, subprocess.TimeoutExpired) as error:
            blocked.append({"request_id": request_id, "reason": safe_error(error)})
    jobs.sort(key=lambda job: (job["priority"], job["id"]))
    return jobs, blocked, policy, {
        "registry": registry_pin, "requests": requests_pin, "policy": policy_pin,
    }


def attestation_paths(root, job):
    pins = job.get("evidence_manifests")
    require(isinstance(pins, list) and 1 <= len(pins) <= 64, "missing bounded dependency evidence closure")
    manifests, paths = {}, set()
    for pin in pins:
        require(isinstance(pin, dict) and set(pin) == {"id", "path", "sha256"},
                "invalid dependency evidence pin")
        manifest, revision = contracts.load_manifest(relative(root, pin["path"]), root)
        require(manifest["id"] == pin["id"] and revision == pin["sha256"]
                and pin["id"] not in manifests, "dependency evidence drift or duplicate")
        manifests[pin["id"]] = (pin, manifest)
        paths.add(pin["path"])
        paths.update(item["path"] for item in manifest["artifacts"])
    require(job["capability_id"] in manifests, "primary capability missing from evidence closure")
    primary = manifests[job["capability_id"]][0]
    require(primary["path"] == job["manifest_path"] and primary["sha256"] == job["manifest_sha256"],
            "primary evidence pin changed")
    for _, manifest in manifests.values():
        for dependency in manifest["reuses"]:
            require(dependency["id"] in manifests
                    and manifests[dependency["id"]][0]["sha256"] == dependency["manifest_sha256"],
                    "transitive evidence dependency missing or changed")
    require(len(paths) + 2 <= frames.MAX_ARTIFACTS, "complete evidence closure exceeds recorder artifact limit")
    size = sum(len(frames.read_bytes(relative(root, path), contracts.MAX_JSON_BYTES)) for path in paths)
    require(size + 2 * contracts.MAX_JSON_BYTES <= frames.MAX_TOTAL_ARTIFACT_BYTES,
            "complete evidence closure leaves insufficient capsule/report capacity")
    return sorted(paths)


def read_job(state, identity):
    contracts.sha256(identity)
    path = state / "jobs" / (identity + ".json")
    runs = state / "runs" / identity
    frames.no_symlinks(path)
    frames.no_symlinks(runs)
    attempts = []
    if runs.exists():
        for entry in runs.iterdir():
            frames.no_symlinks(entry)
            require(entry.is_dir() and re.fullmatch(r"attempt-[1-3]", entry.name),
                    "unexpected attempt directory")
            attempts.append(int(entry.name.rsplit("-", 1)[1]))
    attempts.sort()
    if not path.exists():
        return {"status": "recovery-required" if attempts else "pending",
                "attempts": len(attempts), "reason": "orphan attempt evidence" if attempts else ""}
    value = contracts.load_json(path)
    require(value.get("schema") == STATE_SCHEMA and value.get("id") == identity, "invalid job state")
    require(value.get("status") in {"running", "failed", "completed", "recovery-required"},
            "invalid stored job status")
    require(type(value.get("attempts")) is int and 1 <= value["attempts"] <= 3, "invalid attempt count")
    require(attempts == list(range(1, value["attempts"] + 1)), "state/attempt history mismatch")
    if value["status"] == "completed":
        require(isinstance(value.get("receipt"), dict), "completed state requires a recorded receipt")
    return value


def plan(root, registry, requests, policy, state, output):
    root = frames.root_path(root)
    state_path = relative(root, state)
    output_path = relative(root, output)
    require(output_path.suffix == ".json", "plan output must be JSON")
    jobs, blocked, caller_policy, inputs = candidates(root, registry, requests, policy)
    require(output not in {item["path"] for item in inputs.values()}, "plan cannot overwrite inputs")
    protected = {relative(root, item["path"]) for item in inputs.values()}
    for job in jobs:
        protected.update(relative(root, path) for path in attestation_paths(root, job))
    require(output_path not in protected, "plan cannot overwrite a pinned source artifact")
    for directory in ("runs", "jobs", "plans", "slots", "locks"):
        reserved = state_path / directory
        require(not output_path.is_relative_to(reserved)
                and not any(path.is_relative_to(reserved) for path in protected),
                "scheduler state cannot overlap input assets or plan output")
    eligible = []
    for job in jobs:
        previous = read_job(state_path, job["id"])
        if (state_path / "locks" / (job["id"] + ".lock")).exists():
            reason = "busy or stale job lock; recovery review required"
        elif previous["status"] in {"running", "recovery-required"}:
            reason = "recovery-required: interrupted work must not be silently rerun"
        elif previous["status"] == "completed":
            reason = "completed idempotency key; no new execution"
        elif previous["attempts"] >= caller_policy["max_attempts"]:
            reason = "attempt limit reached"
        else:
            eligible.append(job)
            continue
        blocked.append({"request_id": job["request_id"], "reason": reason})
    value = {
        "schema": contracts.PLAN_SCHEMA, "generated_at": frames.utc_now(),
        "policy_sha256": inputs["policy"]["sha256"], "inputs": inputs, "state": state,
        "status": "ready" if eligible else "idle", "jobs": eligible, "blocked": blocked,
        "limitations": LIMITATIONS,
    }
    value["plan_sha256"] = contracts.digest(contracts.json_bytes(value))
    receipt = state_path / "plans" / (value["plan_sha256"] + ".json")
    frames.directory(receipt.parent, create=True)
    frames.immutable_write(receipt, contracts.json_bytes(value), deduplicate=True)
    contracts.atomic_json(output_path, value)
    return value


def validate_plan(root, plan_name, policy_name, state_name):
    value, _ = json_input(root, plan_name)
    require(set(value) == {
        "schema", "generated_at", "policy_sha256", "inputs", "state", "status", "jobs",
        "blocked", "limitations", "plan_sha256",
    } and value["schema"] == contracts.PLAN_SCHEMA, "invalid plan contract")
    expected = contracts.digest(contracts.json_bytes({key: item for key, item in value.items()
                                                     if key != "plan_sha256"}))
    require(value["plan_sha256"] == expected, "plan contents changed")
    state = relative(root, state_name)
    require(value["state"] == state_name, "plan is bound to its original state directory")
    receipt = state / "plans" / (expected + ".json")
    require(contracts.load_json(receipt) == value, "plan does not match the retained planning receipt")
    inputs = value["inputs"]
    require(set(inputs) == {"registry", "requests", "policy"}, "invalid plan input bindings")
    require(inputs["policy"]["path"] == policy_name, "plan policy path changed")
    jobs, _, policy, actual = candidates(
        root, inputs["registry"]["path"], inputs["requests"]["path"], policy_name,
    )
    require(inputs == actual and value["policy_sha256"] == actual["policy"]["sha256"],
            "policy, registry, or requests changed since planning")
    allowed = {job["id"]: job for job in jobs}
    require(isinstance(value["jobs"], list), "invalid planned jobs")
    seen = set()
    for job in value["jobs"]:
        require(isinstance(job, dict) and job.get("id") in allowed
                and job == allowed[job["id"]], "job no longer matches validated input assets")
        require(job["id"] not in seen, "duplicate job in plan")
        seen.add(job["id"])
    require(value["jobs"] == sorted(value["jobs"], key=lambda job: (job["priority"], job["id"])),
            "plan priority order changed")
    return value, policy, state


class BusyError(ValueError):
    pass


@contextmanager
def exclusive(path, identity):
    frames.directory(path.parent, create=True)
    frames.no_symlinks(path)
    try:
        path.mkdir()
    except FileExistsError as error:
        raise BusyError("busy or stale lock; it was not stolen") from error
    try:
        contracts.atomic_json(path / "owner.json",
                              {"job_id": identity, "pid": os.getpid(), "started_at": frames.utc_now()})
        yield
    finally:
        (path / "owner.json").unlink(missing_ok=True)
        path.rmdir()


@contextmanager
def capacity(state, policy_sha, maximum, identity):
    for number in range(maximum):
        lock = exclusive(state / "slots" / policy_sha / (str(number) + ".lock"), identity)
        try:
            lock.__enter__()
        except BusyError:
            continue
        try:
            yield
        finally:
            lock.__exit__(None, None, None)
        return
    raise BusyError("parallel capacity occupied by live or stale locks; no slot was stolen")


def qualification_argv(job, capsule, report):
    argv = [
        "python3", ENTRYPOINT, "qualify", "--root", ".", "--manifest", job["manifest_path"],
        "--repo", job["source_repo"], "--ref", job["source_commit"],
        "--repository", job["repository"],
    ]
    for path in job["paths"]:
        argv += ["--path", path]
    return argv + ["--workflow", job["workflow"], "--capsule", capsule, "--report", report, "--allow-checks"]


def replay_argv(value, job, capsule, report):
    contracts.validate_source_replay(value, ENTRYPOINT)
    expected = contracts.source_replay_argv(
        ENTRYPOINT, job["manifest_path"], job["source_repo"], capsule, report,
    )
    require(value == expected, "replay options escape this qualification")
    return value


def validate_report(root, job, capsule, report, tree, manifest):
    value = contracts.load_json(root / report)
    require(value.get("schema") == contracts.QUALIFICATION_SCHEMA, "invalid qualification report schema")
    require(all(isinstance(value.get(key), dict) for key in ("capability", "context", "capsule", "gates")),
            "qualification report sections must be objects")
    require(value.get("capability", {}).get("id") == job["capability_id"]
            and value["capability"].get("manifest_sha256") == job["manifest_sha256"],
            "qualification capability pin mismatch")
    context = value.get("context", {})
    require(all(context.get(key) == expected for key, expected in {
        "repository": job["repository"], "commit": job["source_commit"],
        "tree": tree, "workflow": job["workflow"],
    }.items()), "qualification source context mismatch")
    body = frames.read_bytes(root / capsule, contracts.MAX_JSON_BYTES)
    require(value.get("capsule", {}).get("sha256") == contracts.digest(body)
            and value["capsule"].get("bytes") == len(body), "qualification capsule digest mismatch")
    require(value.get("outcome") == "passed" and
            all(value.get("gates", {}).get(key) is True
                for key in ("source_matches", "round_trip", "artifacts_stable")),
            "qualification gates did not pass")
    checks = value.get("checks")
    require(isinstance(checks, list) and len(checks) == len(manifest["checks"]),
            "qualification must retain every declared check result")
    for actual, declared in zip(checks, manifest["checks"]):
        require(isinstance(actual, dict) and actual.get("argv") == declared["argv"]
                and type(actual.get("exit_code")) is int and frames.check_passed(actual),
                "qualification check was missing, failed, or changed")
        require(actual.get("timeout_seconds") == declared["timeout_seconds"],
                "qualification check timeout changed")
        for stream in ("stdout", "stderr"):
            contracts.sha256(actual.get(stream + "_sha256"))
            require(type(actual.get(stream + "_bytes")) is int and actual[stream + "_bytes"] >= 0,
                    "qualification check output evidence missing")
    # Reports, unlike source capsules, contain metadata only.
    def public_metadata(item):
        if isinstance(item, str) and item:
            frames.public_text(item, 8192)
        elif isinstance(item, dict):
            for child in item.values():
                public_metadata(child)
        elif isinstance(item, list):
            for child in item:
                public_metadata(child)
    public_metadata(value)
    return replay_argv(value.get("replay_argv"), job, capsule, report)


class RappRecorder:
    """The production recorder always uses the existing byte-pinned reference."""

    def __init__(self, root, store, rapp_dir):
        self.root, self.store = root, frames.root_path(store)
        self.reference = frames.Reference(rapp_dir)
        frames.store_layout(self.store, allow_publishing=True)
        self.identity = frames.load_identity(self.store, self.reference)

    def prepare(self, identity, attempt):
        location = self.store / "runs" / identity / ("attempt-" + str(attempt))
        frames.no_symlinks(location)
        require(not location.exists(), "recovery-required: the attempt already has a recorder stream")

    def record(self, job, attempt, artifacts, argv, timeout):
        args = argparse.Namespace(
            store=str(self.store), repo=str(self.root), run_id=job["id"], worker="attempt-" + str(attempt),
            phase="review",
            summary="Capability qualification " + job["capability_id"] + "; requested_model="
                    + job["requested_model"] + "; model_execution=not_invoked",
            artifact=artifacts, check=[json.dumps(argv)], check_timeout=timeout, parent=[],
        )
        result, code = frames.record(args, self.reference)
        require(code == 0 and result["outcome"] == "checks_passed", "recorded replay did not pass")
        self.verify(job, attempt, result)
        return result

    def verify(self, job, attempt, receipt):
        stream = frames.read_stream(self.store, self.reference, self.identity["rappid"],
                                    job["id"], "attempt-" + str(attempt))
        frames.verify_objects(self.store, stream)
        require(len(stream) == 1 and receipt.get("path") in stream, "missing or ambiguous job receipt")
        frame = stream[receipt["path"]]
        require(all(receipt.get(key) == frame[key] for key in
                    ("frame_hash", "payload_hash", "stream_id", "seq")), "recorded receipt hash mismatch")
        payload = frame["payload"]
        require(payload["outcome"] == "checks_passed" and len(payload["checks"]) == 1,
                "receipt does not prove a passing replay")
        suffix = "/runs/" + job["id"] + "/attempt-" + str(attempt) + "/"
        by_path = {item["path"]: item for item in payload["artifacts"]}
        reports = [path for path in by_path if path.endswith(suffix + "qualification.json")]
        require(len(reports) == 1, "receipt is not bound to this attempt's qualification")
        report = reports[0]
        capsule = report.removesuffix("qualification.json") + "capsule.json"
        manifest, sha = contracts.load_manifest(relative(self.root, job["manifest_path"]), self.root)
        require(sha == job["manifest_sha256"], "receipt manifest pin changed")
        expected = {capsule, report, *attestation_paths(self.root, job)}
        require(set(by_path) == expected, "receipt omits or substitutes qualification artifacts")
        for path, item in by_path.items():
            body = frames.read_bytes(self.root / path, contracts.MAX_JSON_BYTES)
            require(contracts.digest(body) == item["sha256"] and len(body) == item["bytes"],
                    "current qualification artifacts no longer match their receipt")
        argv = validate_report(self.root, job, capsule, report, source_context(self.root, job), manifest)
        require(payload["checks"][0]["argv"] == argv, "recorded check is not the exact qualification replay")


def execute_job(root, state, state_name, store_name, job, policy, policy_sha, recorder):
    identity = job["id"]
    result = {"id": identity, "request_id": job["request_id"],
              "requested_model": job["requested_model"], "model_execution": "not_invoked"}
    try:
        with exclusive(state / "locks" / (identity + ".lock"), identity):
            previous = read_job(state, identity)
            if previous["status"] == "completed":
                require(previous.get("store") == store_name, "completed job belongs to a different receipt store")
                recorder.verify(job, previous["attempts"], previous["receipt"])
                return {**result, "status": "no-op", "reason": "completed idempotency key"}
            if previous["status"] in {"running", "recovery-required"}:
                return {**result, "status": "recovery-required", "reason": "interrupted attempt; no commands rerun"}
            if previous["attempts"] >= policy["max_attempts"]:
                return {**result, "status": "blocked", "reason": "attempt limit reached"}
            with capacity(state, policy_sha, policy["max_parallel"], identity):
                number = previous["attempts"] + 1
                recorder.prepare(identity, number)
                manifest, sha = contracts.load_manifest(relative(root, job["manifest_path"]), root)
                require(sha == job["manifest_sha256"], "manifest changed before execution")
                closure_paths = attestation_paths(root, job)
                tree = source_context(root, job)
                attempt_rel = state_name + "/runs/" + identity + "/attempt-" + str(number)
                attempt_path = relative(root, attempt_rel)
                frames.directory(attempt_path.parent, create=True)
                attempt_path.mkdir()
                capsule, report = attempt_rel + "/capsule.json", attempt_rel + "/qualification.json"
                value = {
                    "schema": STATE_SCHEMA, "id": identity, "job": job, "policy_sha256": policy_sha,
                    "attempts": number, "max_attempts": policy["max_attempts"], "status": "running",
                    "phase": "qualification", "started_at": frames.utc_now(), "store": store_name,
                    "requested_model": job["requested_model"], "model_execution": "not_invoked",
                    "attempt_path": attempt_rel,
                }
                state_file = state / "jobs" / (identity + ".json")
                contracts.atomic_json(attempt_path / "intent.json", value)
                contracts.atomic_json(state_file, value)
                uncertain = True
                try:
                    check = frames.run_check(qualification_argv(job, capsule, report), root,
                                             policy["timeout_seconds"])
                    contracts.atomic_json(attempt_path / "command.json", check)
                    uncertain = False
                    require(frames.check_passed(check), "qualification command failed; evidence retained")
                    argv = validate_report(root, job, capsule, report, tree, manifest)
                    _, current_sha = contracts.load_manifest(relative(root, job["manifest_path"]), root)
                    require(current_sha == sha, "manifest changed during qualification")
                    require(attestation_paths(root, job) == closure_paths,
                            "dependency evidence changed during qualification")
                    artifacts = [*closure_paths, capsule, report]
                    value["phase"] = "recording"
                    contracts.atomic_json(state_file, value)
                    uncertain = True
                    receipt = recorder.record(job, number, artifacts, argv, policy["timeout_seconds"])
                    contracts.atomic_json(attempt_path / "receipt.json", receipt)
                    value.update(status="completed", phase="recorded", receipt=receipt)
                except (ValueError, OSError, TypeError, KeyError, subprocess.TimeoutExpired) as error:
                    value.update(status="recovery-required" if uncertain else "failed", reason=safe_error(error))
                value["finished_at"] = frames.utc_now()
                contracts.atomic_json(attempt_path / "outcome.json", value)
                contracts.atomic_json(state_file, value)
                return {**result, **{key: value[key] for key in ("status", "attempts", "attempt_path")},
                        "reason": value.get("reason", ""), "receipt": value.get("receipt")}
    except BusyError as error:
        return {**result, "status": "recovery-required", "reason": safe_error(error)}
    except (ValueError, OSError, TypeError, KeyError, subprocess.TimeoutExpired) as error:
        return {**result, "status": "blocked", "reason": safe_error(error)}


def run_plan(root, plan_name, policy_name, state_name, store_name, rapp_dir, jobs=None):
    root = frames.root_path(root)
    value, policy, state = validate_plan(root, plan_name, policy_name, state_name)
    maximum = policy["max_jobs"] if jobs is None else jobs
    require(type(maximum) is int and 1 <= maximum <= policy["max_jobs"], "--jobs exceeds caller policy")
    store = relative(root, store_name)
    require(not store.is_relative_to(state / "runs") and not state.is_relative_to(store),
            "job state and RAPP store must have separate layouts")
    results, selected, blocked_results = [], [], []
    for job in value["jobs"]:
        previous = read_job(state, job["id"])
        if (state / "locks" / (job["id"] + ".lock")).exists():
            blocked_results.append({
                "id": job["id"], "request_id": job["request_id"], "status": "recovery-required",
                "reason": "busy or stale job lock; no commands rerun",
                "requested_model": job["requested_model"], "model_execution": "not_invoked",
            })
        elif previous["status"] == "completed":
            # Completed replays still verify their stored receipt but consume no execution budget.
            results.append(job)
        elif previous["status"] in {"running", "recovery-required"}:
            blocked_results.append({
                "id": job["id"], "request_id": job["request_id"], "status": "recovery-required",
                "reason": "interrupted attempt; no commands rerun",
                "requested_model": job["requested_model"], "model_execution": "not_invoked",
            })
        elif previous["attempts"] >= policy["max_attempts"]:
            blocked_results.append({
                "id": job["id"], "request_id": job["request_id"], "status": "blocked",
                "reason": "attempt limit reached",
                "requested_model": job["requested_model"], "model_execution": "not_invoked",
            })
        elif len(selected) < maximum:
            selected.append(job)
    if not results and not selected:
        return {"schema": "localfirst-capability-run/v1", "status": "needs-attention" if blocked_results else "idle",
                "results": blocked_results, "blocked": value["blocked"], "limitations": LIMITATIONS}
    recorder = RappRecorder(root, store, rapp_dir)
    completed = blocked_results + [
        execute_job(root, state, state_name, store_name, job, policy, value["policy_sha256"], recorder)
        for job in results
    ]
    with ThreadPoolExecutor(max_workers=min(policy["max_parallel"], maximum)) as pool:
        futures = [pool.submit(execute_job, root, state, state_name, store_name, job,
                               policy, value["policy_sha256"], recorder) for job in selected]
        completed.extend(future.result() for future in futures)
    bad = any(item["status"] not in {"completed", "no-op"} for item in completed)
    return {
        "schema": "localfirst-capability-run/v1", "status": "needs-attention" if bad else "completed",
        "results": completed, "deferred": max(0, len(value["jobs"]) - len(completed)),
        "blocked": value["blocked"], "limitations": LIMITATIONS,
    }


def status(state_path):
    state = Path(os.path.abspath(state_path))
    frames.no_symlinks(state)
    identities = set()
    for directory, suffix in (("jobs", ".json"), ("runs", ""), ("locks", ".lock")):
        base = state / directory
        frames.no_symlinks(base)
        if base.exists():
            for item in base.iterdir():
                name = item.name[:-len(suffix)] if suffix and item.name.endswith(suffix) else item.name
                contracts.sha256(name)
                identities.add(name)
    summaries = []
    for identity in sorted(identities):
        previous = read_job(state, identity)
        locked = (state / "locks" / (identity + ".lock")).exists()
        current = previous["status"]
        if locked or current == "running":
            current = "recovery-required"
        action = {
            "completed": "No execution needed; explicit run can verify the stored receipt.",
            "recovery-required": "Wait for a live owner or inspect retained evidence; never steal locks or replay blindly.",
            "pending": "Create a bounded plan from explicit requests and policy.",
            "failed": "Attempt limit reached." if previous["attempts"] >= previous.get("max_attempts", 1)
                      else "Explicit run may attempt one bounded retry under the unchanged policy.",
        }[current]
        summaries.append({"id": identity, "status": current, "attempts": previous["attempts"],
                          "locked": locked, "next_action": action})
    slots = []
    base = state / "slots"
    frames.no_symlinks(base)
    if base.exists():
        for group in sorted(base.iterdir()):
            contracts.sha256(group.name)
            frames.no_symlinks(group)
            for entry in sorted(group.iterdir()):
                frames.no_symlinks(entry)
                slots.append(entry.relative_to(state).as_posix())
    return {"schema": "localfirst-capability-status/v1", "status": "idle" if not summaries and not slots else "observed",
            "jobs": summaries, "occupied_or_stale_slots": slots,
            "verification": "Stored state only; no commands run and no receipt reverified.",
            "limitations": LIMITATIONS}


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    for command in ("plan", "run"):
        child = sub.add_parser(command)
        child.add_argument("--root", required=True)
        child.add_argument("--policy", required=True)
        child.add_argument("--state", required=True)
        if command == "plan":
            for name in ("registry", "requests", "output"):
                child.add_argument("--" + name, required=True)
        else:
            child.add_argument("--plan", required=True)
            child.add_argument("--store", required=True)
            child.add_argument("--rapp-dir", required=True)
            child.add_argument("--jobs", type=int)
    sub.add_parser("status").add_argument("--state", required=True)
    return cli


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "plan":
            value = plan(args.root, args.registry, args.requests, args.policy, args.state, args.output)
        elif args.command == "run":
            value = run_plan(args.root, args.plan, args.policy, args.state, args.store, args.rapp_dir, args.jobs)
        else:
            value = status(args.state)
        print(json.dumps(value, indent=2, allow_nan=False))
        return 1 if value["status"] == "needs-attention" else 0
    except (ValueError, OSError, TypeError, KeyError, RecursionError, subprocess.TimeoutExpired) as error:
        print("error: " + safe_error(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
