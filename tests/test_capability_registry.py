"""Registry tests use real pinned RAPP frames, Git objects and replay processes.

RAPP_REFERENCE_DIR is mandatory. Fixture files stay beneath this checkout; no
system temporary directory, network, fabricated passing frame, or skipped
reference coverage is used.
"""

import argparse
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
import uuid
import warnings


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import autocomplete_frames as frames
import capability_contracts as contracts
import capability_registry as registry


ENTRYPOINT = "scripts/mini_capsule.py"
HELPER = "scripts/mini_support.py"
MANIFEST = "manifests/source-capsule.json"
CAPSULE = "capsules/source.json"
REPORT = "reports/qualification.json"
CAPSULE_FILES = (ENTRYPOINT, HELPER, "sample.txt")
MINI_SOURCE = '''\
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import uuid
from mini_support import MARKER

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(["git", *args])

parser = argparse.ArgumentParser()
parser.add_argument("command", choices=["check", "verify"])
parser.add_argument("--manifest")
parser.add_argument("--capsule")
parser.add_argument("--report")
parser.add_argument("--root")
parser.add_argument("--repo")
parser.add_argument("--replay", action="store_true")
parser.add_argument("--allow-checks", action="store_true")
args = parser.parse_args()
if args.command == "check":
    data = Path("sample.txt").read_bytes()
    assert data.decode().startswith(MARKER), "fixture source does not satisfy the declared job"
    print(sha(data))
else:
    assert args.replay and args.allow_checks
    manifest_raw = Path(args.manifest).read_bytes()
    manifest = json.loads(manifest_raw)
    capsule_raw = Path(args.capsule).read_bytes()
    capsule = json.loads(capsule_raw)
    report = json.loads(Path(args.report).read_bytes())
    assert report["capability"] == {"id": manifest["id"], "manifest_sha256": sha(manifest_raw)}
    assert report["capsule"] == {"sha256": sha(capsule_raw), "bytes": len(capsule_raw)}
    assert report["outcome"] == "passed"
    assert all(report["gates"][name] is True for name in ["source_matches", "round_trip", "artifacts_stable"])
    assert capsule["schema"] == "localfirst-source-capsule/v1"
    assert capsule["origin"]["commit"] == git("rev-parse", "HEAD").decode().strip()
    assert capsule["origin"]["tree"] == git("rev-parse", "HEAD^{tree}").decode().strip()
    remote = git("config", "--get", "remote.origin.url").decode().strip()
    assert remote.startswith("https://github.com/") and remote.endswith(".git")
    assert capsule["origin"]["repository"].casefold() == remote[19:-4].casefold()
    for name in ("repository", "commit", "tree"):
        assert report["context"][name] == capsule["origin"][name]
    assert len(report["checks"]) == len(manifest["checks"])
    for check, expected in zip(report["checks"], manifest["checks"]):
        assert check["argv"] == expected["argv"] and check["timeout_seconds"] == expected["timeout_seconds"]
        assert check["exit_code"] == 0 and check["timed_out"] is False
        assert check["capture_complete"] is True and check["launch_error"] is None
    for artifact in manifest["artifacts"]:
        data = Path(artifact["path"]).read_bytes()
        assert sha(data) == artifact["sha256"] and len(data) == artifact["bytes"]
    total = 0
    seen = set()
    restored = Path(".mini-replay-" + uuid.uuid4().hex)
    restored.mkdir()
    try:
        for file in capsule["files"]:
            path = Path(file["path"])
            assert not path.is_absolute() and ".." not in path.parts and str(path) not in seen
            seen.add(str(path))
            data = file["text"].encode("utf-8")
            assert len(data) == file["bytes"] and sha(data) == file["sha256"]
            assert Path(path).read_bytes() == data and git("show", "HEAD:" + str(path)) == data
            mode = git("ls-tree", "HEAD", "--", str(path)).decode().split()[0]
            assert mode == file["mode"] and mode in ("100644", "100755")
            target = restored / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            total += len(data)
        assert capsule["totals"] == {"files": len(seen), "bytes": total}
        for check in manifest["checks"]:
            completed = subprocess.run(check["argv"], cwd=restored, timeout=check["timeout_seconds"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert completed.returncode == 0, "fresh restored source failed its real check"
        for file in capsule["files"]:
            assert sha((restored / file["path"]).read_bytes()) == file["sha256"]
    finally:
        shutil.rmtree(restored)
    print(sha(capsule_raw))
'''


class CapabilityRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = os.environ.get("RAPP_REFERENCE_DIR")
        if not source:
            raise RuntimeError("RAPP_REFERENCE_DIR is required; qualification coverage cannot be skipped")
        cls.reference_dir = Path(source).absolute()
        cls.reference = frames.Reference(cls.reference_dir)

    def setUp(self):
        self.fixture = ROOT / (".capability-registry-test-" + uuid.uuid4().hex)
        self.fixture.mkdir()
        self.addCleanup(shutil.rmtree, self.fixture)
        self.root = self.fixture / "project"
        (self.root / "scripts").mkdir(parents=True)
        (self.root / ENTRYPOINT).write_text(MINI_SOURCE, encoding="utf-8")
        (self.root / HELPER).write_text("MARKER = 'source:'\n", encoding="utf-8")
        (self.root / "sample.txt").write_text("source: alpha\n", encoding="utf-8")
        self.manifest = self.make_manifest()
        self.write_json(self.root / MANIFEST, self.manifest)
        self.init_git(self.root, "fixture-owner/alpha")
        self.store = self.root / "evidence"
        self.sequence = 0

    def write_json(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contracts.json_bytes(value))

    def git(self, repo, *args):
        environment = {key: value for key, value in os.environ.items()
                       if key not in {"GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"}}
        environment.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
        return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                              text=True, timeout=10, env=environment).stdout.strip()

    def init_git(self, repo, name):
        self.git(repo, "init", "--quiet")
        self.git(repo, "remote", "add", "origin", "https://github.com/" + name + ".git")
        self.git(repo, "add", *CAPSULE_FILES, MANIFEST)
        self.commit(repo)

    def commit(self, repo):
        self.git(repo, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "fixture source")

    def make_manifest(self, identifier="source-capsule", reuses=None):
        return {
            "schema": contracts.CAPABILITY_SCHEMA, "id": identifier, "version": "1.0.0",
            "title": "Source capsule", "job": "Package source and independently replay its declared job",
            "entrypoint": ENTRYPOINT,
            "artifacts": [{"path": path, "sha256": frames.digest((self.root / path).read_bytes()),
                           "bytes": len((self.root / path).read_bytes())} for path in (ENTRYPOINT, HELPER)],
            "contract": {
                "inputs": {"type": "object", "properties": {"source": {"type": "string"}}},
                "outputs": {"type": "object", "properties": {"capsule": {"type": "object"}}},
                "permissions": ["repository.read", "artifact.write", "process.execute"], "network": "none",
            },
            "checks": [{"id": "sample-content", "argv": ["python3", ENTRYPOINT, "check"], "timeout_seconds": 5}],
            "failure_cases": ["Reject modified source or a capsule that cannot replay its check"],
            "reuses": reuses or [], "visibility": "public",
        }

    def build(self, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            return registry.build_registry(self.root, manifests="manifests",
                                           rapp_dir=self.reference_dir, **kwargs)

    def cli(self, arguments, expected=0):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err), warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            code = registry.main(arguments)
        self.assertEqual(code, expected, out.getvalue() + err.getvalue())
        return json.loads(out.getvalue()) if code == 0 else err.getvalue()

    def context(self, repo):
        remote = self.git(repo, "config", "--get", "remote.origin.url")
        return {"repository": remote[19:-4], "commit": self.git(repo, "rev-parse", "HEAD"),
                "tree": self.git(repo, "rev-parse", "HEAD^{tree}"), "workflow": "fresh-source-replay"}

    def prepare_report(self, repo=None):
        repo = repo or self.root
        context = self.context(repo)
        manifest = contracts.load_json(repo / MANIFEST)
        files = []
        for name in CAPSULE_FILES:
            data = (repo / name).read_bytes()
            files.append({"path": name, "mode": self.git(repo, "ls-tree", "HEAD", "--", name).split()[0],
                          "sha256": frames.digest(data), "bytes": len(data), "text": data.decode("utf-8")})
        capsule = {"schema": contracts.CAPSULE_SCHEMA,
                   "origin": {key: context[key] for key in ("repository", "commit", "tree")},
                   "files": files, "totals": {"files": len(files), "bytes": sum(file["bytes"] for file in files)}}
        self.write_json(repo / CAPSULE, capsule)
        checks = [frames.run_check(check["argv"], repo, check["timeout_seconds"]) for check in manifest["checks"]]
        source_matches = all(self.git(repo, "show", "HEAD:" + file["path"]) == file["text"].strip()
                             for file in files)
        restored = repo / (".qualification-restore-" + uuid.uuid4().hex)
        restored.mkdir()
        try:
            for file in files:
                target = restored / file["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(file["text"], encoding="utf-8")
            replay = [frames.run_check(check["argv"], restored, check["timeout_seconds"])
                      for check in manifest["checks"]]
            stable = all(frames.digest((restored / file["path"]).read_bytes()) == file["sha256"] for file in files)
            round_trip = all(frames.check_passed(check) for check in replay) and stable
        finally:
            shutil.rmtree(restored)
        raw = (repo / CAPSULE).read_bytes()
        argv = contracts.source_replay_argv(ENTRYPOINT, MANIFEST, ".", CAPSULE, REPORT)
        report = {
            "schema": contracts.QUALIFICATION_SCHEMA,
            "capability": {"id": manifest["id"], "manifest_sha256": frames.digest((repo / MANIFEST).read_bytes())},
            "context": context, "capsule": {"sha256": frames.digest(raw), "bytes": len(raw)},
            "outcome": "passed" if source_matches and round_trip and all(frames.check_passed(check) for check in checks)
                       else "failed",
            "gates": {"source_matches": source_matches, "round_trip": round_trip, "artifacts_stable": stable},
            "checks": checks, "replay_argv": argv, "limitations": ["Fixture evidence is unsigned and local."],
        }
        self.write_json(repo / REPORT, report)
        return report

    def record_report(self, repo=None, phase="implementation", omit=(), command=None, expected=0, prepare=True):
        repo = repo or self.root
        report = self.prepare_report(repo) if prepare else contracts.load_json(repo / REPORT)
        if not self.store.exists():
            frames.init_store(self.store, "fixture-owner", "qualification", self.reference)
        self.sequence += 1
        artifacts = [MANIFEST, ENTRYPOINT, HELPER, CAPSULE, REPORT]
        args = argparse.Namespace(
            store=str(self.store), repo=str(repo), run_id="qualification", worker="worker-" + str(self.sequence),
            phase=phase, summary="Check actual source capsule replay", parent=[], check_timeout=10,
            artifact=[path for path in artifacts if path not in omit],
            check=[json.dumps(command if command is not None else report["replay_argv"])],
        )
        result, code = frames.record(args, self.reference)
        self.assertEqual(code, expected, result)
        return result

    def test_help_only_replay_cannot_promote_even_when_its_process_exits_zero(self):
        report = self.prepare_report()
        report["replay_argv"].append("--help")
        self.write_json(self.root / REPORT, report)
        self.record_report(prepare=False)
        asset = self.build(store="evidence")["assets"][0]
        self.assertEqual(asset["status"], "built")
        self.assertIn("not_capability_replay", {failure["reason"] for failure in asset["failures"]})

    def clone_context(self, name, repository="fixture-owner/beta", change_source=False):
        repo = self.fixture / name
        shutil.copytree(self.root, repo, ignore=shutil.ignore_patterns("evidence", "reports", "capsules"))
        self.git(repo, "remote", "set-url", "origin", "https://github.com/" + repository + ".git")
        if change_source:
            (repo / "sample.txt").write_text("source: " + name + "\n", encoding="utf-8")
            self.git(repo, "add", "sample.txt")
            self.commit(repo)
        return repo

    def test_built_descriptor_is_real_code_not_check_execution(self):
        self.manifest["checks"][0]["argv"] = [
            "python3", "-c", "from pathlib import Path; Path('should-not-run.txt').write_text('executed')",
        ]
        self.write_json(self.root / MANIFEST, self.manifest)
        value = self.build()
        asset = value["assets"][0]
        self.assertEqual(asset["status"], "built")
        self.assertEqual(asset["contract"]["permissions"], self.manifest["contract"]["permissions"])
        self.assertEqual(asset["manifest_sha256"], frames.digest((self.root / MANIFEST).read_bytes()))
        self.assertEqual(value["evidence"]["state"], "not_configured")
        self.assertEqual(value["summary"], {"assets": 1, "built": 1, "proven": 0, "reused": 0})
        self.assertFalse((self.root / "should-not-run.txt").exists())
        explicit = registry.build_registry(self.root, manifest_paths=[MANIFEST])
        self.assertEqual(explicit["assets"], value["assets"])

    def test_artifact_exact_byte_drift_fails_whole_registry(self):
        (self.root / HELPER).write_text("MARKER = 'changed:'\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "artifact changed"):
            self.build()

    def test_manifest_cannot_self_assess_graduation(self):
        self.manifest["status"] = "reused"
        self.write_json(self.root / MANIFEST, self.manifest)
        with self.assertRaisesRegex(ValueError, "invalid capability manifest fields"):
            self.build()

    def test_duplicate_ids_missing_dependencies_and_cycles_fail(self):
        self.write_json(self.root / "manifests/duplicate.json", self.manifest)
        with self.assertRaisesRegex(ValueError, "duplicate capability"):
            self.build()
        (self.root / "manifests/duplicate.json").unlink()
        self.manifest["reuses"] = [{"id": "missing", "manifest_sha256": "0" * 64}]
        self.write_json(self.root / MANIFEST, self.manifest)
        with self.assertRaisesRegex(ValueError, "missing capability dependency"):
            self.build()
        helper = self.make_manifest("helper", [{"id": "source-capsule", "manifest_sha256": "0" * 64}])
        self.manifest["reuses"] = [{"id": "helper", "manifest_sha256": "0" * 64}]
        self.write_json(self.root / MANIFEST, self.manifest)
        self.write_json(self.root / "manifests/helper.json", helper)
        with self.assertRaisesRegex(ValueError, "cyclic capability"):
            self.build()

    def test_dependency_version_or_hash_drift_is_not_discarded(self):
        helper = self.make_manifest("helper")
        path = self.root / "manifests/helper.json"
        self.write_json(path, helper)
        self.manifest["reuses"] = [{"id": "helper", "manifest_sha256": frames.digest(path.read_bytes())}]
        self.write_json(self.root / MANIFEST, self.manifest)
        self.assertEqual(self.build()["summary"]["assets"], 2)
        helper["version"] = "2.0.0"
        self.write_json(path, helper)
        with self.assertRaisesRegex(ValueError, "dependency manifest hash/version drift"):
            self.build()

    def test_missing_store_is_explicit_built_existing_empty_store_fails(self):
        self.assertEqual(self.build(store="absent-store")["evidence"]["state"], "missing_store")
        frames.init_store(self.store, "fixture-owner", "qualification", self.reference)
        with self.assertRaisesRegex(ValueError, "zero frames"):
            self.build(store="evidence")
        with self.assertRaisesRegex(ValueError, "rapp-dir"):
            registry.build_registry(self.root, manifests="manifests", store="evidence")

    def test_a_real_replayed_bound_report_is_proven(self):
        receipt = self.record_report()
        self.assertEqual(receipt["outcome"], "checks_passed")
        value = self.build(store="evidence")
        asset = value["assets"][0]
        self.assertEqual(asset["status"], "proven", asset["failures"])
        self.assertEqual(asset["distinct_repositories"], 1)
        self.assertEqual(asset["uses"][0]["frame_hash"], receipt["frame_hash"])
        self.assertEqual(asset["uses"][0]["commit"], self.git(self.root, "rev-parse", "HEAD"))
        self.assertEqual(value["evidence"]["state"], "verified")
        self.assertEqual(value["evidence"]["frames"], 1)

    def test_duplicate_proof_in_another_stream_is_one_use(self):
        self.record_report()
        self.record_report(prepare=False)
        asset = self.build(store="evidence")["assets"][0]
        self.assertEqual(asset["status"], "proven")
        self.assertEqual(len(asset["uses"]), 1)
        self.assertEqual(asset["distinct_repositories"], 1)

    def test_same_repository_aliases_or_new_commits_are_not_reuse(self):
        self.record_report()
        clone = self.clone_context("copy", "FIXTURE-OWNER/Alpha", change_source=True)
        self.record_report(clone)
        asset = self.build(store="evidence")["assets"][0]
        self.assertEqual(asset["status"], "proven")
        self.assertEqual(asset["distinct_repositories"], 1)
        self.assertEqual(len(asset["uses"]), 2)

    def test_two_repo_names_with_identical_commit_and_tree_are_not_reused(self):
        self.record_report()
        clone = self.clone_context("other-path")
        self.assertEqual(self.context(clone)["commit"], self.context(self.root)["commit"])
        self.record_report(clone)
        asset = self.build(store="evidence")["assets"][0]
        self.assertEqual(asset["distinct_repositories"], 2)
        self.assertEqual(asset["status"], "proven")

    def test_two_distinct_real_source_contexts_are_reused(self):
        self.record_report()
        other = self.clone_context("different-source", change_source=True)
        self.assertNotEqual(self.context(other)["commit"], self.context(self.root)["commit"])
        self.assertNotEqual(self.context(other)["tree"], self.context(self.root)["tree"])
        self.record_report(other)
        value = self.build(store="evidence")
        self.assertEqual(value["assets"][0]["status"], "reused", value["assets"][0]["failures"])
        self.assertEqual(value["summary"]["reused"], 1)
        self.assertEqual(value["assets"][0]["distinct_repositories"], 2)
        self.assertNotIn(str(self.fixture), json.dumps(value))
        self.assertNotIn("model", value["assets"][0])

    def test_failed_qualification_is_a_failure_signal_not_promotion(self):
        (self.root / "sample.txt").write_text("does not satisfy the declared job\n", encoding="utf-8")
        self.git(self.root, "add", "sample.txt")
        self.commit(self.root)
        receipt = self.record_report(expected=1)
        self.assertEqual(receipt["outcome"], "checks_failed")
        asset = self.build(store="evidence")["assets"][0]
        self.assertEqual(asset["status"], "built")
        self.assertEqual(asset["failures"][0]["reason"], "qualification_failed")

    def test_plan_or_older_manifest_does_not_graduate_current_code(self):
        self.record_report(phase="plan")
        asset = self.build(store="evidence")["assets"][0]
        self.assertEqual(asset["status"], "built")
        self.assertEqual(asset["failures"][0]["reason"], "non_implementation_frame")
        self.record_report(prepare=False)
        self.assertEqual(self.build(store="evidence")["assets"][0]["status"], "proven")
        self.manifest["version"] = "2.0.0"
        self.write_json(self.root / MANIFEST, self.manifest)
        asset = self.build(store="evidence")["assets"][0]
        self.assertEqual(asset["status"], "built")
        self.assertTrue(all(failure["reason"] == "manifest_revision_mismatch" for failure in asset["failures"]))

    def test_unbound_mutable_report_and_index_claims_are_ignored(self):
        self.record_report(omit=(REPORT, CAPSULE), command=["python3", ENTRYPOINT, "check"])
        fake = {"schema": frames.EVIDENCE_SCHEMA, "claims": {"qualification": "reused"},
                "events": [{"phase": "implementation", "outcome": "checks_passed",
                            "report": contracts.load_json(self.root / REPORT)}]}
        self.write_json(self.store / "index.json", fake)
        asset = self.build(store="evidence")["assets"][0]
        self.assertEqual(asset["status"], "built")
        self.assertFalse(asset["uses"])
        self.assertFalse(asset["failures"])

    def test_arbitrary_success_command_cannot_qualify_a_fabricated_report(self):
        report = self.prepare_report()
        report["replay_argv"] = ["true"]
        self.write_json(self.root / REPORT, report)
        self.record_report(prepare=False)
        asset = self.build(store="evidence")["assets"][0]
        self.assertEqual(asset["status"], "built")
        self.assertEqual(asset["failures"][0]["reason"], "not_capability_replay")

    def test_report_replay_must_be_the_actual_recorded_command(self):
        self.record_report(command=["python3", ENTRYPOINT, "check"])
        asset = self.build(store="evidence")["assets"][0]
        self.assertEqual(asset["status"], "built")
        self.assertEqual(asset["failures"][0]["reason"], "replay_command_not_recorded")

    def test_helper_manifest_and_capsule_bytes_must_be_attested_in_same_frame(self):
        for omitted, reason in ((HELPER, "implementation_artifact_not_attested"),
                                (MANIFEST, "manifest_not_attested"), (CAPSULE, "capsule_not_attested")):
            with self.subTest(omitted=omitted):
                self.record_report(omit=(omitted,))
                asset = self.build(store="evidence")["assets"][0]
                self.assertEqual(asset["status"], "built")
                self.assertIn(reason, {failure["reason"] for failure in asset["failures"]})

    def test_capsule_fingerprints_origin_and_totals_have_refusal_witnesses(self):
        self.prepare_report()
        capsule = contracts.load_json(self.root / CAPSULE)
        context = self.context(self.root)
        registry.capsule_envelope(capsule, context)
        for target, key, value, reason in (
            ("origin", "tree", "0" * 40, "capsule_context_mismatch"),
            ("files", "sha256", "0" * 64, "capsule_file_fingerprint_mismatch"),
            ("totals", "bytes", 0, "capsule_totals_mismatch"),
        ):
            changed = json.loads(json.dumps(capsule))
            (changed[target][0] if target == "files" else changed[target])[key] = value
            with self.subTest(mutated=target), self.assertRaisesRegex(registry.Unqualified, reason):
                registry.capsule_envelope(changed, context)
        registry.capsule_envelope(capsule, context)

    def test_tampered_store_fails_instead_of_degrading_to_built(self):
        receipt = self.record_report()
        path = self.store / receipt["path"]
        frame = frames.read_json(path)
        frame["payload"]["summary"] = "changed after hashing"
        self.write_json(path, frame)
        with self.assertRaisesRegex(ValueError, "canonical frame rejection"):
            self.build(store="evidence")

    def test_registry_verify_rejects_tampering_but_ignores_only_generated_at(self):
        self.record_report()
        output = "registry.json"
        value = self.build(store="evidence")
        registry.write_registry(self.root, output, value, manifests="manifests", store="evidence")
        value["generated_at"] = "2020-01-01T00:00:00.000Z"
        self.write_json(self.root / output, value)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            verified = registry.verify_registry(self.root, output, manifests="manifests",
                                                store="evidence", rapp_dir=self.reference_dir)
        self.assertTrue(verified["verified"])
        value["assets"][0]["job"] = "Tampered discovery job"
        self.write_json(self.root / output, value)
        with warnings.catch_warnings(), self.assertRaisesRegex(ValueError, "stale or tampered"):
            warnings.simplefilter("ignore", ResourceWarning)
            registry.verify_registry(self.root, output, manifests="manifests",
                                     store="evidence", rapp_dir=self.reference_dir)

    def test_projection_rejects_invalid_utc_or_extra_promotion_fields(self):
        original = self.build()
        changed = json.loads(json.dumps(original))
        changed["generated_at"] = "2026-02-30T00:00:00.000Z"
        with self.assertRaisesRegex(ValueError, "invalid registry UTC"):
            registry.validate_projection(changed)
        changed = json.loads(json.dumps(original))
        changed["assets"][0]["promotion"] = "core"
        with self.assertRaisesRegex(ValueError, "invalid registry asset fields"):
            registry.validate_projection(changed)
        registry.validate_projection(original)

    def test_cli_build_verify_and_search_are_stable_and_job_oriented(self):
        common = ["--root", str(self.root), "--manifests", "manifests"]
        value = self.cli(["build", *common, "--output", "registry.json"])
        self.assertEqual(value["summary"]["built"], 1)
        self.assertTrue(self.cli(["verify", *common, "--registry", "registry.json"])["verified"])
        arguments = ["search", "--registry", str(self.root / "registry.json"),
                     "--query", "source capsule", "--limit", "10"]
        first = self.cli(arguments)
        self.assertEqual(first, self.cli(arguments))
        self.assertTrue(first["projection_only"])
        match = first["matches"][0]
        self.assertEqual(match["job"], self.manifest["job"])
        self.assertEqual(match["contract"]["inputs"], self.manifest["contract"]["inputs"])
        self.assertEqual(match["contract"]["outputs"], self.manifest["contract"]["outputs"])
        self.assertIn("permissions", match["contract"])
        self.assertIn("failure_cases", match)
        self.assertIn("uses", match)
        self.assertGreater(match["discovery_score"], 0)

    def test_paths_and_output_cannot_escape_or_overwrite_pinned_inputs(self):
        with self.assertRaises(ValueError):
            registry.build_registry(self.root, manifest_paths=["../project/" + MANIFEST])
        alias = self.root / "manifests/alias.json"
        alias.symlink_to(self.root / MANIFEST)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            self.build()
        alias.unlink()
        value = self.build()
        with self.assertRaises(ValueError):
            registry.write_registry(self.root, MANIFEST, value, manifests="manifests")
        with self.assertRaises(ValueError):
            registry.write_registry(self.root, "../escaped.json", value)
        with self.assertRaises(ValueError):
            registry.write_registry(self.root, "evidence/index.json", value, store="evidence")

    def test_missing_reference_is_a_hard_test_failure(self):
        result = subprocess.run(
            [sys.executable, "-B", str(Path(__file__)),
             "CapabilityRegistryTests.test_a_real_replayed_bound_report_is_proven"],
            env={key: value for key, value in os.environ.items() if key != "RAPP_REFERENCE_DIR"},
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("RAPP_REFERENCE_DIR is required", result.stderr)
        self.assertNotIn("OK (skipped", result.stderr)


if __name__ == "__main__":
    unittest.main()
