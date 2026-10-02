#!/usr/bin/env python3
"""Read-only capability discovery and RAPP-bound qualification projection.

Manifest commands are data, never executed here. build writes only its explicit
registry output; verify regenerates the projection from current source pins and
immutable evidence rather than trusting cached status or approval assertions.
"""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import sys

if __package__:
    from . import autocomplete_frames as frames
    from . import capability_contracts as contracts
else:
    import autocomplete_frames as frames
    import capability_contracts as contracts


MAX_MANIFESTS = 128
MAX_DIRECTORY_ENTRIES = 4096
MAX_REPORTS = 4096
MAX_CAPSULE_FILES = 1024
MAX_EVIDENCE_BYTES = 64 * 1024 * 1024
MANIFEST_FIELDS = {
    "schema", "id", "version", "title", "job", "entrypoint", "artifacts",
    "contract", "checks", "failure_cases", "reuses", "visibility",
}
USE_FIELDS = {
    "repository", "commit", "tree", "workflow", "frame_path", "frame_hash",
    "report_sha256", "capsule_sha256",
}
ASSET_FIELDS = (MANIFEST_FIELDS - {"schema"}) | {
    "manifest_path", "manifest_sha256", "status", "uses", "distinct_repositories", "failures",
}
CHECK_FIELDS = {
    "argv", "exit_code", "timed_out", "launch_error", "capture_complete",
    "timeout_seconds", "duration_ms", "stdout_sha256", "stdout_bytes",
    "stderr_sha256", "stderr_bytes",
}
REPOSITORY = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})/[A-Za-z0-9][A-Za-z0-9._-]{0,99}")
LIMITATIONS = [
    "built means current manifest and code bytes validate; it is not qualification or production acceptance.",
    "proven requires a qualifying immutable report, capsule, pinned implementation, and a successful recorded replay command in the same verified RAPP frame.",
    "reused requires different public repository identities with different commits and trees; copies, path aliases, repeated frames, and model or reviewer metadata do not establish transfer.",
    "No asset is automatically promoted to shared-default, core, or production. Permission labels are declarations from the common contract, not granted authority.",
    "The registry does not execute manifest checks, generated prompts, replay commands, or network requests.",
    "Unsigned RAPP receipts establish integrity and lineage, not authenticated human authorship, trusted time, correctness in every context, demonstrated user demand, or legal priority.",
    "Search scores are deterministic discovery heuristics, not measured demand or evidence of successful reuse. Verify a saved projection against source and evidence before relying on its status.",
]


class Unqualified(ValueError):
    """A well-addressed report is retained, but cannot graduate the asset."""


def require_use(condition, reason):
    if not condition:
        raise Unqualified(reason)


def public_values(value):
    pending = [(value, 0)]
    count = 0
    while pending:
        item, depth = pending.pop()
        count += 1
        contracts.require(depth <= 32 and count <= 200000, "public metadata exceeds structural limits")
        if isinstance(item, str):
            contracts.require(not frames.ABSOLUTE_TEXT.search(item) and not frames.PRIVATE_TEXT.search(item),
                              "local paths or secret-oriented values are not public registry metadata")
        elif isinstance(item, dict):
            pending.extend((key, depth + 1) for key in item)
            pending.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            pending.extend((child, depth + 1) for child in item)


def relative(root, name, directory=False):
    selected = frames.relative_path(name)
    frames.artifact_path(name + "/manifest.json" if directory else name)
    path = root.joinpath(*selected.parts)
    frames.no_symlinks(path)
    return path


