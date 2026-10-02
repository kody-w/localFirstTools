#!/usr/bin/env python3
"""Non-skipping acceptance gate for the evergreen capability/reuse loop."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


def command(argv, root, timeout=300):
    result = subprocess.run(argv, cwd=root, capture_output=True, text=True,
                            check=False, timeout=timeout)
    if result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv[0]}\n"
            f"{result.stdout[-3000:]}\n{result.stderr[-3000:]}"
        )
    return result.stdout


def unit_gate(root, reference):
    os.environ["RAPP_REFERENCE_DIR"] = str(reference)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    suite = unittest.defaultTestLoader.discover(str(root / "tests"), pattern="test_capability_*.py")

    def module_names(tests):
        for item in tests:
            if isinstance(item, unittest.TestSuite):
                yield from module_names(item)
            else:
                yield type(item).__module__.rsplit(".", 1)[-1]

    modules = set(module_names(suite))
    required = {
        "test_capability_contracts", "test_capability_registry",
        "test_capability_package", "test_capability_scheduler",
    }
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful() or result.skipped or not result.testsRun or not required <= modules:
        raise ValueError(
            f"nonempty passing coverage is required; run={result.testsRun}, "
            f"skips={len(result.skipped)}, missing={sorted(required - modules)}"
        )
    return f"{result.testsRun} checks; zero skips"


def binding_gate(root):
    directory = root / "landgrab/autocomplete/capabilities"
    document = (directory / "operator.html").read_bytes()
    manifest = json.loads((directory / "operator.manifest.json").read_text(encoding="utf-8"))
    if manifest.get("file") != "operator.html" or manifest.get("schema") != "rapp/1-html":
        raise ValueError("incorrect operator binding")
    if len(document) != manifest["bytes"] or hashlib.sha256(document).hexdigest() != manifest["sha256"]:
        raise ValueError("operator changed without a matching byte binding")
    return "operator bytes match their manifest"


def registry_gate(root, reference):
    prefix = "landgrab/autocomplete/capabilities"
    command([
        sys.executable, "scripts/capability_registry.py", "verify",
        "--root", ".", "--registry", f"{prefix}/registry.json",
        "--manifests", f"{prefix}/manifests", "--store", f"{prefix}/provenance",
        "--rapp-dir", str(reference),
    ], root)
    registry = json.loads((root / prefix / "registry.json").read_text(encoding="utf-8"))
    if registry.get("schema") != "localfirst-capability-registry/v1":
        raise ValueError("missing capability registry")
    matches = [asset for asset in registry["assets"] if asset["id"] == "source-capsule"]
    if len(matches) != 1 or matches[0]["status"] != "reused":
        raise ValueError("the unchanged source-capsule capability has not earned reused status")
    asset = matches[0]
    uses = asset["uses"]
    repositories = {use["repository"].casefold() for use in uses}
    commits = {use["commit"] for use in uses}
    trees = {use["tree"] for use in uses}
    if not {"kody-w/localfirsttools", "kody-w/openrappter"} <= repositories:
        raise ValueError("the demonstration must include both real source projects")
    if min(len(repositories), len(commits), len(trees)) < 2:
        raise ValueError("renamed checkouts or repeated inputs are not independent reuse")
    return f"one pinned capability reused across {len(repositories)} distinct repositories"


def evidence_gate(root, reference):
    store = "landgrab/autocomplete/capabilities/provenance"
    result = json.loads(command([
        sys.executable, "scripts/autocomplete_frames.py", "verify",
        "--store", store, "--rapp-dir", str(reference), "--repo", ".",
    ], root))
    if result["verification"]["verdict"] != "COMPLIANT":
        raise ValueError("capability evidence is not conforming")
    if result["counts"]["frames"] < 2 or result["counts"]["streams"] < 2:
        raise ValueError("require actual emitted evidence from independent jobs")
    return f"{result['counts']['frames']} real frames in {result['counts']['streams']} streams"


def exercise_gate(root, reference):
    prefix = "landgrab/autocomplete/capabilities"
    with tempfile.TemporaryDirectory(prefix=".capability-gate-", dir=root) as temporary:
        scratch = Path(temporary).resolve()
        relative = scratch.relative_to(root).as_posix()
        registry = f"{relative}/registry.json"
        plan = f"{relative}/plan.json"
        state = f"{relative}/state"
        store = f"{relative}/provenance"
        command([
            sys.executable, "scripts/autocomplete_frames.py", "init",
            "--store", store, "--rapp-dir", str(reference),
            "--owner", "test-owner", "--slug", "capability-qualification",
        ], root)
        command([
            sys.executable, "scripts/capability_registry.py", "build",
            "--root", ".", "--manifests", f"{prefix}/manifests", "--output", registry,
        ], root)
        command([
            sys.executable, "scripts/capability_scheduler.py", "plan",
            "--root", ".", "--registry", registry, "--requests", f"{prefix}/requests.json",
            "--policy", f"{prefix}/policy.json", "--state", state, "--output", plan,
        ], root)
        run = [
            sys.executable, "scripts/capability_scheduler.py", "run",
            "--root", ".", "--plan", plan, "--policy", f"{prefix}/policy.json",
            "--state", state, "--store", store, "--rapp-dir", str(reference), "--jobs", "2",
        ]
        command(run, root, timeout=600)
        verify = [
            sys.executable, "scripts/autocomplete_frames.py", "verify",
            "--store", store, "--rapp-dir", str(reference), "--repo", ".",
        ]
        before = json.loads(command(verify, root))
        if before["counts"]["frames"] < 2 or before["counts"]["streams"] < 2:
            raise ValueError("fresh execution did not produce independent real job evidence")
        command([
            sys.executable, "scripts/capability_registry.py", "build",
            "--root", ".", "--manifests", f"{prefix}/manifests",
            "--store", store, "--rapp-dir", str(reference), "--output", f"{relative}/reused-registry.json",
        ], root)
        regenerated = json.loads((scratch / "reused-registry.json").read_text(encoding="utf-8"))
        asset = next((item for item in regenerated["assets"] if item["id"] == "source-capsule"), None)
        if asset is None or asset["status"] != "reused":
            raise ValueError("fresh real execution did not earn evidence-derived reuse")
        frozen = {event["path"]: event["frame_hash"] for event in before["events"]}
        command(run, root, timeout=600)
        after = json.loads(command(verify, root))
        if {event["path"]: event["frame_hash"] for event in after["events"]} != frozen:
            raise ValueError("replaying completed work created or changed frame history")
        return "fresh two-project execution earns reuse; completed-plan replay creates no new frames"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--rapp-dir", required=True, type=Path)
    parser.add_argument("--exercise", action="store_true",
                        help="Execute both real source jobs in fresh owned state and replay for idempotency.")
    args = parser.parse_args()
    root, reference = args.root.resolve(), args.rapp_dir.resolve()
    checks = [
        ("capability behavior and refusal cases", lambda: unit_gate(root, reference)),
        ("canonical operator binding", lambda: binding_gate(root)),
        ("evidence-derived independent reuse", lambda: registry_gate(root, reference)),
        ("actual capability RAPP evidence", lambda: evidence_gate(root, reference)),
    ]
    if args.exercise:
        checks.append(("fresh reuse and duplicate-run refusal", lambda: exercise_gate(root, reference)))
    failures = []
    for name, check in checks:
        try:
            result = check()
        except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.SubprocessError) as error:
            failures.append(name)
            print(f"FAIL {name}: {error}", flush=True)
        else:
            print(f"PASS {name}: {result}", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
