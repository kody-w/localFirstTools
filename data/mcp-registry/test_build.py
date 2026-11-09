"""Offline build regressions. Run python3 -B data/mcp-registry/test_build.py."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import rapp


ROOT = Path(__file__).resolve().parent


def snapshot(root):
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*") if path.is_file()
            and not any(part.startswith(".") for part in path.relative_to(root).parts)
            and "__pycache__" not in path.parts}


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".test-", dir=ROOT)
        self.work = Path(self.temp.name)
        for path in ROOT.iterdir():
            if path.name.startswith(".") and path.name != ".nojekyll":
                continue
            if path.name == "__pycache__":
                continue
            target = self.work / path.name
            if path.is_dir():
                shutil.copytree(path, target)
            else:
                shutil.copyfile(path, target)

    def tearDown(self):
        self.temp.cleanup()

    def rebuild(self):
        code = (
            "import pathlib, runpy, socket, sys; "
            "root=pathlib.Path(sys.argv[1]); sys.path.insert(0,str(root)); "
            "socket.socket=lambda *a,**k: (_ for _ in ()).throw(OSError('offline')); "
            "runpy.run_path(str(root/'build.py'),run_name='__main__')"
        )
        subprocess.run([sys.executable, "-I", "-B", "-c", code, str(self.work)],
                       check=True, timeout=20, capture_output=True)

    def assert_index(self):
        registry = json.loads((self.work / "registry.json").read_text())
        for entry in registry["entries"]:
            source = self.work / entry["path"]
            content = source.read_bytes()
            sha8 = hashlib.sha256(content).hexdigest()[:12]
            self.assertEqual(entry["sha8"], sha8)
            version = self.work / "versions" / entry["name"] / (sha8 + source.suffix)
            self.assertEqual(version.read_bytes(), content)

    def test_repeated_build_and_deleted_outputs(self):
        before = snapshot(self.work)
        for _ in range(2):
            self.rebuild()
            self.assertEqual(snapshot(self.work), before)
        registry = json.loads((self.work / "registry.json").read_text())
        deleted = {"registry.json", "api/v1/servers.json", "api/v1/status.json",
                   "api/v1/badge.json", "llms.txt", ".nojekyll", "chain.jsonl", "orient.json"}
        deleted.update("versions/" + entry["name"] + "/" + entry["sha8"] +
                       Path(entry["path"]).suffix for entry in registry["entries"])
        for relative in deleted:
            (self.work / relative).unlink()
        self.rebuild()
        self.assertEqual(snapshot(self.work), before)
        self.assertEqual((self.work / ".nojekyll").read_bytes(), b"")
        self.assert_index()

    def test_changed_input_refreshes_chain_and_preserves_versions(self):
        before = snapshot(self.work)
        source = sorted((self.work / "servers").glob("*.json"))[0]
        server = json.loads(source.read_text())
        server["description"] = "Updated local documentation server."
        source.write_text(json.dumps(server))
        self.rebuild()
        expected = sorted(
            (json.loads(path.read_text()) for path in (self.work / "servers").glob("*.json")),
            key=lambda value: value["name"],
        )
        endpoint = json.loads((self.work / "api/v1/servers.json").read_text())
        self.assertEqual(endpoint["servers"], expected)
        head = None
        for seq, (line, entry) in enumerate(zip(
            (self.work / "chain.jsonl").read_text().splitlines(), expected, strict=True
        )):
            frame = json.loads(line)
            self.assertTrue(rapp.verify_frame(frame, head=head)[0])
            self.assertEqual(frame["seq"], seq)
            self.assertEqual(frame["payload"], entry)
            head = frame
        orient = json.loads((self.work / "orient.json").read_text())
        self.assertEqual(orient["head"], {"seq": head["seq"], "frame_hash": head["frame_hash"]})
        self.assertNotEqual((self.work / "chain.jsonl").read_bytes(), before["chain.jsonl"])
        for relative, content in before.items():
            if relative.startswith("versions/"):
                self.assertEqual((self.work / relative).read_bytes(), content)
        self.assert_index()


if __name__ == "__main__":
    unittest.main()
