"""Synthetic committed source transport and qualification refusal witnesses."""

from argparse import Namespace
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import unittest
from unittest.mock import patch
import uuid

from scripts import capability_contracts as contracts
from scripts import capability_package as package


class CapabilityPackageTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = Path("tests/.capability-package-fixtures")
        self.case = self.fixtures / uuid.uuid4().hex
        self.source = self.case / "source"
        self.root = self.case / "capability"
        self.source.mkdir(parents=True)
        self.root.mkdir()
        self.addCleanup(self.cleanup)
        self.git("init", "--quiet")
        self.write_source("sample.txt", b"Committed caf\xc3\xa9\r\nsecond line\n")
        self.write_source("nested/run.py", b"print('portable source')\r\n", 0o755)
        self.commit = self.snapshot()
        for name, source in package.IMPLEMENTATION.items():
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
        (self.root / "check.py").write_text("print('real trusted check')\n", encoding="utf-8")
        self.manifest = self.pin_manifest()
        self.args = Namespace(
            root=str(self.root), manifest="capability.json", repo="../source",
            ref=self.commit, repository="example/public-source", path=["sample.txt", "nested/run.py"],
            workflow="source-reuse", capsule="results/capsule.json", report="results/qualification.json",
            allow_checks=True, replay=True,
        )

    def cleanup(self):
        shutil.rmtree(self.case)
        try:
            self.fixtures.rmdir()
        except OSError:
            pass

    def git(self, *args, input=None):
        environment = package.git_source._git_environment()
        environment.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                            "GIT_AUTHOR_DATE": "2026-09-05T12:00:00Z",
                            "GIT_COMMITTER_DATE": "2026-09-05T12:00:00Z"})
        return subprocess.run(
            ["git", "-C", str(self.source), "-c", "user.name=Capsule Tests",
             "-c", "user.email=capsule@example.invalid", "-c", "commit.gpgsign=false",
             "-c", "core.hooksPath=.git/no-hooks", "-c", "init.defaultBranch=main", *args],
            input=input, env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
        ).stdout.decode("utf-8").strip()

    def write_source(self, name, data, mode=0o644):
        target = self.source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(mode)

    def snapshot(self):
        self.git("add", "--all")
        self.git("commit", "--quiet", "--allow-empty", "-m", "synthetic source")
        return self.git("rev-parse", "HEAD")

    def pin_manifest(self, argv=None, permissions=None, timeout=3):
        artifacts = []
        for name in sorted([*package.IMPLEMENTATION, "check.py"]):
            body = (self.root / name).read_bytes()
            artifacts.append({"path": name, "sha256": package.frames.digest(body), "bytes": len(body)})
        value = {
            "schema": contracts.CAPABILITY_SCHEMA, "id": "source-capsule", "version": "1.0.0",
            "title": "Committed source transport", "job": "Restore exact declared UTF-8 source bytes.",
            "entrypoint": package.ENTRYPOINT, "artifacts": artifacts,
            "contract": {"inputs": {"type": "object"}, "outputs": {"type": "object"},
                         "permissions": permissions if permissions is not None else
                         ["repository.read", "artifact.write", "process.execute"], "network": "none"},
            "checks": [{"id": "real-check", "argv": argv or ["python3", "check.py"],
                        "timeout_seconds": timeout}],
            "failure_cases": ["Modified source hash", "Existing destination", "Failing declared check"],
            "reuses": [], "visibility": "public",
        }
        (self.root / "capability.json").write_bytes(contracts.json_bytes(value))
        self.manifest = value
        return value

    def pack(self, paths=None):
        return package.pack_sources(self.source, self.commit, "example/public-source",
                                    paths if paths is not None else ["sample.txt", "nested/run.py"])

    def assert_refused(self, data):
        destination = self.case / "refused"
        with self.assertRaises(ValueError):
            package.restore_capsule(data, destination)
        self.assertFalse(destination.exists(), "Whole-capsule validation must precede writes.")

    def qualified(self):
        report = package.qualify(self.args)
        self.assertEqual(report["outcome"], "passed")
        return report

    def write_report(self, report, reseal=False):
        if reseal:
            report["integrity_sha256"] = package._integrity(report)
        (self.root / self.args.report).write_bytes(contracts.json_bytes(report))

    def test_pack_is_deterministic_committed_only_and_public(self):
        before = self.pack()
        self.write_source("sample.txt", b"staged bytes\n")
        self.git("add", "sample.txt")
        self.write_source("sample.txt", b"dirty bytes\n")
        self.write_source("untracked.txt", b"not committed")
        after = self.pack(["nested/run.py", "sample.txt"])
        self.assertEqual(contracts.json_bytes(before), contracts.json_bytes(after))
        self.assertEqual(before["origin"]["commit"], self.commit)
        self.assertEqual(before["origin"]["tree"], self.git("rev-parse", "HEAD^{tree}"))
        self.assertEqual(before["totals"]["files"], 2)
        self.assertNotIn(str(self.case.resolve()), contracts.json_bytes(before).decode())
        self.assertNotIn("generated_at", before)

    def test_restore_preserves_bytes_line_endings_and_modes(self):
        data = self.pack()
        destination = package.restore_capsule(data, self.case / "restored")
        for item in data["files"]:
            path = destination / item["path"]
            self.assertEqual(path.read_bytes(), item["text"].encode("utf-8"))
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), int(item["mode"][-3:], 8))

    def test_restore_collision_does_not_overlay_or_delete_user_data(self):
        destination = self.case / "existing"
        destination.mkdir()
        marker = destination / "keep.txt"
        marker.write_text("user data", encoding="utf-8")
        with self.assertRaises(ValueError):
            package.restore_capsule(self.pack(), destination)
        self.assertEqual(marker.read_text(encoding="utf-8"), "user data")
        empty = self.case / "already-empty"
        empty.mkdir()
        with self.assertRaises(ValueError):
            package.restore_capsule(self.pack(), empty)
        self.assertTrue(empty.is_dir())

    def test_capsule_tampering_and_invalid_totals_are_refused_before_writes(self):
        original = self.pack()
        mutations = [
            lambda data: data["files"][0].update(text="tampered"),
            lambda data: data["files"][0].update(sha256="0" * 64),
            lambda data: data["files"][0].update(bytes=True),
            lambda data: data["files"][0].update(mode="120000"),
            lambda data: data["files"][0].update(mode=[]),
            lambda data: data["totals"].update(files=3),
            lambda data: data["origin"].update(commit="HEAD"),
            lambda data: data["origin"].update(repository=[]),
            lambda data: data.update(extra="not in exact profile"),
            lambda data: data["files"].reverse(),
            lambda data: data.update(files=[]),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                data = deepcopy(original)
                mutation(data)
                self.assert_refused(data)

    def test_traversal_private_binary_and_colliding_paths_are_refused(self):
        original = self.pack()
        for name in ("../escape.py", "/escape.py", "a/../escape.py", ".git/config",
                     ".env.json", "credentials.json", "private-token.txt", "a\\b.py"):
            with self.subTest(path=name):
                data = deepcopy(original)
                data["files"][0]["path"] = name
                self.assert_refused(data)
                with self.assertRaises(ValueError):
                    self.pack([name])
        fake_assignment = "".join(("pass", "word", "=", "fixture-only-not-a-credential"))
        for text in ("contains\x00binary", fake_assignment, "\ud800"):
            with self.subTest(text=repr(text)):
                data = deepcopy(original)
                data["files"][0]["text"] = text
                self.assert_refused(data)
        for names in (["a.py", "a.py/child.txt"], ["A.py", "a.py"]):
            data = deepcopy(original)
            for item, name in zip(data["files"], names):
                item["path"] = name
            self.assert_refused(data)

    def test_pack_refuses_symlinks_non_utf8_and_missing_sources(self):
        oid = self.git("hash-object", "-w", "--stdin", input=b"../outside.txt")
        self.git("update-index", "--add", "--cacheinfo", "120000", oid, "link.txt")
        self.git("commit", "--quiet", "-m", "symlink fixture")
        self.commit = self.git("rev-parse", "HEAD")
        with self.assertRaises(ValueError):
            self.pack(["link.txt"])
        with self.assertRaises(ValueError):
            self.pack(["missing.txt"])
        self.write_source("invalid.txt", b"\xff\xfe")
        self.commit = self.snapshot()
        with self.assertRaisesRegex(ValueError, "UTF-8"):
            self.pack(["invalid.txt"])

    def test_restore_refuses_symlink_parent(self):
        real = self.case / "real-parent"
        real.mkdir()
        link = self.case / "linked-parent"
        link.symlink_to(real.resolve(), target_is_directory=True)
        with self.assertRaises(ValueError):
            package.restore_capsule(self.pack(), link / "destination")
        self.assertEqual(list(real.iterdir()), [])

    def test_count_raw_and_encoded_limits_are_enforced(self):
        with self.assertRaises(ValueError):
            self.pack(["sample.txt"] * 33)
        with self.assertRaises(ValueError):
            self.pack(["sample.txt", "sample.txt"])
        self.write_source("large.txt", b"x" * (package.MAX_SOURCE_BYTES + 1))
        self.commit = self.snapshot()
        with patch.object(package.git_source, "_blobs", side_effect=AssertionError("must preflight size")):
            with self.assertRaisesRegex(ValueError, "4 MiB"):
                self.pack(["large.txt"])
        self.write_source("large.txt", ("\u00e9" * (package.MAX_SOURCE_BYTES // 2)).encode("utf-8"))
        self.commit = self.snapshot()
        with self.assertRaisesRegex(ValueError, "8 MiB"):
            self.pack(["large.txt"])

    def test_qualification_and_actual_portable_replay_are_stable(self):
        report = self.qualified()
        self.assertEqual(report["gates"], {"source_matches": True, "round_trip": True, "artifacts_stable": True})
        self.assertTrue(report["checks"])
        self.assertEqual(report["checks"][0]["exit_code"], 0)
        self.assertGreater(report["checks"][0]["stdout_bytes"], 0)
        before = {path: (self.root / path).read_bytes()
                  for path in [self.args.manifest, self.args.capsule, self.args.report, *package.IMPLEMENTATION]}
        replay = subprocess.run(
            report["replay_argv"], cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        self.assertEqual(replay.returncode, 0, replay.stderr.decode("utf-8"))
        self.assertTrue(json.loads(replay.stdout)["replayed"])
        for path, raw in before.items():
            self.assertEqual((self.root / path).read_bytes(), raw)
        self.assertFalse(list(self.root.glob(".capability-replay-*")))
        self.assertNotIn(str(self.case.resolve()), contracts.json_bytes(report).decode())
        self.assertEqual(report["replay_argv"][3:5], ["--root", "."])

    def test_checks_require_both_explicit_flag_and_manifest_permission(self):
        for flag, permissions in ((False, ["process.execute"]), (True, ["repository.read"])):
            with self.subTest(flag=flag):
                self.pin_manifest(permissions=permissions)
                self.args.allow_checks = flag
                self.args.capsule = f"denied-{flag}.json"
                self.args.report = f"denied-report-{flag}.json"
                with patch.object(package.frames, "run_check", side_effect=AssertionError("must not execute")):
                    report = package.qualify(self.args)
                self.assertEqual(report["outcome"], "failed")
                self.assertEqual(report["checks"], [])
                self.assertTrue((self.root / self.args.report).is_file())

    def test_failed_and_timed_out_checks_leave_failed_reports(self):
        for name, argv, timeout in (
            ("failure", ["python3", "-c", "raise SystemExit(7)"], 3),
            ("timeout", ["python3", "-c", "import time; time.sleep(4)"], 1),
        ):
            with self.subTest(check=name):
                self.pin_manifest(argv=argv, timeout=timeout)
                self.args.capsule, self.args.report = f"{name}.json", f"{name}-report.json"
                report = package.qualify(self.args)
                self.assertEqual(report["outcome"], "failed")
                self.assertEqual(len(report["checks"]), 1)
                if name == "timeout":
                    self.assertTrue(report["checks"][0]["timed_out"])
                else:
                    self.assertEqual(report["checks"][0]["exit_code"], 7)
                with self.assertRaises(ValueError):
                    package.verify(self.args)

    def test_qualification_replays_the_pinned_commit_not_current_checkout_files(self):
        expected = self.pack()
        self.write_source("sample.txt", b"staged later source")
        self.git("add", "sample.txt")
        self.write_source("sample.txt", b"dirty later source")
        report = package.qualify(self.args)
        self.assertEqual(report["outcome"], "passed")
        self.assertTrue(report["gates"]["source_matches"])
        self.assertEqual(json.loads((self.root / self.args.capsule).read_bytes()), expected)
        (self.source / "sample.txt").unlink()
        self.assertEqual(package.verify(self.args)["outcome"], "passed")

    def test_check_mutating_a_pinned_artifact_invalidates_qualification(self):
        self.pin_manifest(argv=["python3", "-c", "from pathlib import Path; Path('check.py').write_text('changed')"])
        report = package.qualify(self.args)
        self.assertEqual(report["checks"][0]["exit_code"], 0)
        self.assertFalse(report["gates"]["artifacts_stable"])
        self.assertEqual(report["outcome"], "failed")

    def test_verify_refuses_report_mutations_even_when_resealed(self):
        original = self.qualified()
        mutations = [
            lambda value: value.update(outcome="failed"),
            lambda value: value["gates"].update(round_trip=False),
            lambda value: value.update(checks=[]),
            lambda value: value["replay_argv"].append("--unexpected"),
            lambda value: value["checks"][0].update(argv=["python3", "-c", "pass"]),
            lambda value: value["checks"][0].update(exit_code=False),
            lambda value: value["capsule"].update(sha256="0" * 64),
            lambda value: value["capability"].update(manifest_sha256="0" * 64),
            lambda value: value["context"].update(repository="other/repository"),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                report = deepcopy(original)
                mutation(report)
                self.write_report(report, reseal=True)
                with patch.object(package.frames, "run_check", side_effect=AssertionError("must refuse first")):
                    with self.assertRaises(ValueError):
                        package.verify(self.args)
        altered = deepcopy(original)
        altered["checks"][0]["duration_ms"] += 1
        self.write_report(altered)
        with self.assertRaisesRegex(ValueError, "integrity"):
            package.verify(self.args)

    def test_verify_refuses_valid_but_different_capsule_source(self):
        report = self.qualified()
        path = self.root / self.args.capsule
        capsule = json.loads(path.read_bytes())
        item = capsule["files"][0]
        old_size = item["bytes"]
        item["text"] = "different source\n"
        body = item["text"].encode()
        item["bytes"], item["sha256"] = len(body), package.frames.digest(body)
        capsule["totals"]["bytes"] += len(body) - old_size
        raw = contracts.json_bytes(capsule)
        path.write_bytes(raw)
        report["capsule"] = {"sha256": package.frames.digest(raw), "bytes": len(raw)}
        self.write_report(report, reseal=True)
        with self.assertRaisesRegex(ValueError, "committed source"):
            package.verify(self.args)

    def test_code_mutation_invalidates_manifest_and_verify(self):
        self.qualified()
        with (self.root / package.ENTRYPOINT).open("ab") as handle:
            handle.write(b"\n# mutated implementation\n")
        with self.assertRaisesRegex(ValueError, "artifact changed"):
            package.verify(self.args)

    def test_replay_runs_real_checks_and_refuses_new_failure_without_rewriting_report(self):
        (self.root / "check.py").write_text(
            "from pathlib import Path\nraise SystemExit(5 if Path('fail-now.txt').exists() else 0)\n",
            encoding="utf-8",
        )
        self.pin_manifest()
        self.qualified()
        report_path = self.root / self.args.report
        before = report_path.read_bytes()
        (self.root / "fail-now.txt").write_text("replay must fail", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "replayed checks failed"):
            package.verify(self.args)
        self.assertEqual(report_path.read_bytes(), before)

    def test_outputs_cannot_escape_overwrite_sources_or_existing_observations(self):
        for capsule, report in (
            ("../escape.json", "report.json"), ("capability.json", "report.json"),
            ("results/capsule.json", "scripts/capability_package.py"),
            ("same.json", "same.json"), ("outer.json", "outer.json/inner.json"),
        ):
            with self.subTest(capsule=capsule, report=report):
                args = Namespace(**vars(self.args))
                args.capsule, args.report = capsule, report
                with self.assertRaises(ValueError):
                    package.qualify(args)
        before = (self.root / "capability.json").read_bytes()
        self.qualified()
        report = (self.root / self.args.report).read_bytes()
        with self.assertRaises(ValueError):
            package.qualify(self.args)
        self.assertEqual((self.root / self.args.report).read_bytes(), report)
        self.assertEqual((self.root / "capability.json").read_bytes(), before)

    def test_cli_failure_is_nonzero_and_success_commands_match_contract(self):
        argv = [
            "qualify", "--root", str(self.root), "--manifest", self.args.manifest,
            "--repo", self.args.repo, "--ref", self.commit, "--repository", self.args.repository,
            "--path", "sample.txt", "--workflow", self.args.workflow,
            "--capsule", self.args.capsule, "--report", self.args.report,
        ]
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(package.main(argv), 1)
        report = json.loads((self.root / self.args.report).read_bytes())
        self.assertEqual(report["outcome"], "failed")
        self.assertEqual(report["checks"], [])

    def test_cli_pack_restore_and_collision_refusal(self):
        prefix = ["python3", package.ENTRYPOINT]
        environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        packed = subprocess.run(
            [*prefix, "pack", "--repo", "../source", "--ref", self.commit,
             "--repository", self.args.repository, "--path", "sample.txt", "--output", "packed.json"],
            cwd=self.root, env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(packed.returncode, 0, packed.stderr.decode())
        command = [*prefix, "restore", "--capsule", "packed.json", "--destination", "restored"]
        restored = subprocess.run(command, cwd=self.root, env=environment, capture_output=True, check=False)
        self.assertEqual(restored.returncode, 0, restored.stderr.decode())
        self.assertEqual((self.root / "restored/sample.txt").read_bytes(), (self.source / "sample.txt").read_bytes())
        collision = subprocess.run(command, cwd=self.root, env=environment, capture_output=True, check=False)
        self.assertNotEqual(collision.returncode, 0)
        self.assertEqual((self.root / "restored/sample.txt").read_bytes(), (self.source / "sample.txt").read_bytes())

    def test_restore_failure_cleans_only_its_new_owned_directory(self):
        destination = self.case / "failed-restore"
        marker = self.case / "unrelated.txt"
        marker.write_text("keep", encoding="utf-8")
        with patch.object(package, "_compare_files", side_effect=ValueError("verification failed")):
            with self.assertRaises(ValueError):
                package.restore_capsule(self.pack(), destination)
        self.assertFalse(destination.exists())
        self.assertEqual(marker.read_text(), "keep")

    def test_deleted_committed_source_is_not_an_available_output(self):
        self.write_source("unselected.json", b'{"source":true}\n')
        self.commit = self.snapshot()
        (self.source / "unselected.json").unlink()
        with self.assertRaisesRegex(ValueError, "committed source"):
            package._not_committed_output(
                (self.source / "unselected.json").resolve(), self.source.resolve(), self.pack(),
            )
        self.assertFalse((self.source / "unselected.json").exists())


if __name__ == "__main__":
    unittest.main()
