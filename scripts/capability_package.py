#!/usr/bin/env python3
"""Transport explicit committed UTF-8 sources and replay bounded capability checks."""

import argparse
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import uuid

if __package__:
    from . import autocomplete_catalog as git_source
    from . import autocomplete_frames as frames
    from . import capability_contracts as contracts
else:
    import autocomplete_catalog as git_source
    import autocomplete_frames as frames
    import capability_contracts as contracts


MAX_FILES = 32
MAX_SOURCE_BYTES = 4 * 1024 * 1024
ENTRYPOINT = "scripts/capability_package.py"
IMPLEMENTATION = {
    ENTRYPOINT: Path(__file__),
    "scripts/capability_contracts.py": Path(contracts.__file__),
    "scripts/autocomplete_catalog.py": Path(git_source.__file__),
    "scripts/autocomplete_frames.py": Path(frames.__file__),
}
LIMITATIONS = [
    "Qualification proves only the explicit source transport, restore, and declared command observations.",
    "Checks are trusted local processes, not a sandbox; network:none is a declared contract, not OS network isolation.",
    "Capability implementation artifacts are compared before and after; source content is bound to the selected immutable Git commit, not the checkout's current files.",
    "Path and secret-shaped-value guards are not a general secret scanner; selected public source still requires human review.",
    "The report integrity hash detects uncoordinated edits, not forgery; reports do not authenticate authorship or prove first invention.",
    "Check durations and output hashes are historical observations; replay requires passing checks, not identical timings or nondeterministic output.",
    "Bounded process checks and exact executable-mode restoration require POSIX support.",
]
require = contracts.require


def _public_source(text):
    require(isinstance(text, str) and len(text) <= MAX_SOURCE_BYTES, "source text exceeds its bound")
    try:
        body = text.encode("utf-8")
    except UnicodeError as exc:
        raise contracts.ContractError("source must be strict UTF-8") from exc
    require(not any(ord(c) < 32 and c not in "\t\r\n" or ord(c) == 127 for c in text),
            "binary/control bytes are not public source text")
    require(not frames.PRIVATE_TEXT.search(text), "secret-shaped source is forbidden")
    return body


def validate_capsule(data):
    require(isinstance(data, dict) and set(data) == {"schema", "origin", "files", "totals"},
            "invalid source capsule fields")
    require(data["schema"] == contracts.CAPSULE_SCHEMA, "unsupported source capsule schema")
    origin = data["origin"]
    require(isinstance(origin, dict) and set(origin) == {"repository", "commit", "tree"},
            "invalid capsule origin")
    require(isinstance(origin["repository"], str), "repository must be a public owner/name")
    git_source._repository(origin["repository"], None)
    contracts.committed_ref(origin["commit"])
    contracts.committed_ref(origin["tree"])
    files = data["files"]
    require(isinstance(files, list) and 1 <= len(files) <= MAX_FILES, "select 1-32 source files")
    names, total = [], 0
    for item in files:
        require(isinstance(item, dict) and set(item) == {"path", "mode", "sha256", "bytes", "text"},
                "invalid capsule file fields")
        name = str(frames.artifact_path(item["path"]))
        require(isinstance(item["mode"], str) and item["mode"] in {"100644", "100755"},
                "only regular Git source modes are supported")
        contracts.sha256(item["sha256"])
        require(type(item["bytes"]) is int and 0 <= item["bytes"] <= MAX_SOURCE_BYTES,
                "invalid source byte count")
        body = _public_source(item["text"])
        require(len(body) == item["bytes"] and frames.digest(body) == item["sha256"],
                "capsule source hash or byte count mismatch")
        names.append(name)
        total += len(body)
        require(total <= MAX_SOURCE_BYTES, "aggregate source exceeds 4 MiB")
    require(names == sorted(names) and len(set(name.casefold() for name in names)) == len(names),
            "capsule paths must be sorted, unique, and case-unambiguous")
    folded = {name.casefold() for name in names}
    require(not any(str(parent).casefold() in folded
                    for name in names for parent in Path(name).parents if str(parent) != "."),
            "capsule file/directory path collision")
    totals = data["totals"]
    require(isinstance(totals, dict) and set(totals) == {"files", "bytes"}
            and type(totals["files"]) is int and type(totals["bytes"]) is int
            and totals == {"files": len(files), "bytes": total}, "capsule totals mismatch")
    require(len(contracts.json_bytes(data)) <= contracts.MAX_JSON_BYTES,
            "encoded capsule exceeds 8 MiB")
    return data