def manifest_locations(root, manifests=None, manifest_paths=None):
    contracts.require(bool(manifests) != bool(manifest_paths),
                      "select either a manifest directory or explicit --manifest paths")
    if manifest_paths:
        contracts.require(0 < len(manifest_paths) <= MAX_MANIFESTS
                          and len(set(manifest_paths)) == len(manifest_paths),
                          "duplicate or excessive explicit manifest paths")
        locations = [relative(root, name) for name in manifest_paths]
    else:
        directory = relative(root, manifests, directory=True)
        frames.directory(directory)
        pending, locations, count = [(directory, 0)], [], 0
        while pending:
            directory, depth = pending.pop()
            contracts.require(depth <= 16, "manifest directory nesting exceeds limit")
            for path in sorted(directory.iterdir()):
                count += 1
                contracts.require(count <= MAX_DIRECTORY_ENTRIES, "manifest directory entry limit exceeded")
                frames.no_symlinks(path)
                if path.is_dir():
                    relative(root, path.relative_to(root).as_posix(), directory=True)
                    pending.append((path, depth + 1))
                elif path.suffix.lower() == ".json":
                    locations.append(path)
                    contracts.require(len(locations) <= MAX_MANIFESTS, "manifest count exceeds limit")
    contracts.require(locations, "no capability manifests found")
    return sorted(locations)


def dependencies(inventory):
    for info in inventory.values():
        for dependency in info["manifest"]["reuses"]:
            contracts.require(dependency["id"] in inventory, "missing capability dependency: " + dependency["id"])
    active, done, closures = set(), set(), {}

    def visit(identifier):
        contracts.require(identifier not in active, "cyclic capability dependency")
        if identifier in done:
            return closures[identifier]
        active.add(identifier)
        result = {identifier}
        for dependency in inventory[identifier]["manifest"]["reuses"]:
            result.update(visit(dependency["id"]))
        active.remove(identifier)
        done.add(identifier)
        closures[identifier] = result
        return result

    for identifier in sorted(inventory):
        visit(identifier)
    for info in inventory.values():
        for dependency in info["manifest"]["reuses"]:
            contracts.require(inventory[dependency["id"]]["sha256"] == dependency["manifest_sha256"],
                              "dependency manifest hash/version drift: " + dependency["id"])
    return closures


def load_inventory(root, manifests=None, manifest_paths=None):
    inventory = {}
    for path in manifest_locations(root, manifests, manifest_paths):
        relative(root, path.relative_to(root).as_posix())
        manifest, sha = contracts.load_manifest(path, root)
        raw = frames.read_bytes(path, contracts.MAX_MANIFEST_BYTES)
        contracts.require(frames.digest(raw) == sha
                          and contracts.json_bytes(parse_json(raw)) == contracts.json_bytes(manifest),
                          "manifest changed while loading")
        public_values(manifest)
        contracts.require(manifest["id"] not in inventory, "duplicate capability identifier: " + manifest["id"])
        inventory[manifest["id"]] = {
            "manifest": manifest, "path": path.relative_to(root).as_posix(),
            "sha256": sha, "bytes": len(raw),
        }
    return inventory, dependencies(inventory)


def parse_json(raw):
    return json.loads(raw, object_pairs_hook=frames.unique_pairs,
                      parse_constant=frames.reject_constant, parse_float=frames.reject_constant)


def repository_identity(value):
    contracts.require(isinstance(value, str) and REPOSITORY.fullmatch(value)
                      and not value.casefold().endswith(".git"),
                      "repository must be public owner/name, not a local path or clone URL")
    return value.casefold()


def source_context(value):
    contracts.require(isinstance(value, dict)
                      and {"repository", "commit", "tree", "workflow"} <= value.keys(),
                      "invalid qualification context")
    return {
        "repository": repository_identity(value["repository"]),
        "commit": contracts.committed_ref(value["commit"]),
        "tree": contracts.committed_ref(value["tree"]),
        "workflow": frames.public_text(value["workflow"], 256),
    }


