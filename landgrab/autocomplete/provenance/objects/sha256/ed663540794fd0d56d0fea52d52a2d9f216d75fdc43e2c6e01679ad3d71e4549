"""Scheduler tests with real local Git/input/command fixtures.

The recording seam executes real replay commands but is deliberately NOT a RAPP
implementation. Protocol integration is covered by the existing recorder suite.
All disposable files live in this checkout; no installations or network access.
"""

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import unittest
import uuid
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import capability_scheduler as scheduler


PACKAGE = r'''
import argparse, hashlib, json, pathlib, subprocess, sys, time
p = argparse.ArgumentParser()
p.add_argument("command", choices=["qualify", "verify"])
for name in ["root", "manifest", "repo", "ref", "repository", "workflow", "capsule", "report"]:
    p.add_argument("--" + name)
p.add_argument("--path", action="append")
p.add_argument("--allow-checks", action="store_true")
p.add_argument("--replay", action="store_true")
a = p.parse_args()
root = pathlib.Path(".")
behavior = json.loads((root / "behavior.json").read_text())
mode = behavior.get("mode", "")
with (root / (a.command + "-calls.txt")).open("a") as out:
    out.write("actual command\n")
if a.command == "verify":
    capsule = pathlib.Path(a.capsule).read_bytes()
    report = json.loads(pathlib.Path(a.report).read_text())
    assert hashlib.sha256(capsule).hexdigest() == report["capsule"]["sha256"]
    sys.exit(7 if mode == "replay-fail" else 0)
if mode == "timeout":
    time.sleep(5)
if mode == "slow":
    time.sleep(.4)
if mode == "exit-fail":
    print("deliberate qualification failure", file=sys.stderr)
    sys.exit(4)
if mode == "missing-report":
    sys.exit(0)
manifest_raw = pathlib.Path(a.manifest).read_bytes()
manifest = json.loads(manifest_raw)
checks = []
for check in manifest["checks"]:
    result = subprocess.run(check["argv"], capture_output=True, timeout=check["timeout_seconds"])
    checks.append(dict(
        argv=check["argv"], exit_code=result.returncode, timed_out=False, launch_error=None,
        capture_complete=True, timeout_seconds=check["timeout_seconds"], duration_ms=1,
        stdout_sha256=hashlib.sha256(result.stdout).hexdigest(), stdout_bytes=len(result.stdout),
        stderr_sha256=hashlib.sha256(result.stderr).hexdigest(), stderr_bytes=len(result.stderr)))
tree = subprocess.check_output(["git", "-C", a.repo, "rev-parse", a.ref + "^{tree}"]).decode().strip()
context = dict(repository=a.repository, commit=a.ref, tree=tree, workflow=a.workflow)
capsule = json.dumps(dict(schema="fixture-only", context=context, paths=a.path)).encode()
pathlib.Path(a.capsule).write_bytes(capsule)
argv = ["python3", "scripts/capability_package.py", "verify", "--root", ".",
        "--manifest", a.manifest, "--repo", a.repo, "--capsule", a.capsule,
        "--report", a.report, "--replay", "--allow-checks"]
if mode == "bad-replay":
    argv = ["python3", "-c", "raise RuntimeError('unapproved command')"]
if mode == "missing-replay":
    argv.remove("--replay")
if mode == "missing-replay-permission":
    argv.remove("--allow-checks")
report = dict(
    schema="localfirst-capability-qualification/v1",
    capability=dict(id=manifest["id"], manifest_sha256=hashlib.sha256(manifest_raw).hexdigest()),
    context=context, capsule=dict(sha256=hashlib.sha256(capsule).hexdigest(), bytes=len(capsule)),
    outcome="failed" if mode == "failed-gate" else "passed",
    gates=dict(source_matches=True, round_trip=True, artifacts_stable=True),
    checks=checks, replay_argv=argv, limitations=["Test executable, not the real package builder."])
if mode == "bad-context":
    report["context"]["repository"] = "different/repo"
if mode == "bad-capsule":
    report["capsule"]["sha256"] = "0" * 64
if mode == "false-check":
    report["checks"][0]["exit_code"] = False
if mode == "private-metadata":
    report["limitations"] = [str(pathlib.Path(".").resolve())]
if mode == "malformed-section":
    report["capability"] = None
pathlib.Path(a.report).write_text(json.dumps(report))
if mode == "mutate-code":
    with pathlib.Path("scripts/capability_package.py").open("a") as out:
        out.write("\n# changed during qualification\n")
'''