def pack_sources(repo, ref, repository, paths):
    repo = frames.root_path(repo)
    contracts.committed_ref(ref)
    repository = git_source._repository(repository, None)["full_name"]
    require(isinstance(paths, (list, tuple)) and 1 <= len(paths) <= MAX_FILES,
            "select 1-32 explicit source paths")
    names = [str(frames.artifact_path(path)) for path in paths]
    require(len(set(names)) == len(names), "duplicate selected source path")
    commit, tree, entries = git_source._snapshot(repo, ref)
    require(not git_source._git(repo, "rev-parse", "--show-prefix").strip(),
            "source checkout must be the Git repository root")
    sizes, total = {}, 0
    for name in names:
        entry = entries.get(name)
        require(entry is not None and entry.kind == "blob" and entry.mode in {"100644", "100755"},
                "selected source must be a committed regular file")
        if entry.oid not in sizes:
            sizes[entry.oid] = int(git_source._git(repo, "cat-file", "-s", entry.oid))
        total += sizes[entry.oid]
        require(total <= MAX_SOURCE_BYTES, "aggregate source exceeds 4 MiB")
    blobs = dict(git_source._blobs(repo, sizes))
    files = []
    for name in sorted(names):
        entry = entries[name]
        body = blobs[entry.oid]
        require(len(body) == sizes[entry.oid], "committed blob size changed")
        try:
            text = body.decode("utf-8")
        except UnicodeError as exc:
            raise contracts.ContractError("selected source is not strict UTF-8") from exc
        files.append({"path": name, "mode": entry.mode, "sha256": frames.digest(body),
                      "bytes": len(body), "text": text})
    return validate_capsule({
        "schema": contracts.CAPSULE_SCHEMA,
        "origin": {"repository": repository, "commit": commit, "tree": tree},
        "files": files, "totals": {"files": len(files), "bytes": total},
    })


def _compare_files(data, root):
    for item in data["files"]:
        path = root.joinpath(*frames.artifact_path(item["path"]).parts)
        body = frames.read_bytes(path, MAX_SOURCE_BYTES)
        require(body == item["text"].encode("utf-8"), "source bytes differ from capsule")
        require(stat.S_IMODE(path.stat().st_mode) == int(item["mode"][-3:], 8),
                "source executable mode differs from capsule")
    return True


def restore_capsule(data, destination):
    validate_capsule(data)
    require(os.name == "posix", "exact executable-mode restoration requires POSIX support")
    destination = Path(os.path.abspath(destination))
    frames.no_symlinks(destination)
    require(destination.parent.is_dir(), "restore parent must already exist")
    require(not destination.exists(), "restore destination must not exist")
    destination.mkdir(mode=0o700)
    try:
        for item in data["files"]:
            path = destination.joinpath(*frames.artifact_path(item["path"]).parts)
            frames.no_symlinks(path)
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            frames.no_symlinks(path)
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
            with os.fdopen(os.open(path, flags, 0o600), "wb") as handle:
                handle.write(item["text"].encode("utf-8"))
                handle.flush()
                os.fchmod(handle.fileno(), int(item["mode"][-3:], 8))
        _compare_files(data, destination)
    except BaseException:
        shutil.rmtree(destination)
        raise
    return destination


def _round_trip(data, root):
    destination = root / (".capability-replay-" + uuid.uuid4().hex)
    restored = restore_capsule(data, destination)
    try:
        return _compare_files(data, restored)
    finally:
        shutil.rmtree(restored)


def _repo_label(value):
    contracts.text(value, "relative source checkout", 512)
    require(not value.startswith("/") and "\\" not in value and ":" not in value,
            "source checkout must be relative, never an absolute local label")
    require(value == "." or all(part not in {"", "."} for part in value.split("/")),
            "source checkout label must be normalized")
    return value


def _file(root, relative):
    return root.joinpath(*frames.artifact_path(relative).parts)


def _load(args):
    root = frames.root_path(args.root)
    manifest_path = _file(root, args.manifest)
    manifest, revision = contracts.load_manifest(manifest_path, root)
    declared = {item["path"]: item for item in manifest["artifacts"]}
    require(set(IMPLEMENTATION) <= set(declared), "manifest must pin the verifier and its three local helpers")
    for name, executing in IMPLEMENTATION.items():
        require(frames.digest(frames.read_bytes(executing, contracts.MAX_JSON_BYTES)) == declared[name]["sha256"],
                "executing packaging code differs from the pinned capability")
    repo = frames.root_path(root / _repo_label(args.repo))
    return root, repo, manifest_path, manifest, revision


def _paths(args, root, repo, manifest, capsule=None, new=False):
    output, report = _file(root, args.capsule), _file(root, args.report)
    protected = [_file(root, args.manifest), *[_file(root, item["path"]) for item in manifest["artifacts"]]]
    if capsule:
        protected.extend(repo / item["path"] for item in capsule["files"])
    for path in (output, report):
        require(path.suffix == ".json", "capsule and report outputs must be JSON paths")
        frames.no_symlinks(path)
        require(all(path != source and path not in source.parents and source not in path.parents
                    for source in protected), "output overlaps source or manifest")
        if new:
            require(not path.exists(), "qualification outputs must be new files")
            _not_committed_output(path, repo, capsule)
    require(output != report and output not in report.parents and report not in output.parents,
            "capsule and report paths overlap")
    return output, report