def valid_passing_check(check, expected):
    contracts.require(isinstance(check, dict) and set(check) == CHECK_FIELDS, "invalid qualification check")
    frames.check_argv(check["argv"])
    require_use(check["argv"] == expected["argv"]
                and type(check["timeout_seconds"]) is int
                and check["timeout_seconds"] == expected["timeout_seconds"],
                "manifest_checks_mismatch")
    require_use(type(check["exit_code"]) is int and check["exit_code"] == 0
                and check["timed_out"] is False and check["capture_complete"] is True
                and check["launch_error"] is None, "qualification_check_failed")
    contracts.require(frames.valid_uint(check["duration_ms"]), "invalid check duration")
    for stream in ("stdout", "stderr"):
        contracts.sha256(check[stream + "_sha256"])
        contracts.require(frames.valid_uint(check[stream + "_bytes"]), "invalid output byte count")


def argument_value(argv, flag):
    values = []
    for index, argument in enumerate(argv):
        if argument == flag:
            require_use(index + 1 < len(argv) and not argv[index + 1].startswith("--"),
                        "replay_file_binding_missing")
            values.append(argv[index + 1])
        elif argument.startswith(flag + "="):
            values.append(argument[len(flag) + 1:])
    require_use(len(values) == 1, "replay_file_binding_missing")
    frames.artifact_path(values[0])
    return values[0]


def capsule_envelope(capsule, context):
    contracts.require(isinstance(capsule, dict) and capsule.get("schema") == contracts.CAPSULE_SCHEMA,
                      "invalid capsule envelope")
    origin = capsule.get("origin")
    contracts.require(isinstance(origin, dict) and {"repository", "commit", "tree"} <= origin.keys(),
                      "invalid capsule origin")
    require_use(repository_identity(origin["repository"]) == context["repository"]
                and contracts.committed_ref(origin["commit"]) == context["commit"]
                and contracts.committed_ref(origin["tree"]) == context["tree"],
                "capsule_context_mismatch")
    files, totals = capsule.get("files"), capsule.get("totals")
    contracts.require(isinstance(files, list) and 1 <= len(files) <= MAX_CAPSULE_FILES
                      and isinstance(totals, dict), "invalid capsule file inventory")
    seen, total = set(), 0
    for file in files:
        contracts.require(isinstance(file, dict) and {"path", "mode", "sha256", "bytes", "text"} <= file.keys(),
                          "invalid capsule file")
        frames.artifact_path(file["path"])
        contracts.require(file["path"] not in seen, "duplicate capsule file path")
        seen.add(file["path"])
        contracts.require(file["mode"] in ("100644", "100755"), "capsule must contain regular Git source files")
        contracts.sha256(file["sha256"])
        contracts.require(type(file["bytes"]) is int and 0 <= file["bytes"] <= contracts.MAX_JSON_BYTES
                          and isinstance(file["text"], str), "invalid capsule file bytes")
        data = file["text"].encode("utf-8")
        require_use(frames.digest(data) == file["sha256"] and len(data) == file["bytes"],
                    "capsule_file_fingerprint_mismatch")
        total += len(data)
        contracts.require(total <= contracts.MAX_JSON_BYTES, "capsule content exceeds byte limit")
    require_use(type(totals.get("files")) is int and totals["files"] == len(files)
                and type(totals.get("bytes")) is int and totals["bytes"] == total,
                "capsule_totals_mismatch")


def load_evidence(root, store, rapp_dir):
    if store is None:
        return None, [], {"state": "not_configured", "store": None, "frames": 0, "unmatched_reports": []}
    path = relative(root, store, directory=True)
    if not path.exists():
        return None, [], {"state": "missing_store", "store": store, "frames": 0, "unmatched_reports": []}
    frames.directory(path)
    contracts.require(rapp_dir is not None, "--rapp-dir is required for an existing evidence store")
    reference = frames.Reference(rapp_dir)
    index = frames.evidence_index(path, reference)
    verified, heads = [], {}
    # Read the actual payloads, never a mutable index.json's projection claims.
    for event in sorted(index["events"], key=lambda item: (item["stream_id"], item["seq"])):
        frames.frame_location(event["path"])
        frame = frames.read_json(path / event["path"])
        contracts.require(isinstance(frame, dict), "invalid evidence frame")
        ok, _, _ = reference.rapp.verify_frame(
            frame, head=heads.get(event["stream_id"]), stream_id_of_record=event["stream_id"],
        )
        contracts.require(ok and frame["frame_hash"] == event["frame_hash"],
                          "evidence changed after canonical verification")
        heads[event["stream_id"]] = frame
        verified.append((event["path"], frame))
    verified.sort(key=lambda pair: (pair[1]["utc"], pair[1]["frame_hash"], pair[0]))
    return path, verified, {
        "state": "verified", "store": store, "frames": index["verification"]["canonical_scanned_frames"],
        "rappid": index["rappid"], "reference": index["reference"], "unmatched_reports": [],
    }


