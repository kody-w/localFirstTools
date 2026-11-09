"""Offline regression tests for rebuilding, immutable history, and live local queries."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent
META = "io.modelcontextprotocol.registry/publisher-provided"


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".build-test-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name) / "work"
        self.data = self.work / "data/mcp-registry"
        shutil.copytree(
            ROOT, self.data,
            ignore=lambda directory, names: [
                name for name in names
                if name.startswith((".build-test-", ".validation")) or name == "__pycache__"
            ],
        )

    def build(self):
        subprocess.run(
            [sys.executable, "-B", str(self.data / "build.py")],
            cwd=self.work, check=True, capture_output=True, text=True,
        )

    def snapshot(self):
        return {
            path.relative_to(self.data).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.data.rglob("*") if path.is_file()
        }

    def test_rebuild_restores_deleted_outputs_and_current_blobs(self):
        before = self.snapshot()
        for _ in range(2):
            self.build()
            self.assertEqual(before, self.snapshot())
        registry = json.loads((self.data / "registry.json").read_text())
        for entry in registry["entries"]:
            (self.data / entry["version_path"]).unlink()
        for name in ["api/v1/servers.json", "api/v1/status.json", "api/v1/badge.json",
                     "chain.jsonl", "orient.json", "registry.json", "llms.txt", ".nojekyll"]:
            (self.data / name).unlink()
        self.build()
        self.assertEqual(before, self.snapshot())

    def test_changed_input_refreshes_catalog_chain_and_preserves_history(self):
        registry_before = (self.data / "registry.json").read_bytes()
        orient_before = json.loads((self.data / "orient.json").read_text())
        history = {
            path.relative_to(self.data): path.read_bytes()
            for path in (self.data / "versions").rglob("*") if path.is_file()
        }
        source = self.data / "servers/context7.json"
        server = json.loads(source.read_text())
        server["description"] = "Updated local documentation discovery."
        source.write_text(json.dumps(server) + "\n")
        self.build()
        self.assertNotEqual(registry_before, (self.data / "registry.json").read_bytes())
        self.assertNotEqual(orient_before["head"], json.loads((self.data / "orient.json").read_text())["head"])
        endpoint = json.loads((self.data / "api/v1/servers.json").read_text())
        self.assertIn(server, endpoint["servers"])
        registry = json.loads((self.data / "registry.json").read_text())
        for entry in registry["entries"]:
            current = (self.data / entry["path"]).read_bytes()
            self.assertEqual(entry["sha8"], hashlib.sha256(current).hexdigest()[:12])
            self.assertEqual(current, (self.data / entry["version_path"]).read_bytes())
        for path, data in history.items():
            self.assertEqual(data, (self.data / path).read_bytes())
        before = self.snapshot()
        self.build()
        self.assertEqual(before, self.snapshot())

    def test_agent_queries_follow_changed_endpoint_without_reinitialization(self):
        sys.path.insert(0, str(ROOT.parents[1] / "agents"))
        self.addCleanup(sys.path.pop, 0)
        from agents import mcp_registry
        with patch.object(mcp_registry, "__file__", str(self.work / "agents/mcp_registry.py")):
            agent = mcp_registry.MCPRegistryAgent()
            path = self.data / "api/v1/servers.json"
            endpoint = json.loads(path.read_text())
            self.assertEqual(endpoint["servers"], json.loads(agent.perform())["servers"])
            tools = {tool["name"] for server in endpoint["servers"] for tool in server["_meta"][META]["tools"]}
            for tool in tools:
                expected = [
                    server for server in endpoint["servers"]
                    if any(item["name"] == tool for item in server["_meta"][META]["tools"])
                ]
                self.assertEqual(expected, json.loads(agent.perform(tool=tool))["servers"])
            self.assertEqual([], json.loads(agent.perform(tool="no-such-tool"))["servers"])
            endpoint["servers"][0]["_meta"][META]["tools"].append({"name": "local-new-tool"})
            path.write_text(json.dumps(endpoint) + "\n")
            self.assertEqual(
                [endpoint["servers"][0]],
                json.loads(agent.perform(tool="local-new-tool"))["servers"],
            )


if __name__ == "__main__":
    unittest.main()