def _not_committed_output(path, repo, capsule):
    if capsule is None:
        return
    try:
        relative = path.relative_to(repo).as_posix()
    except ValueError:
        return
    tracked = git_source._git(
        repo, "ls-tree", "-r", "-z", capsule["origin"]["commit"], "--", relative,
    )
    require(not tracked, "output would replace committed source, including a deleted working file")


def _new_json(path, value):
    body = contracts.json_bytes(value)
    require(len(body) <= contracts.MAX_JSON_BYTES, "JSON output exceeds 8 MiB")
    frames.no_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frames.immutable_write(path, body)
    return body


def _read_canonical(path):
    raw = frames.read_bytes(path, contracts.MAX_JSON_BYTES)
    data = contracts.load_json(path)
    require(raw == contracts.json_bytes(data), "expected unchanged canonical JSON bytes")
    return data, raw


def _source_matches(data, repo):
    origin = data["origin"]
    current = pack_sources(repo, origin["commit"], origin["repository"],
                           [item["path"] for item in data["files"]])
    require(current == data, "capsule does not match the selected committed source")
    return True


def _stable(args, root, repo, manifest, revision, data, output, raw):
    after, after_revision = contracts.load_manifest(_file(root, args.manifest), root)
    require(after == manifest and after_revision == revision, "capability manifest or artifacts changed")
    require(frames.read_bytes(output, contracts.MAX_JSON_BYTES) == raw, "capsule changed during checks")
    return _source_matches(data, repo)


def _replay_argv(args):
    return contracts.source_replay_argv(
        ENTRYPOINT, args.manifest, _repo_label(args.repo), args.capsule, args.report,
    )


def _checks(manifest, root, allowed):
    require(allowed, "explicit --allow-checks is required")
    require("process.execute" in manifest["contract"]["permissions"], "process.execute permission is required")
    checks = manifest["checks"]
    for check in checks:
        frames.check_argv(check["argv"])
        require(Path(check["argv"][0]).name.lower() not in
                {"sh", "bash", "zsh", "dash", "fish", "cmd", "cmd.exe", "powershell", "pwsh"},
                "direct shell checks are forbidden")
    return [frames.run_check(check["argv"], root, check["timeout_seconds"]) for check in checks]


def _integrity(report):
    return frames.digest(contracts.json_bytes({key: value for key, value in report.items()
                                               if key != "integrity_sha256"}))


def qualify(args):
    root, repo, _, manifest, revision = _load(args)
    workflow = frames.label(args.workflow)
    data = pack_sources(repo, args.ref, args.repository, args.path)
    output, report_path = _paths(args, root, repo, manifest, data, new=True)
    raw = _new_json(output, data)
    report = {
        "schema": contracts.QUALIFICATION_SCHEMA,
        "capability": {"id": manifest["id"], "manifest_sha256": revision},
        "context": {**data["origin"], "workflow": workflow},
        "capsule": {"sha256": frames.digest(raw), "bytes": len(raw)},
        "outcome": "failed",
        "gates": {"source_matches": False, "round_trip": False, "artifacts_stable": False},
        "checks": [], "replay_argv": _replay_argv(args), "limitations": list(LIMITATIONS),
    }
    failure = False
    try:
        report["gates"]["source_matches"] = _source_matches(data, repo)
        report["gates"]["round_trip"] = _round_trip(data, root)
        report["checks"] = _checks(manifest, root, args.allow_checks)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        failure = True
        report["limitations"].append(f"Qualification refused or failed: {type(exc).__name__}.")
    try:
        report["gates"]["artifacts_stable"] = _stable(
            args, root, repo, manifest, revision, data, output, raw,
        )
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        failure = True
        report["limitations"].append(f"Input stability check refused or failed: {type(exc).__name__}.")
    if (not failure and all(report["gates"].values()) and report["checks"]
            and all(frames.check_passed(check) for check in report["checks"])):
        report["outcome"] = "passed"
    report["integrity_sha256"] = _integrity(report)
    _new_json(report_path, report)
    return report


