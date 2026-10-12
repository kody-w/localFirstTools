#!/usr/bin/env python3
"""Non-skipping release gate for the repository-autocomplete implementation."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import quote


def command(argv, cwd, timeout=300):
    result = subprocess.run(
        argv, cwd=cwd, check=False, text=True, capture_output=True, timeout=timeout
    )
    if result.returncode:
        raise RuntimeError(
            f"{argv[0]} exited {result.returncode}\n"
            f"{result.stdout[-4000:]}\n{result.stderr[-4000:]}"
        )
    return result.stdout


def check_catalog(repo):
    path = repo / "landgrab/autocomplete/catalog.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "localfirst-autocomplete-catalog/v1":
        raise ValueError("Missing or incorrect published catalog schema.")
    revision = data["repository"]["commit"]
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", revision):
        raise ValueError("Catalog revision must be a full Git object ID.")
    resolved = command(["git", "rev-parse", f"{revision}^{{commit}}"], repo).strip()
    if resolved != revision:
        raise ValueError("Catalog source is not an exact available commit.")
    if command(["git", "rev-parse", f"{revision}^{{tree}}"], repo).strip() != data["repository"]["tree"]:
        raise ValueError("Catalog tree does not belong to its declared commit.")
    tools = data["tools"]
    if not tools or data["counts"]["canonical_tools"] != len(tools):
        raise ValueError("Canonical catalog must contain real, consistently counted records.")
    if len({item["id"] for item in tools}) != len(tools):
        raise ValueError("Canonical IDs are not unique.")
    for item in tools:
        encoded_path = quote(item["path"], safe="/", errors="surrogateescape")
        repository = data["repository"]["full_name"]
        expected_sources = {
            f"https://github.com/{repository}/blob/{revision}/{encoded_path}",
            f"https://raw.githubusercontent.com/{repository}/{revision}/{encoded_path}",
        }
        if item["source_url"] not in expected_sources:
            raise ValueError(f"Unpinned source URL: {item['path']}")
    sample = sorted(tools, key=lambda item: item["path"])[0]
    raw = subprocess.run(
        ["git", "show", f"{revision}:{sample['path']}"],
        cwd=repo, check=True, capture_output=True, timeout=60,
    ).stdout
    if hashlib.sha256(raw).hexdigest() != sample["sha256"]:
        raise ValueError("A real source object's bytes do not match its passport.")
    with tempfile.TemporaryDirectory(prefix="autocomplete-catalog-gate-") as temporary:
        expected_path = Path(temporary).resolve() / "catalog.json"
        command(
            [sys.executable, "scripts/autocomplete_catalog.py",
             "--repo", str(repo), "--ref", revision, "--output", str(expected_path),
             "--repository", data["repository"]["full_name"],
             "--site-url", data["repository"]["site_url"],
             "--max-tasks", str(data["planning"]["task_limit"])], repo
        )
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        verify_index_projection(data, expected, "Published catalog differs from its committed source-tree projection.")
    return f"{len(tools)} canonical records match the complete committed-tree projection"


def check_operator(repo):
    root = repo / "landgrab/autocomplete"
    document = (root / "operator.html").read_bytes()
    manifest = json.loads((root / "operator.manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") != "rapp/1-html" or manifest.get("file") != "operator.html":
        raise ValueError("Incorrect operator binding.")
    if len(document) != manifest["bytes"]:
        raise ValueError("Operator byte count mismatch.")
    if hashlib.sha256(document).hexdigest() != manifest["sha256"]:
        raise ValueError("Operator SHA-256 mismatch.")
    return "operator bytes match the committed manifest"


def check_unit_tests(repo, reference):
    os.environ["RAPP_REFERENCE_DIR"] = str(reference)
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))
    suite = unittest.defaultTestLoader.discover(
        str(repo / "tests"), pattern="test_autocomplete_*.py"
    )
    def modules(tests):
        for test in tests:
            if isinstance(test, unittest.TestSuite):
                yield from modules(test)
            else:
                yield type(test).__module__.rsplit(".", 1)[-1]

    covered = set(modules(suite))
    required = {"test_autocomplete_catalog", "test_autocomplete_frames", "test_autocomplete_gate"}
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful() or not result.testsRun or result.skipped or not required <= covered:
        raise ValueError(
            f"Unit gate requires nonempty, successful, non-skipped coverage: "
            f"run={result.testsRun}, skipped={len(result.skipped)}, "
            f"missing_modules={sorted(required - covered)}"
        )
    return f"{result.testsRun} checks ran with no skips"


def verify_index_projection(published, expected, message="Published evidence differs from the projection of verified frame payloads."):
    actual_content = {key: value for key, value in published.items() if key != "generated_at"}
    expected_content = {key: value for key, value in expected.items() if key != "generated_at"}
    if actual_content != expected_content:
        raise ValueError(message)


def verify_event_projection(event, frame, relative_path):
    for key in ("run_id", "worker", "phase", "outcome", "summary", "artifacts", "checks",
                "references", "repository", "changed_artifacts", "base_commit_unchanged"):
        if key not in event or event[key] != frame["payload"][key]:
            raise ValueError(f"Published event changes verified payload field: {key}")
    for key in ("utc", "stream_id", "seq", "payload_hash", "frame_hash"):
        if key not in event or event[key] != frame[key]:
            raise ValueError(f"Published event changes verified envelope field: {key}")
    if event.get("path") != relative_path:
        raise ValueError("Published event points to a different frame file.")


def check_frames(repo, reference):
    store = repo / "landgrab/autocomplete/provenance"
    command(
        [sys.executable, "scripts/autocomplete_frames.py", "verify",
         "--store", str(store), "--rapp-dir", str(reference), "--repo", str(repo)], repo
    )
    result = json.loads(command(
        [sys.executable, str(reference / "rapp_check.py"), str(store), "--json"], repo
    ))
    frames = list(store.glob("runs/*/*/frames/[0-9]*.json"))
    streams = {path.parent for path in frames}
    if result["verdict"] != "COMPLIANT" or not frames or len(streams) < 2:
        raise ValueError("Require COMPLIANT, emitted frames, and at least two independent streams.")
    index = json.loads((repo / "landgrab/autocomplete/evidence.json").read_text(encoding="utf-8"))
    if index.get("schema") != "localfirst-autocomplete-evidence/v1":
        raise ValueError("Missing evidence index.")
    if index["counts"]["frames"] != len(frames) or len(index["events"]) != len(frames):
        raise ValueError("Evidence index is stale or does not account for every stored frame.")
    stored = {
        value["frame_hash"]: (path, value)
        for path in frames
        for value in [json.loads(path.read_text(encoding="utf-8"))]
    }
    if len(stored) != len(frames) or {event["frame_hash"] for event in index["events"]} != set(stored):
        raise ValueError("Browser evidence refers to different frames.")
    for event in index["events"]:
        path, frame = stored[event["frame_hash"]]
        verify_event_projection(event, frame, path.relative_to(store).as_posix())
    stream_ids = {frame["stream_id"] for _, frame in stored.values()}
    if len(stream_ids) != len(streams):
        raise ValueError("Separate directories do not represent distinct worker streams.")
    with tempfile.TemporaryDirectory(prefix="autocomplete-index-gate-") as temporary:
        expected_path = Path(temporary).resolve() / "evidence.json"
        command(
            [sys.executable, "scripts/autocomplete_frames.py", "index",
             "--store", str(store), "--rapp-dir", str(reference),
             "--output", str(expected_path)], repo
        )
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        verify_index_projection(index, expected)
    return f"{len(frames)} conforming frames across {len(streams)} independent streams"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--rapp-dir", required=True, type=Path)
    parser.add_argument("--cdp", required=True, help="Explicit isolated-browser loopback CDP URL.")
    parser.add_argument("--url", required=True, help="Loopback workbench URL served from --repo.")
    args = parser.parse_args()
    repo, reference = args.repo.resolve(), args.rapp_dir.resolve()
    checks = [
        ("unit and refusal behavior", lambda: check_unit_tests(repo, reference)),
        ("committed-source catalog", lambda: check_catalog(repo)),
        ("operator binding", lambda: check_operator(repo)),
        ("real parallel RAPP evidence", lambda: check_frames(repo, reference)),
        ("integrated browser output", lambda: command(
            ["node", "tests/test_autocomplete_workbench.mjs",
             "--cdp", args.cdp, "--url", args.url, "--require-published"], repo)),
    ]
    failed = []
    for name, check in checks:
        try:
            detail = check()
        except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError) as error:
            failed.append(name)
            print(f"FAIL {name}: {error}", flush=True)
        else:
            print(f"PASS {name}: {str(detail).strip()}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