class RecordingSeam:
    """Test-only injected adapter: actual replay, no fabricated protocol claim."""

    def __init__(self, root, store, rapp_dir):
        self.root, self.store = Path(root), Path(store)
        if not self.store.is_dir():
            raise ValueError("test recorder prerequisite missing")

    def prepare(self, identity, attempt):
        scheduler.contracts.sha256(identity)
        assert 1 <= attempt <= 3

    def record(self, job, attempt, artifacts, argv, timeout):
        before = {path: hashlib.sha256((self.root / path).read_bytes()).hexdigest() for path in artifacts}
        check = scheduler.frames.run_check(argv, self.root, timeout)
        if not scheduler.frames.check_passed(check):
            raise ValueError("actual replay command failed")
        result = {"test_seam_not_rapp": True, "artifacts": before, "check": check}
        self.verify(job, attempt, result)
        return result

    def verify(self, job, attempt, receipt):
        if not receipt.get("test_seam_not_rapp"):
            raise ValueError("not a test recording receipt")
        for path, sha in receipt["artifacts"].items():
            if hashlib.sha256((self.root / path).read_bytes()).hexdigest() != sha:
                raise ValueError("recorded artifact changed")
        if not scheduler.frames.check_passed(receipt["check"]):
            raise ValueError("recorded command did not pass")