def _validate_report(report, args, manifest, revision, data, raw):
    require(set(report) == {"schema", "capability", "context", "capsule", "outcome", "gates",
                           "checks", "replay_argv", "limitations", "integrity_sha256"},
            "invalid qualification report fields")
    require(report["integrity_sha256"] == _integrity(report), "qualification report integrity mismatch")
    require(report["schema"] == contracts.QUALIFICATION_SCHEMA and report["outcome"] == "passed",
            "qualification did not pass")
    require(report["capability"] == {"id": manifest["id"], "manifest_sha256": revision},
            "qualification manifest binding mismatch")
    require(isinstance(report["context"], dict) and set(report["context"]) ==
            {"repository", "commit", "tree", "workflow"}, "invalid qualification context")
    frames.label(report["context"]["workflow"])
    require({key: report["context"][key] for key in data["origin"]} == data["origin"],
            "qualification source context mismatch")
    require(report["capsule"] == {"sha256": frames.digest(raw), "bytes": len(raw)},
            "qualification capsule fingerprint mismatch")
    require(report["gates"] == {"source_matches": True, "round_trip": True, "artifacts_stable": True}
            and all(type(value) is bool for value in report["gates"].values()),
            "qualification gates did not pass")
    require(report["replay_argv"] == _replay_argv(args), "qualification replay argv mismatch")
    require(report["limitations"] == LIMITATIONS, "qualification limitations were changed")
    checks = report["checks"]
    require(isinstance(checks, list) and len(checks) == len(manifest["checks"]), "missing qualification checks")
    expected_fields = {
        "argv", "exit_code", "timed_out", "launch_error", "capture_complete", "timeout_seconds",
        "duration_ms", "stdout_sha256", "stdout_bytes", "stderr_sha256", "stderr_bytes",
    }
    for observed, declared in zip(checks, manifest["checks"]):
        require(isinstance(observed, dict) and set(observed) == expected_fields, "invalid check observation")
        require(observed["argv"] == declared["argv"]
                and type(observed["timeout_seconds"]) is int
                and observed["timeout_seconds"] == declared["timeout_seconds"], "check command binding mismatch")
        require(type(observed["exit_code"]) is int and observed["exit_code"] == 0
                and observed["timed_out"] is False and observed["capture_complete"] is True
                and observed["launch_error"] is None, "recorded check failed")
        for key in ("duration_ms", "stdout_bytes", "stderr_bytes"):
            require(type(observed[key]) is int and observed[key] >= 0, "invalid check measurement")
        for key in ("stdout_sha256", "stderr_sha256"):
            contracts.sha256(observed[key])


def verify(args):
    require(args.replay and args.allow_checks, "verification requires --replay --allow-checks")
    root, repo, _, manifest, revision = _load(args)
    output, report_path = _paths(args, root, repo, manifest)
    data, raw = _read_canonical(output)
    validate_capsule(data)
    _paths(args, root, repo, manifest, data)
    report, report_raw = _read_canonical(report_path)
    _validate_report(report, args, manifest, revision, data, raw)
    _source_matches(data, repo)
    _round_trip(data, root)
    checks = _checks(manifest, root, args.allow_checks)
    _stable(args, root, repo, manifest, revision, data, output, raw)
    require(frames.read_bytes(report_path, contracts.MAX_JSON_BYTES) == report_raw,
            "qualification report changed during replay")
    require(checks and all(frames.check_passed(check) for check in checks), "replayed checks failed")
    return {"outcome": "passed", "replayed": True, "checks": checks}


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    pack = commands.add_parser("pack")
    for name in ("repo", "ref", "repository", "output"):
        pack.add_argument("--" + name, required=True)
    pack.add_argument("--path", action="append", required=True)
    restore = commands.add_parser("restore")
    restore.add_argument("--capsule", required=True)
    restore.add_argument("--destination", required=True)
    for name in ("qualify", "verify"):
        command = commands.add_parser(name)
        for field in ("root", "manifest", "repo", "capsule", "report"):
            command.add_argument("--" + field, required=True)
        command.add_argument("--allow-checks", action="store_true")
        if name == "qualify":
            for field in ("ref", "repository", "workflow"):
                command.add_argument("--" + field, required=True)
            command.add_argument("--path", action="append", required=True)
        else:
            command.add_argument("--replay", action="store_true")
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "pack":
            data = pack_sources(args.repo, args.ref, args.repository, args.path)
            destination = _file(frames.root_path("."), args.output)
            _not_committed_output(destination, frames.root_path(args.repo), data)
            _new_json(destination, data)
            result = {"files": data["totals"]["files"], "bytes": data["totals"]["bytes"]}
        elif args.command == "restore":
            data = contracts.load_json(Path(args.capsule))
            restore_capsule(data, args.destination)
            result = {"restored_files": data["totals"]["files"]}
        else:
            result = qualify(args) if args.command == "qualify" else verify(args)
        print(contracts.json_bytes(
            {"outcome": result["outcome"]} if args.command == "qualify" else result,
        ).decode("utf-8").rstrip())
        return 1 if result.get("outcome") == "failed" else 0
    except Exception as exc:
        message = str(exc) if isinstance(exc, (contracts.ContractError, frames.EvidenceError,
                                               git_source.CatalogError)) else type(exc).__name__
        print("capability_package: " + message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