def qualify(report, artifact, frame_path, frame, info, inventory, closure, blob):
    required = {"schema", "capability", "context", "capsule", "outcome", "gates", "checks",
                "replay_argv", "limitations"}
    contracts.require(isinstance(report, dict) and required <= report.keys(), "invalid qualification report")
    capability = report["capability"]
    contracts.require(isinstance(capability, dict) and {"id", "manifest_sha256"} <= capability.keys(),
                      "invalid qualification capability")
    contracts.identifier(capability["id"])
    contracts.sha256(capability["manifest_sha256"])
    require_use(capability["id"] == info["manifest"]["id"]
                and capability["manifest_sha256"] == info["sha256"], "manifest_revision_mismatch")
    context = source_context(report["context"])
    require_use(report["outcome"] == "passed", "qualification_failed")
    gates = report["gates"]
    require_use(isinstance(gates, dict) and all(gates.get(key) is True for key in
                ("source_matches", "round_trip", "artifacts_stable")), "qualification_gates_failed")
    payload = frame["payload"]
    require_use(payload["phase"] in {"implementation", "review", "integration"}, "non_implementation_frame")
    require_use(payload["outcome"] == "checks_passed" and not payload["changed_artifacts"]
                and payload["base_commit_unchanged"] is True, "frame_checks_or_inputs_failed")
    checks = report["checks"]
    expected = info["manifest"]["checks"]
    require_use(isinstance(checks, list) and len(checks) == len(expected) and checks,
                "manifest_checks_mismatch")
    for check, definition in zip(checks, expected):
        valid_passing_check(check, definition)
    argv = report["replay_argv"]
    try:
        contracts.validate_source_replay(argv, info["manifest"]["entrypoint"])
    except ValueError:
        require_use(False, "not_capability_replay")
    require_use(any(check["argv"] == argv and frames.check_passed(check) for check in payload["checks"]),
                "replay_command_not_recorded")
    attested = {item["path"]: item for item in payload["artifacts"]}
    require_use(argument_value(argv, "--report") == artifact["path"], "report_command_binding_mismatch")
    manifest_path = argument_value(argv, "--manifest")
    capsule_path = argument_value(argv, "--capsule")
    require_use(manifest_path in attested and attested[manifest_path]["sha256"] == info["sha256"]
                and attested[manifest_path]["bytes"] == info["bytes"], "manifest_not_attested")
    for identifier in sorted(closure):
        dependency = inventory[identifier]
        require_use(any(item["sha256"] == dependency["sha256"] and item["bytes"] == dependency["bytes"]
                        for item in attested.values()), "dependency_manifest_not_attested")
        for source in dependency["manifest"]["artifacts"]:
            require_use(source["path"] in attested and attested[source["path"]] == source,
                        "implementation_artifact_not_attested")
            blob(source)
    capsule_ref = report["capsule"]
    contracts.require(isinstance(capsule_ref, dict) and {"sha256", "bytes"} <= capsule_ref.keys(),
                      "invalid capsule reference")
    contracts.sha256(capsule_ref["sha256"])
    contracts.require(type(capsule_ref["bytes"]) is int and 0 <= capsule_ref["bytes"] <= contracts.MAX_JSON_BYTES,
                      "invalid capsule byte count")
    require_use(capsule_path in attested and capsule_path != artifact["path"]
                and attested[capsule_path]["sha256"] == capsule_ref["sha256"]
                and attested[capsule_path]["bytes"] == capsule_ref["bytes"], "capsule_not_attested")
    capsule_envelope(parse_json(blob(attested[capsule_path])), context)
    contracts.require(isinstance(report["limitations"], list)
                      and len(report["limitations"]) <= 64
                      and all(isinstance(item, str) and len(item) <= 4096 for item in report["limitations"]),
                      "invalid report limitations")
    return {**context, "frame_path": frame_path, "frame_hash": frame["frame_hash"],
            "report_sha256": artifact["sha256"], "capsule_sha256": capsule_ref["sha256"]}