class CapabilitySchedulerTests(unittest.TestCase):
    def setUp(self):
        self.fixture = ROOT / (".capability-scheduler-test-" + uuid.uuid4().hex)
        self.fixture.mkdir()
        self.addCleanup(shutil.rmtree, self.fixture)
        self.root = self.fixture / "code"
        self.source = self.fixture / "source"
        (self.root / "scripts").mkdir(parents=True)
        self.source.mkdir()
        (self.root / "scripts/capability_package.py").write_text(PACKAGE)
        (self.root / "helper.txt").write_text("pinned helper\n")
        (self.source / "public.py").write_text("print('committed fixture')\n")
        self.git("init", "--quiet")
        self.git("add", "public.py")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "disposable test input")
        self.commit = self.git("rev-parse", "HEAD").stdout.strip()
        self.manifest = {
            "schema": scheduler.contracts.CAPABILITY_SCHEMA, "id": "source-capsule",
            "version": "1.0.0", "title": "Fixture source capsule", "job": "Qualify explicit source inputs.",
            "entrypoint": scheduler.ENTRYPOINT,
            "artifacts": [self.artifact("scripts/capability_package.py"), self.artifact("helper.txt")],
            "contract": {"inputs": {"type": "object"}, "outputs": {"type": "object"},
                         "permissions": sorted(scheduler.contracts.PERMISSIONS), "network": "none"},
            "checks": [{"id": "fixture-check", "argv": ["python3", "-c", "print('real check')"],
                        "timeout_seconds": 1}],
            "failure_cases": ["A selected path is missing."], "reuses": [], "visibility": "public",
        }
        self.write("manifest.json", self.manifest)
        self.sha = self.digest("manifest.json")
        self.registry = {"schema": scheduler.contracts.REGISTRY_SCHEMA, "assets": [self.asset()]}
        self.policy = {
            "schema": scheduler.POLICY_SCHEMA, "allowed_capabilities": [self.sha],
            "permissions": sorted(scheduler.contracts.PERMISSIONS),
            "max_jobs": 1, "max_parallel": 1, "max_attempts": 2,
            "timeout_seconds": 10, "visibility": "private",
        }
        self.request = {
            "id": "request-one", "capability_id": "source-capsule", "source_repo": "../source",
            "source_commit": self.commit, "repository": "fixture/source", "workflow": "snapshot",
            "paths": ["public.py"], "trigger": {"kind": "manual", "key": "operator-one"},
            "requested_model": "gpt-6-astra",
        }
        self.requests = {"schema": scheduler.REQUEST_SCHEMA, "requests": [self.request]}
        self.write_inputs()
        self.write("behavior.json", {})
        (self.root / "rapp-store").mkdir()

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.source), *args], capture_output=True, text=True,
            check=True, timeout=10, env={**os.environ, "GIT_CONFIG_NOSYSTEM": "1",
                                       "GIT_CONFIG_GLOBAL": os.devnull},
        )

    def artifact(self, path):
        data = (self.root / path).read_bytes()
        return {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}

    def digest(self, path):
        return hashlib.sha256((self.root / path).read_bytes()).hexdigest()

    def write(self, path, value):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(value))

    def asset(self):
        return {**copy.deepcopy(self.manifest), "manifest_path": "manifest.json",
                "manifest_sha256": self.sha, "status": "built", "uses": [],
                "distinct_repositories": 0, "failures": []}

    def write_inputs(self):
        self.write("registry.json", self.registry)
        self.write("requests.json", self.requests)
        self.write("policy.json", self.policy)

    def repin(self):
        self.write("manifest.json", self.manifest)
        self.sha = self.digest("manifest.json")
        self.registry["assets"][0] = self.asset()
        self.policy["allowed_capabilities"] = [self.sha]
        self.write_inputs()

    def plan(self):
        return scheduler.plan(self.root, "registry.json", "requests.json", "policy.json", "state", "plan.json")

    def run_job(self, **kwargs):
        with patch.object(scheduler, "RappRecorder", RecordingSeam):
            return scheduler.run_plan(self.root, "plan.json", "policy.json", "state", "rapp-store",
                                      "unused-test-reference", **kwargs)

    def calls(self, kind):
        path = self.root / (kind + "-calls.txt")
        return len(path.read_text().splitlines()) if path.exists() else 0

    def assert_blocked(self):
        value = self.plan()
        self.assertEqual(value["status"], "idle")
        self.assertFalse(value["jobs"])
        self.assertTrue(value["blocked"])
        self.assertEqual(self.calls("qualify"), 0)
        return value

    def rewrite_plan(self, value, retained=False):
        value["plan_sha256"] = scheduler.contracts.digest(scheduler.contracts.json_bytes(
            {key: item for key, item in value.items() if key != "plan_sha256"}))
        self.write("plan.json", value)
        if retained:
            self.write("state/plans/" + value["plan_sha256"] + ".json", value)

    def test_planning_is_nonexecuting_and_retains_bound_input_hashes(self):
        value = self.plan()
        self.assertEqual(value["schema"], scheduler.contracts.PLAN_SCHEMA)
        self.assertEqual(value["policy_sha256"], self.digest("policy.json"))
        self.assertEqual(value["inputs"]["requests"]["sha256"], self.digest("requests.json"))
        self.assertEqual(self.calls("qualify"), 0)
        self.assertFalse((self.root / "state/runs").exists())

    def test_empty_and_unknown_work_emit_idle_not_random_tasks(self):
        self.requests["requests"] = []
        self.write_inputs()
        self.assertEqual(self.plan()["status"], "idle")
        self.assertEqual(self.run_job()["status"], "idle")
        self.requests["requests"] = [{**self.request, "capability_id": "unknown"}]
        self.write_inputs()
        self.assert_blocked()

    def test_event_priority_is_failure_then_model_then_change_then_manual(self):
        self.requests["requests"] = [
            {**self.request, "id": "request-" + kind, "trigger": {"kind": kind, "key": "event"}}
            for kind in ("manual", "repository-change", "model-upgrade", "failure")
        ]
        self.write_inputs()
        jobs = self.plan()["jobs"]
        self.assertEqual([job["trigger"]["kind"] for job in jobs],
                         ["failure", "model-upgrade", "repository-change", "manual"])
        self.assertIn("model not invoked", jobs[1]["reason"])

    def test_duplicate_requests_and_path_duplicates_do_not_duplicate_jobs(self):
        self.requests["requests"] += [{**self.request, "id": "request-two", "paths": ["public.py", "public.py"]}]
        self.write_inputs()
        result = self.plan()
        self.assertEqual(len(result["jobs"]), 1)
        self.assertIn("duplicate idempotency", result["blocked"][0]["reason"])

    def test_unseen_manual_context_precedes_already_evidenced_context(self):
        self.registry["assets"][0]["uses"] = [
            {"context": {"repository": "fixture/source", "workflow": "snapshot"}}
        ]
        self.requests["requests"].append({**self.request, "id": "unseen", "workflow": "new-context"})
        self.write_inputs()
        jobs = self.plan()["jobs"]
        self.assertEqual([job["workflow"] for job in jobs], ["new-context", "snapshot"])
        self.assertEqual([job["priority"] for job in jobs], [3, 4])

    def test_identity_ignores_local_repository_names_request_ids_and_clock(self):
        first = self.plan()["jobs"][0]["id"]
        shutil.copytree(self.source, self.fixture / "relocated")
        self.request.update(id="different-request", source_repo="../relocated")
        self.write_inputs()
        self.assertEqual(self.plan()["jobs"][0]["id"], first)

    def test_model_event_workflow_input_and_policy_changes_have_new_keys(self):
        baseline = self.plan()["jobs"][0]["id"]
        for key, value in (
            ("requested_model", "future-frontier-model"), ("workflow", "new-context"),
            ("trigger", {"kind": "model-upgrade", "key": "upgrade"}),
        ):
            with self.subTest(key=key):
                old = self.request[key]
                self.request[key] = value
                self.write_inputs()
                self.assertNotEqual(self.plan()["jobs"][0]["id"], baseline)
                self.request[key] = old
        self.policy["max_attempts"] = 1
        self.write_inputs()
        self.assertNotEqual(self.plan()["jobs"][0]["id"], baseline)

    def test_policy_denies_unapproved_pins_missing_permissions_and_invalid_bounds(self):
        for key, value in (("allowed_capabilities", []), ("permissions", ["repository.read"])):
            with self.subTest(key=key):
                original = self.policy[key]
                self.policy[key] = value
                self.write_inputs()
                self.assert_blocked()
                self.policy[key] = original
        for key, value in (("max_jobs", 11), ("max_parallel", 0), ("max_attempts", 4),
                           ("timeout_seconds", 301), ("max_jobs", True)):
            with self.subTest(key=key):
                original = self.policy[key]
                self.policy[key] = value
                self.write_inputs()
                with self.assertRaises(ValueError):
                    self.plan()
                self.policy[key] = original

    def test_public_policy_does_not_promote_private_manifest(self):
        self.manifest["visibility"] = "private"
        self.repin()
        self.policy["visibility"] = "public"
        self.write_inputs()
        self.assert_blocked()

    def test_absolute_check_metadata_and_excessive_timeouts_are_refused_before_execution(self):
        self.manifest["checks"][0]["argv"] = [sys.executable, "-c", "print('check')"]
        self.repin()
        self.assert_blocked()
        self.manifest["checks"][0]["argv"] = ["python3", "-c", "print('check')"]
        self.manifest["checks"][0]["timeout_seconds"] = 11
        self.repin()
        self.assert_blocked()

    def test_unknown_executor_is_a_blocked_host_work_order(self):
        (self.root / "scripts/other.py").write_text("raise RuntimeError('never run')\n")
        self.manifest["entrypoint"] = "scripts/other.py"
        self.manifest["artifacts"].append(self.artifact("scripts/other.py"))
        self.repin()
        self.assertIn("host-work-order", self.assert_blocked()["blocked"][0]["reason"])

    def test_dependency_must_exist_and_be_pinned_and_approved(self):
        self.manifest["reuses"] = [{"id": "dependency", "manifest_sha256": "b" * 64}]
        self.repin()
        self.assert_blocked()
        dependency = {**self.manifest, "id": "dependency", "reuses": []}
        self.write("dependency.json", dependency)
        dep_sha = self.digest("dependency.json")
        self.registry["assets"].append({**dependency, "manifest_path": "dependency.json",
                                        "manifest_sha256": dep_sha, "status": "built"})
        self.policy["allowed_capabilities"].append(dep_sha)
        self.write_inputs()
        self.assertIn("dependency pin drift", self.assert_blocked()["blocked"][0]["reason"])
        self.manifest["reuses"][0]["manifest_sha256"] = dep_sha
        self.repin()
        self.assert_blocked()  # repin intentionally removed dependency approval
        self.policy["allowed_capabilities"].append(dep_sha)
        self.write_inputs()
        self.assertEqual(len(self.plan()["jobs"]), 1)

    def test_missing_commit_path_and_symlink_source_are_rejected(self):
        for key, value in (("source_commit", "f" * 40), ("paths", ["missing.py"]),
                           ("paths", ["../outside.py"]), ("source_repo", str(self.source))):
            with self.subTest(key=key):
                old = self.request[key]
                self.request[key] = value
                self.write_inputs()
                self.assert_blocked()
                self.request[key] = old
        (self.fixture / "linked-source").symlink_to(self.source, target_is_directory=True)
        self.request["source_repo"] = "../linked-source"
        self.write_inputs()
        self.assert_blocked()

    def test_staged_only_source_and_git_blob_instead_of_commit_are_rejected(self):
        (self.source / "uncommitted.py").write_text("print('not committed')\n")
        self.git("add", "uncommitted.py")
        self.request["paths"] = ["uncommitted.py"]
        self.write_inputs()
        self.assert_blocked()
        self.request["paths"] = ["public.py"]
        self.request["source_commit"] = self.git("rev-parse", "HEAD:public.py").stdout.strip()
        self.write_inputs()
        self.assert_blocked()

    def test_state_and_outputs_cannot_escape_or_overwrite_inputs(self):
        for state, output in (("../escape", "plan.json"), ("state", "../escape.json"),
                              ("state", "manifest.json"), ("state", "policy.json"),
                              ("state", "state/runs/overwrite.json")):
            with self.subTest(state=state, output=output), self.assertRaises(ValueError):
                scheduler.plan(self.root, "registry.json", "requests.json", "policy.json", state, output)

    def test_raw_manifest_and_code_drift_prevent_execution(self):
        self.plan()
        (self.root / "manifest.json").write_text((self.root / "manifest.json").read_text() + "\n")
        with self.assertRaises(ValueError):
            self.run_job()
        self.repin()
        self.plan()
        (self.root / "helper.txt").write_text("changed helper\n")
        with self.assertRaises(ValueError):
            self.run_job()
        self.assertEqual(self.calls("qualify"), 0)

    def test_registry_request_and_policy_changes_invalidate_plan(self):
        for path in ("registry.json", "requests.json", "policy.json"):
            with self.subTest(path=path):
                self.write_inputs()
                self.plan()
                original = (self.root / path).read_text()
                (self.root / path).write_text(original + "\n")
                with self.assertRaises(ValueError):
                    self.run_job()
                (self.root / path).write_text(original)
        self.assertEqual(self.calls("qualify"), 0)

    def test_plan_mutation_cannot_introduce_argv_even_with_recomputed_receipt(self):
        result = self.plan()
        result["jobs"][0]["argv"] = ["python3", "-c", "raise RuntimeError('injected')"]
        self.rewrite_plan(result, retained=True)
        with self.assertRaises(ValueError):
            self.run_job()
        self.assertEqual(self.calls("qualify"), 0)

    def test_modified_or_unretained_plan_is_refused(self):
        value = self.plan()
        value["jobs"][0]["priority"] = 999
        self.write("plan.json", value)
        with self.assertRaisesRegex(ValueError, "plan contents changed"):
            self.run_job()
        self.rewrite_plan(value)
        with self.assertRaises((ValueError, OSError)):
            self.run_job()

    def test_duplicate_jobs_in_tampered_plan_are_refused(self):
        value = self.plan()
        value["jobs"].append(copy.deepcopy(value["jobs"][0]))
        self.rewrite_plan(value, retained=True)
        with self.assertRaisesRegex(ValueError, "duplicate job"):
            self.run_job()

    def test_real_qualification_and_replay_are_idempotent_and_attest_all_artifacts(self):
        self.plan()
        result = self.run_job()["results"][0]
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["model_execution"], "not_invoked")
        self.assertEqual(self.calls("qualify"), 1)
        self.assertEqual(self.calls("verify"), 1)
        artifacts = result["receipt"]["artifacts"]
        self.assertIn("manifest.json", artifacts)
        self.assertIn("scripts/capability_package.py", artifacts)
        self.assertIn("helper.txt", artifacts)
        self.assertEqual(len(artifacts), 5)
        self.assertEqual(self.run_job()["results"][0]["status"], "no-op")
        self.assertEqual(self.calls("qualify"), 1)
        self.assertEqual(self.calls("verify"), 1)
        self.assertEqual(self.plan()["status"], "idle")
        self.assertNotIn(str(self.fixture), json.dumps(result))

    def test_real_command_failure_retained_and_retries_explicitly_capped(self):
        self.write("behavior.json", {"mode": "exit-fail"})
        self.plan()
        for number in (1, 2):
            result = self.run_job()["results"][0]
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["attempts"], number)
            command = json.loads((self.root / result["attempt_path"] / "command.json").read_text())
            self.assertEqual(command["exit_code"], 4)
            self.assertGreater(command["stderr_bytes"], 0)
        self.assertEqual(self.run_job()["results"][0]["status"], "blocked")
        self.assertEqual(self.calls("qualify"), 2)
        self.assertEqual(self.calls("verify"), 0)
        self.assertIn("attempt limit", self.plan()["blocked"][0]["reason"])

    def test_invalid_reports_never_reach_replay(self):
        for mode in ("failed-gate", "bad-context", "bad-capsule", "bad-replay",
                     "missing-report", "false-check", "private-metadata", "malformed-section",
                     "missing-replay", "missing-replay-permission"):
            with self.subTest(mode=mode):
                self.request["workflow"] = "case-" + mode
                self.write_inputs()
                self.write("behavior.json", {"mode": mode})
                self.plan()
                self.assertEqual(self.run_job()["results"][0]["status"], "failed")
        self.assertEqual(self.calls("verify"), 0)

    def test_dependency_manifests_and_artifacts_are_recorded_with_the_job(self):
        (self.root / "dependency.py").write_text("print('dependency source')\n")
        dependency = copy.deepcopy(self.manifest)
        dependency.update(id="dependency", entrypoint="dependency.py",
                          artifacts=[self.artifact("dependency.py")], reuses=[])
        self.write("dependency.json", dependency)
        dependency_sha = self.digest("dependency.json")
        self.manifest["reuses"] = [{"id": "dependency", "manifest_sha256": dependency_sha}]
        self.repin()
        self.registry["assets"].append({
            **dependency, "manifest_path": "dependency.json", "manifest_sha256": dependency_sha,
            "status": "built", "uses": [], "distinct_repositories": 0, "failures": [],
        })
        self.policy["allowed_capabilities"].append(dependency_sha)
        self.write_inputs()
        self.plan()
        result = self.run_job()["results"][0]
        self.assertEqual(result["status"], "completed", result)
        self.assertTrue({"dependency.json", "dependency.py"} <= set(result["receipt"]["artifacts"]))

    def test_exhausted_job_does_not_starve_later_eligible_work(self):
        self.policy["max_attempts"] = 1
        self.request["trigger"]["kind"] = "failure"
        second = copy.deepcopy(self.request)
        second.update(id="request-two", workflow="second-context")
        second["trigger"] = {"kind": "manual", "key": "second"}
        self.requests["requests"].append(second)
        self.write_inputs()
        self.write("behavior.json", {"mode": "exit-fail"})
        self.plan()
        first = self.run_job()
        self.assertEqual(first["results"][0]["status"], "failed")
        self.write("behavior.json", {})
        second_run = self.run_job()
        by_request = {result["request_id"]: result for result in second_run["results"]}
        self.assertEqual(by_request["request-one"]["status"], "blocked")
        self.assertEqual(by_request["request-two"]["status"], "completed")
        self.assertEqual(self.calls("qualify"), 2)

    def test_declared_check_failure_and_code_mutation_never_complete(self):
        self.manifest["checks"][0]["argv"] = ["python3", "-c", "raise SystemExit(6)"]
        self.repin()
        self.plan()
        self.assertEqual(self.run_job()["results"][0]["status"], "failed")
        self.manifest["checks"][0]["argv"] = ["python3", "-c", "print('real check')"]
        self.repin()
        self.request["workflow"] = "mutating"
        self.write_inputs()
        self.write("behavior.json", {"mode": "mutate-code"})
        self.plan()
        self.assertEqual(self.run_job()["results"][0]["status"], "failed")
        self.assertEqual(self.calls("verify"), 0)

    def test_timeout_is_actual_and_evidence_survives(self):
        self.policy["timeout_seconds"] = 1
        self.write_inputs()
        self.write("behavior.json", {"mode": "timeout"})
        self.plan()
        result = self.run_job()["results"][0]
        self.assertEqual(result["status"], "failed")
        command = json.loads((self.root / result["attempt_path"] / "command.json").read_text())
        self.assertTrue(command["timed_out"])
        self.assertEqual(command["timeout_seconds"], 1)
        self.assertEqual(self.calls("verify"), 0)

    def test_replay_failure_is_not_marked_completed_or_blindly_retried(self):
        self.plan()
        self.write("behavior.json", {"mode": "replay-fail"})
        self.assertEqual(self.run_job()["results"][0]["status"], "recovery-required")
        self.assertEqual(self.run_job()["results"][0]["status"], "recovery-required")
        self.assertEqual(self.calls("qualify"), 1)
        self.assertEqual(self.calls("verify"), 1)

    def test_crash_gap_after_actual_replay_exposes_recovery_without_rerunning(self):
        self.plan()
        original = RecordingSeam.record

        def interrupt(*args, **kwargs):
            original(*args, **kwargs)
            raise OSError("simulated loss before receipt state update")

        with patch.object(RecordingSeam, "record", interrupt):
            self.assertEqual(self.run_job()["results"][0]["status"], "recovery-required")
        self.assertEqual(self.run_job()["results"][0]["status"], "recovery-required")
        self.assertEqual(self.calls("qualify"), 1)
        self.assertEqual(self.calls("verify"), 1)

    def test_orphan_attempt_and_stale_locks_are_not_stolen(self):
        value = self.plan()
        identity = value["jobs"][0]["id"]
        lock = self.root / "state/locks" / (identity + ".lock")
        lock.mkdir(parents=True)
        self.assertEqual(self.run_job()["results"][0]["status"], "recovery-required")
        self.assertTrue(lock.exists())
        self.assertTrue(scheduler.status(self.root / "state")["jobs"][0]["locked"])
        lock.rmdir()  # Explicit fixture operator cleanup; runner never performs this.
        (self.root / "state/runs" / identity / "attempt-1").mkdir(parents=True)
        self.assertEqual(self.run_job()["results"][0]["status"], "recovery-required")
        self.assertEqual(self.calls("qualify"), 0)

    def test_stale_capacity_slot_blocks_execution_and_appears_in_status(self):
        value = self.plan()
        slot = self.root / "state/slots" / value["policy_sha256"] / "0.lock"
        slot.mkdir(parents=True)
        self.assertEqual(self.run_job()["results"][0]["status"], "recovery-required")
        self.assertTrue(slot.exists())
        self.assertEqual(len(scheduler.status(self.root / "state")["occupied_or_stale_slots"]), 1)
        self.assertEqual(self.calls("qualify"), 0)

    def test_max_jobs_bounds_each_run_without_starving_remaining_jobs(self):
        self.requests["requests"] = [{**self.request, "id": "request-" + str(i), "workflow": "context-" + str(i)}
                                     for i in range(3)]
        self.write_inputs()
        self.plan()
        self.assertEqual(self.run_job()["deferred"], 2)
        self.assertEqual(self.calls("qualify"), 1)
        self.assertEqual(self.run_job()["deferred"], 1)
        self.assertEqual(self.calls("qualify"), 2)
        with self.assertRaises(ValueError):
            self.run_job(jobs=2)
        with self.assertRaises(ValueError):
            self.run_job(jobs=0)

    def test_parallel_execution_obeys_bound(self):
        self.policy.update(max_jobs=3, max_parallel=2)
        self.requests["requests"] = [{**self.request, "id": "request-" + str(i), "workflow": "context-" + str(i)}
                                     for i in range(3)]
        self.write_inputs()
        self.write("behavior.json", {"mode": "slow"})
        self.plan()
        original = scheduler.frames.run_check
        mutex = threading.Lock()
        active, maximum = 0, 0

        def observed(*args, **kwargs):
            nonlocal active, maximum
            with mutex:
                active += 1
                maximum = max(maximum, active)
            try:
                return original(*args, **kwargs)
            finally:
                with mutex:
                    active -= 1

        with patch.object(scheduler.frames, "run_check", observed):
            result = self.run_job()
        self.assertTrue(all(item["status"] == "completed" for item in result["results"]))
        self.assertEqual(maximum, 2)
        self.assertEqual(self.calls("qualify"), 3)

    def test_concurrent_processes_cannot_execute_the_same_job_twice(self):
        self.plan()
        self.write("behavior.json", {"mode": "slow"})
        code = (
            "import sys; sys.path.insert(0, 'tests'); "
            "from test_capability_scheduler import scheduler, RecordingSeam; "
            "scheduler.RappRecorder = RecordingSeam; "
            "value = scheduler.run_plan(sys.argv[1], 'plan.json', 'policy.json', 'state', "
            "'rapp-store', 'unused-test-reference'); "
            "import json; print(json.dumps(value))"
        )
        processes = [subprocess.Popen([sys.executable, "-B", "-c", code, str(self.root)],
                                      cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                     for _ in range(2)]
        try:
            results = []
            for process in processes:
                stdout, stderr = process.communicate(timeout=20)
                self.assertEqual(process.returncode, 0, stderr)
                results.append(json.loads(stdout)["results"][0]["status"])
            self.assertEqual(results.count("completed"), 1)
            self.assertTrue(set(results) <= {"completed", "no-op", "recovery-required"})
            self.assertEqual(self.calls("qualify"), 1)
            self.assertEqual(self.calls("verify"), 1)
        finally:
            for process in processes:
                if process.poll() is None:
                    process.kill()
                    process.communicate(timeout=5)

    def test_real_recorder_requires_preinitialized_store_and_reference(self):
        self.plan()
        with self.assertRaises((ValueError, OSError)):
            scheduler.run_plan(self.root, "plan.json", "policy.json", "state",
                               "not-initialized", "missing-reference")
        self.assertFalse((self.root / "not-initialized").exists())
        self.assertEqual(self.calls("qualify"), 0)

    def test_status_is_read_only_and_cli_runs_no_service(self):
        state = self.root / "not-created"
        self.assertEqual(scheduler.status(state)["status"], "idle")
        self.assertFalse(state.exists())
        command = [sys.executable, "-B", str(ROOT / "scripts/capability_scheduler.py"),
                   "plan", "--root", str(self.root), "--registry", "registry.json",
                   "--requests", "requests.json", "--policy", "policy.json",
                   "--state", "state", "--output", "plan.json"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "ready")
        self.assertEqual(self.calls("qualify"), 0)


if __name__ == "__main__":
    unittest.main()
