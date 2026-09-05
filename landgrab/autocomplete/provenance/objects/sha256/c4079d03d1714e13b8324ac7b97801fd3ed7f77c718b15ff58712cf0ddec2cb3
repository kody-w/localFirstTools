import copy
import hashlib
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

from scripts import capability_contracts as contracts


class CapabilityContractTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.source = self.root / "worker.py"
        self.source.write_bytes(b"print('public capability')\n")
        self.manifest = {
            "schema": contracts.CAPABILITY_SCHEMA,
            "id": "source-capsule",
            "version": "1.0.0",
            "title": "Source capsule",
            "job": "Transfer and restore exact committed public source bytes.",
            "entrypoint": "worker.py",
            "artifacts": [{
                "path": "worker.py",
                "sha256": hashlib.sha256(self.source.read_bytes()).hexdigest(),
                "bytes": self.source.stat().st_size,
            }],
            "contract": {
                "inputs": {"type": "object"},
                "outputs": {"type": "object"},
                "permissions": ["repository.read", "artifact.write", "process.execute"],
                "network": "none",
            },
            "checks": [{"id": "source-check", "argv": ["python3", "worker.py"],
                        "timeout_seconds": 30}],
            "failure_cases": ["A changed source fingerprint is rejected."],
            "reuses": [],
            "visibility": "public",
        }
        self.path = self.root / "asset.json"

    def save(self, manifest=None):
        contracts.atomic_json(self.path, manifest or self.manifest)

    def test_valid_manifest_binds_current_source(self):
        self.save()
        value, revision = contracts.load_manifest(self.path, self.root)
        self.assertEqual(value, self.manifest)
        self.assertEqual(revision, hashlib.sha256(self.path.read_bytes()).hexdigest())

    def test_changed_source_cannot_keep_old_manifest_revision(self):
        self.save()
        self.source.write_bytes(b"print('different implementation')\n")
        with self.assertRaisesRegex(ValueError, "artifact changed"):
            contracts.load_manifest(self.path, self.root)

    def test_missing_entrypoint_pin_is_rejected(self):
        value = copy.deepcopy(self.manifest)
        value["entrypoint"] = "other.py"
        with self.assertRaisesRegex(ValueError, "entrypoint"):
            contracts.validate_manifest(value)

    def test_unsafe_paths_permissions_and_empty_evidence_are_rejected(self):
        mutations = [
            lambda value: value["artifacts"][0].update(path="../private.py"),
            lambda value: value["contract"].update(network="unrestricted"),
            lambda value: value["contract"]["permissions"].append("production.deploy"),
            lambda value: value.update(checks=[]),
            lambda value: value.update(failure_cases=[]),
            lambda value: value["artifacts"][0].update(bytes=1.0),
            lambda value: value["checks"][0].update(timeout_seconds=0),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                value = copy.deepcopy(self.manifest)
                mutate(value)
                with self.assertRaises(ValueError):
                    contracts.validate_manifest(value)

    def test_source_symlink_is_rejected(self):
        (self.root / "alias.py").symlink_to(self.source)
        with self.assertRaises(ValueError):
            contracts.source_path(self.root, "alias.py")

    def test_notice_is_preserved_as_an_explicit_public_source(self):
        notice = self.root / "NOTICE"
        notice.write_text("Attribution accompanying licensed source.\n", encoding="utf-8")
        self.assertEqual(contracts.source_path(self.root, "NOTICE"), notice)

    def test_self_dependency_and_duplicate_artifact_are_rejected(self):
        value = copy.deepcopy(self.manifest)
        value["reuses"] = [{"id": value["id"], "manifest_sha256": "a" * 64}]
        with self.assertRaises(ValueError):
            contracts.validate_manifest(value)
        value = copy.deepcopy(self.manifest)
        value["artifacts"].append(dict(value["artifacts"][0]))
        with self.assertRaises(ValueError):
            contracts.validate_manifest(value)

    def test_duplicate_json_fields_cannot_change_meaning(self):
        self.path.write_text('{"schema":"first","schema":"second"}', encoding="utf-8")
        with self.assertRaises(ValueError):
            contracts.load_json(self.path)

    def test_atomic_json_has_deterministic_bytes(self):
        first = contracts.json_bytes({"b": 2, "a": 1})
        self.assertEqual(first, contracts.json_bytes({"a": 1, "b": 2}))
        contracts.atomic_json(self.path, {"b": 2, "a": 1})
        self.assertEqual(self.path.read_bytes(), first)
        self.assertEqual(json.loads(first), {"a": 1, "b": 2})

    def test_replay_contract_rejects_help_duplicate_and_option_like_values(self):
        valid = contracts.source_replay_argv(
            "scripts/capability_package.py", "asset.json", "../source", "capsule.json", "report.json"
        )
        self.assertEqual(contracts.validate_source_replay(valid, valid[1])["repo"], "../source")
        mutations = [
            [*valid, "--help"],
            [*valid, "--manifest", "other.json"],
            valid[:8] + ["--help"] + valid[9:],
            valid[:-1],
        ]
        for value in mutations:
            with self.subTest(argv=value):
                with self.assertRaises(ValueError):
                    contracts.validate_source_replay(value, valid[1])

    def test_python_help_shaped_script_name_cannot_be_a_capability(self):
        script = self.root / "-h.py"
        script.write_text("raise SystemExit(7)\n", encoding="utf-8")
        observed = subprocess.run(
            [sys.executable, "-h.py", "verify"], cwd=self.root,
            capture_output=True, text=True, check=False, timeout=10,
        )
        self.assertEqual(observed.returncode, 0)
        self.assertIn("usage:", observed.stdout.lower())
        manifest = copy.deepcopy(self.manifest)
        manifest["entrypoint"] = "-h.py"
        manifest["artifacts"] = [{
            "path": "-h.py", "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "bytes": script.stat().st_size,
        }]
        with self.assertRaisesRegex(ValueError, "option-like script"):
            contracts.validate_manifest(manifest)
        with self.assertRaisesRegex(ValueError, "option-like script"):
            contracts.source_replay_argv("-h.py", "asset.json", ".", "capsule.json", "report.json")


if __name__ == "__main__":
    unittest.main()