def derive_uses(root, inventory, closures, store, rapp_dir):
    store_path, history, provenance = load_evidence(root, store, rapp_dir)
    uses = {identifier: {} for identifier in inventory}
    failures = {identifier: {} for identifier in inventory}
    raw_cache = {}
    cached_bytes = 0

    def blob(artifact):
        nonlocal cached_bytes
        sha = artifact["sha256"]
        if sha not in raw_cache:
            raw = frames.read_bytes(store_path / "objects" / "sha256" / sha, contracts.MAX_JSON_BYTES)
            contracts.require(frames.digest(raw) == sha, "immutable evidence object hash mismatch")
            cached_bytes += len(raw)
            contracts.require(cached_bytes <= MAX_EVIDENCE_BYTES, "evidence input exceeds 64 MiB")
            raw_cache[sha] = raw
        contracts.require(len(raw_cache[sha]) == artifact["bytes"], "immutable evidence object size mismatch")
        return raw_cache[sha]

    reports = 0
    for frame_path, frame in history:
        for artifact in frame["payload"]["artifacts"]:
            blob(artifact)
        for artifact in frame["payload"]["artifacts"]:
            raw = blob(artifact)
            if not raw.lstrip().startswith(b"{"):
                continue
            try:
                report = parse_json(raw)
            except (ValueError, UnicodeError, RecursionError):
                if contracts.QUALIFICATION_SCHEMA.encode("ascii") not in raw:
                    continue
                report = {"schema": contracts.QUALIFICATION_SCHEMA}
            if not isinstance(report, dict) or report.get("schema") != contracts.QUALIFICATION_SCHEMA:
                continue
            reports += 1
            contracts.require(reports <= MAX_REPORTS, "qualification report limit exceeded")
            capability = report.get("capability")
            identifier = capability.get("id") if isinstance(capability, dict) else None
            failure = {"frame_path": frame_path, "frame_hash": frame["frame_hash"],
                       "report_sha256": artifact["sha256"], "reason": "unknown_capability"}
            if not isinstance(identifier, str) or identifier not in inventory:
                provenance["unmatched_reports"].append(failure)
                continue
            try:
                use = qualify(report, artifact, frame_path, frame, inventory[identifier],
                              inventory, closures[identifier], blob)
            except Unqualified as exc:
                failure["reason"] = str(exc)
            except (contracts.ContractError, frames.EvidenceError, ValueError, TypeError, UnicodeError, RecursionError):
                failure["reason"] = "invalid_qualification_report"
            else:
                key = tuple(use[name] for name in
                            ("repository", "commit", "tree", "report_sha256", "capsule_sha256"))
                uses[identifier].setdefault(key, use)
                continue
            failures[identifier].setdefault((artifact["sha256"], failure["reason"]), failure)
    return uses, failures, provenance


def independent_reuse(uses):
    contexts = sorted({(use["repository"], use["commit"], use["tree"]) for use in uses})
    if any(len({context[index] for context in contexts}) < 2 for index in range(3)):
        return False
    return any(all(left[index] != right[index] for index in range(3))
               for position, left in enumerate(contexts) for right in contexts[position + 1:])


def build_registry(root, manifests=None, store=None, rapp_dir=None, manifest_paths=None):
    root = frames.root_path(root)
    inventory, closures = load_inventory(root, manifests, manifest_paths)
    uses, failures, provenance = derive_uses(root, inventory, closures, store, rapp_dir)
    assets = []
    for identifier, info in sorted(inventory.items()):
        witnesses = [use for _, use in sorted(uses[identifier].items())]
        status = "reused" if independent_reuse(witnesses) else "proven" if witnesses else "built"
        assets.append({
            **{key: value for key, value in info["manifest"].items() if key != "schema"},
            "manifest_path": info["path"], "manifest_sha256": info["sha256"],
            "status": status, "uses": witnesses,
            "distinct_repositories": len({use["repository"] for use in witnesses}),
            "failures": [failure for _, failure in sorted(failures[identifier].items())],
        })
    result = {
        "schema": contracts.REGISTRY_SCHEMA, "generated_at": frames.utc_now(), "assets": assets,
        "summary": {"assets": len(assets), **{status: sum(asset["status"] == status for asset in assets)
                                            for status in ("built", "proven", "reused")}},
        "evidence": provenance, "limitations": LIMITATIONS,
    }
    contracts.require(len(contracts.json_bytes(result)) <= contracts.MAX_JSON_BYTES, "registry exceeds byte limit")
    return result


def validate_projection(value):
    contracts.require(isinstance(value, dict) and value.get("schema") == contracts.REGISTRY_SCHEMA,
                      "invalid capability registry schema")
    contracts.require(isinstance(value.get("generated_at"), str)
                      and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z",
                                       value["generated_at"]), "invalid registry UTC")
    try:
        datetime.strptime(value["generated_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as exc:
        raise contracts.ContractError("invalid registry UTC") from exc
    assets = value.get("assets")
    contracts.require(isinstance(assets, list) and 1 <= len(assets) <= MAX_MANIFESTS, "invalid registry assets")
    identifiers = set()
    for asset in assets:
        contracts.require(isinstance(asset, dict) and set(asset) == ASSET_FIELDS, "invalid registry asset fields")
        manifest = {key: asset.get(key) for key in MANIFEST_FIELDS}
        manifest["schema"] = contracts.CAPABILITY_SCHEMA
        contracts.validate_manifest(manifest)
        contracts.require(asset["id"] not in identifiers, "duplicate registry asset")
        identifiers.add(asset["id"])
        frames.artifact_path(asset.get("manifest_path"))
        contracts.sha256(asset.get("manifest_sha256"))
        uses = asset.get("uses")
        contracts.require(isinstance(uses, list) and len(uses) <= MAX_REPORTS, "invalid registry uses")
        keys = set()
        for use in uses:
            contracts.require(isinstance(use, dict) and set(use) == USE_FIELDS, "invalid use projection")
            contracts.require(source_context(use)["repository"] == use["repository"],
                              "noncanonical repository identity")
            frames.frame_location(use["frame_path"])
            for name in ("frame_hash", "report_sha256", "capsule_sha256"):
                contracts.sha256(use[name])
            key = tuple(use[name] for name in ("repository", "commit", "tree", "report_sha256", "capsule_sha256"))
            contracts.require(key not in keys, "duplicate projected use")
            keys.add(key)
        status = "reused" if independent_reuse(uses) else "proven" if uses else "built"
        contracts.require(asset.get("status") == status
                          and type(asset.get("distinct_repositories")) is int
                          and asset["distinct_repositories"] == len({use["repository"] for use in uses}),
                          "projected status/count does not follow uses")
        contracts.require(isinstance(asset.get("failures"), list) and len(asset["failures"]) <= MAX_REPORTS,
                          "invalid failure projection")
    summary = {"assets": len(assets), **{status: sum(asset["status"] == status for asset in assets)
                                       for status in ("built", "proven", "reused")}}
    contracts.require(contracts.json_bytes(value.get("summary")) == contracts.json_bytes(summary),
                      "invalid registry summary")
    public_values(value)
    return value


def verify_registry(root, registry, manifests=None, store=None, rapp_dir=None, manifest_paths=None):
    root = frames.root_path(root)
    existing = validate_projection(contracts.load_json(relative(root, registry)))
    expected = build_registry(root, manifests, store, rapp_dir, manifest_paths)
    without_time = lambda value: {key: item for key, item in value.items() if key != "generated_at"}
    contracts.require(contracts.json_bytes(without_time(existing)) == contracts.json_bytes(without_time(expected)),
                      "registry projection is stale or tampered")
    return {"schema": "localfirst-capability-registry-verification/v1", "verified": True,
            "summary": expected["summary"], "evidence": expected["evidence"]}


def search_registry(registry, query, limit=10):
    path = Path(os.path.abspath(registry))
    frames.no_symlinks(path)
    value = validate_projection(contracts.load_json(path))
    frames.public_text(query, 512)
    contracts.require(type(limit) is int and 1 <= limit <= 100, "search limit must be 1-100")
    terms = set(re.findall(r"\w+", query.casefold()))
    contracts.require(terms, "query must contain searchable job terms")
    matches = []
    for asset in value["assets"]:
        score = 0
        for field, weight in (("job", 10), ("title", 6), ("id", 4), ("contract", 2), ("failure_cases", 1)):
            text = asset[field] if isinstance(asset[field], str) else json.dumps(asset[field], sort_keys=True)
            score += weight * len(terms & set(re.findall(r"\w+", text.casefold())))
        if score:
            matches.append({**asset, "discovery_score": score})
    matches.sort(key=lambda asset: (-asset["discovery_score"], asset["id"], asset["manifest_sha256"]))
    return {"schema": "localfirst-capability-search/v1", "query": query, "projection_only": True,
            "matches": matches[:limit], "limitations": LIMITATIONS}


def write_registry(root, output, result, manifests=None, store=None):
    root = frames.root_path(root)
    destination = relative(root, output)
    contracts.require(destination.suffix.lower() == ".json", "registry output must be JSON")
    if manifests:
        contracts.require(not destination.is_relative_to(relative(root, manifests, directory=True)),
                          "registry output must be outside the manifest directory")
    if store:
        contracts.require(not destination.is_relative_to(relative(root, store, directory=True)),
                          "registry output must be outside the immutable evidence store")
    protected = {asset["manifest_path"] for asset in result["assets"]}
    protected.update(artifact["path"] for asset in result["assets"] for artifact in asset["artifacts"])
    contracts.require(output not in protected, "registry output would overwrite an input")
    return contracts.atomic_json(destination, result)


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    for command in ("build", "verify"):
        child = sub.add_parser(command)
        child.add_argument("--root", required=True)
        location = child.add_mutually_exclusive_group(required=True)
        location.add_argument("--manifests", help="relative directory containing only capability JSON manifests")
        location.add_argument("--manifest", action="append", dest="manifest_paths", help="explicit relative manifest; repeatable")
        child.add_argument("--store", help="relative RAPP store; omitted/missing means explicitly unqualified built-only")
        child.add_argument("--rapp-dir", help="required for an existing store; byte-pinned canonical RAPP checkout")
        child.add_argument("--output" if command == "build" else "--registry", required=True)
    search = sub.add_parser("search")
    search.add_argument("--registry", required=True)
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=10)
    return cli


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "search":
            result = search_registry(args.registry, args.query, args.limit)
        else:
            options = {"root": args.root, "manifests": args.manifests, "manifest_paths": args.manifest_paths,
                       "store": args.store, "rapp_dir": args.rapp_dir}
            if args.command == "verify":
                result = verify_registry(registry=args.registry, **options)
            else:
                result = build_registry(**options)
                write_registry(args.root, args.output, result, args.manifests, args.store)
        print(contracts.json_bytes(result).decode("utf-8"), end="")
        return 0
    except (contracts.ContractError, frames.EvidenceError, ValueError, TypeError, RecursionError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        return 2
    except OSError as exc:
        print("error: local file operation failed (" + type(exc).__name__ + ")", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
