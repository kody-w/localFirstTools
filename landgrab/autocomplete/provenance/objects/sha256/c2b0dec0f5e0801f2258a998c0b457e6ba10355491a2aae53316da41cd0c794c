#!/usr/bin/env python3
"""Record explicit worktree evidence using a byte-pinned, external RAPP/1 reference.

No scheduler, shell, signing, network, or dependency installation. Run --help for
the operator CLI. Unsigned integrity receipts are not proof of correctness,
authorship, trusted time, priority, or legal ownership.
"""

import argparse
import builtins
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import signal
import stat
import subprocess
import sys
import time
import types
import uuid


PIN_PATH = Path(__file__).resolve().parents[1] / "landgrab/autocomplete/rapp-reference.json"
EVIDENCE_SCHEMA = "localfirst-autocomplete-evidence/v1"
RECORD_SCHEMA = "localfirst-autocomplete-record/v1"
MAX_PAYLOAD_BYTES = 1024 * 1024
MAX_ARTIFACT_BYTES = 8 * 1024 * 1024
MAX_TOTAL_ARTIFACT_BYTES = 32 * 1024 * 1024
MAX_ARTIFACTS, MAX_CHECKS, MAX_REFERENCES, MAX_FRAMES = 64, 8, 32, 10000
LABEL = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
HEX64 = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
FRAME_NAME = re.compile(r"(?:0|[1-9][0-9]*)\.json")
PHASES = ("plan", "implementation", "review", "integration")
SOURCE_SUFFIXES = {
    ".py", ".html", ".css", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".json", ".jsonl", ".toml", ".yaml", ".yml", ".md", ".txt", ".rs",
    ".sh", ".svg", ".csv", ".lock", ".xml", ".sql", ".go", ".c", ".h",
}
PRIVATE_PART = re.compile(
    r"(?:^|[._-])(?:secrets?|credentials?|passwords?|tokens?)(?:$|[._-])",
    re.IGNORECASE,
)
PRIVATE_TEXT = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})|"
    r"(?i:\b(?:password|passwd|api[-_]?key|access[-_]?token|client[-_]?secret)\s*[:=])|"
    r"(?i:--(?:password|passwd|token|secret|api-key)(?:\b|=))"
)
ABSOLUTE_TEXT = re.compile(r"(?:^|[\s=\"'(])(?:/(?!/)|~[/\\]|[A-Za-z]:[/\\]|\\\\)")
LIMITATIONS = [
    "RAPP/1 verifies integrity and lineage, not whether software is correct, complete, safe, or new.",
    "These unsigned memory.save receipts and keyless UUID-derived identity do not authenticate authorship, key ownership, or registered estate authority.",
    "UTC is the recorder's local clock, not a trusted timestamp. External publication must independently establish a dated public paper trail.",
    "Plans are not implementation evidence. checks_passed means only the recorded commands exited successfully on the explicit before/after-stable artifacts; it is not production acceptance.",
    "Artifacts are working-tree snapshots; base_commit is context, not a claim that those bytes were committed at that SHA.",
    "Commands are trusted local processes, not a sandbox. Before/after comparison cannot detect a transient edit reverted during a check or attest undeclared dependencies.",
    "Only explicitly selected public source files are copied. Path and token guards are not a general secret scanner; review source, summary, and argv before publication.",
    "Unsigned history can be replaced or truncated by a writer. Retain independently published head hashes to detect replacement; no first-invention, patent, priority, or other legal claim is made.",
]


class EvidenceError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def label(value):
    require(isinstance(value, str) and 1 <= len(value) <= 64 and LABEL.fullmatch(value),
            "run and worker labels must be lowercase lclabels of 1-64 characters")
    return value


def public_text(value, limit):
    require(isinstance(value, str) and 0 < len(value) <= limit, "invalid public text length")
    require(not any(ord(c) < 32 for c in value), "public text must not contain control characters")
    require(not ABSOLUTE_TEXT.search(value), "local absolute paths are not public metadata")
    require(not PRIVATE_TEXT.search(value), "secret-oriented text is not public metadata")
    return value


def relative_path(value):
    require(isinstance(value, str) and 0 < len(value) <= 512, "invalid relative path")
    require("\\" not in value and ":" not in value and not any(ord(c) < 32 for c in value),
            "paths must be plain relative POSIX paths")
    parts = value.split("/")
    require(all(p not in ("", ".", "..") for p in parts), "absolute paths and path escapes are forbidden")
    return PurePosixPath(value)


def artifact_path(value):
    path = relative_path(value)
    for part in path.parts:
        lower = part.lower()
        require(
            lower not in {".git", ".ssh", ".aws", ".azure", ".gnupg", ".kube", ".config"}
            and not lower.startswith((".env", "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"))
            and not PRIVATE_PART.search(lower),
            "secrets-oriented or .git artifact paths are forbidden",
        )
    require(path.suffix.lower() in SOURCE_SUFFIXES
            or path.name.lower() in {"license", "notice", "makefile", "dockerfile", "justfile", ".gitignore"},
            "select an explicit public source artifact, not a binary or raw log")
    return path


def no_symlinks(path):
    for part in (*reversed(path.parents), path):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        require(not stat.S_ISLNK(info.st_mode), "symlinks are forbidden")


def root_path(value, create=False):
    path = Path(os.path.abspath(value))
    no_symlinks(path)
    if create:
        path.mkdir(parents=True, exist_ok=True)
    require(path.is_dir(), "directory does not exist")
    no_symlinks(path)
    return path


def directory(path, create=False):
    no_symlinks(path)
    if create:
        path.mkdir(parents=True, exist_ok=True)
    require(path.is_dir(), "expected a real directory")
    no_symlinks(path)


def read_bytes(path, limit):
    no_symlinks(path)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    with os.fdopen(os.open(path, flags), "rb") as handle:
        before = os.fstat(handle.fileno())
        require(stat.S_ISREG(before.st_mode), "expected a regular file")
        require(before.st_size <= limit, "file exceeds byte limit")
        data = handle.read(limit + 1)
        after = os.fstat(handle.fileno())
    require(len(data) <= limit, "file exceeds byte limit")
    require((before.st_size, before.st_mtime_ns) ==
            (after.st_size, after.st_mtime_ns), "file changed during read")
    return data


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON member")
        result[key] = value
    return result


def reject_constant(_):
    raise EvidenceError("non-finite JSON value")


def read_json(path, limit=MAX_PAYLOAD_BYTES + 4096):
    try:
        return json.loads(read_bytes(path, limit), object_pairs_hook=unique_pairs,
                          parse_constant=reject_constant, parse_float=reject_constant)
    except (json.JSONDecodeError, UnicodeError, RecursionError) as exc:
        raise EvidenceError("invalid JSON document") from exc


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


@contextmanager
def exclusive_lock(path, wait_seconds=0):
    no_symlinks(path)
    deadline = time.monotonic() + wait_seconds
    while True:
        try:
            path.mkdir()
            break
        except FileExistsError as exc:
            if time.monotonic() >= deadline:
                raise EvidenceError("busy or stale lock; refusing to steal it or fork history") from exc
            time.sleep(0.01)
    try:
        yield
    finally:
        path.rmdir()


def immutable_write(path, data, deduplicate=False):
    """Publish a complete file with an atomic no-replace link, never a truncation."""
    directory(path.parent)
    staged = path.parent / (".pending-" + uuid.uuid4().hex)
    try:
        with staged.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(staged, path)
        except FileExistsError:
            require(deduplicate, "immutable file collision; refusing overwrite")
            require(read_bytes(path, MAX_ARTIFACT_BYTES) == data,
                    "content-addressed object collision or corruption")
    finally:
        staged.unlink(missing_ok=True)
    if os.name == "posix":
        descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


class Reference:
    def __init__(self, path):
        pin = read_json(PIN_PATH)
        require(pin.get("schema") == "localfirst-autocomplete-rapp-reference/v1",
                "invalid reference pin schema")
        require(set(pin.get("files", {})) == {"rapp.py", "rapp_check.py", "SPEC.md"},
                "reference pin must enumerate every local imported helper")
        require(pin["files"]["SPEC.md"] == pin["normative_sha256"], "normative identity mismatch")
        require(isinstance(pin.get("commit"), str) and COMMIT.fullmatch(pin["commit"]),
                "invalid source commit pin")
        for key in ("frame_hash", "payload_hash", "normative_sha256"):
            require(isinstance(pin.get(key), str) and HEX64.fullmatch(pin[key]), "invalid source hash pin")
        source = root_path(path)
        verified = {}
        for name, expected in pin["files"].items():
            raw = read_bytes(source / name, MAX_PAYLOAD_BYTES)
            require(digest(raw) == expected, "pinned-reference mismatch: " + name)
            verified[name] = raw
        self.identity = {key: pin[key] for key in (
            "commit", "revision", "sequence", "frame_hash", "payload_hash", "normative_sha256"
        )}
        self.rapp = types.ModuleType("rapp")
        # Execute the exact verified bytes, not a second filesystem read or a cached .pyc.
        exec(compile(verified["rapp.py"], "<pinned rapp.py>", "exec"), self.rapp.__dict__)
        self.checker = types.ModuleType("rapp_check")

        def pinned_import(name, *args, **kwargs):
            return self.rapp if name == "rapp" else builtins.__import__(name, *args, **kwargs)

        self.checker.__dict__["__builtins__"] = {**vars(builtins), "__import__": pinned_import}
        exec(compile(verified["rapp_check.py"], "<pinned rapp_check.py>", "exec"),
             self.checker.__dict__)


def load_identity(store, reference):
    value = read_json(store / "rappid.json")
    require(isinstance(value, dict) and set(value) ==
            {"schema", "rappid", "created_utc", "identity_kind", "reference"}, "malformed identity")
    require(value["schema"] == "rapp/1" and reference.rapp.rappid_valid(value["rappid"]),
            "malformed RAPP identity; refusing to replace it")
    require(value["identity_kind"] == "keyless-uuid" and value["reference"] == reference.identity,
            "identity kind or source pin mismatch")
    require(reference.rapp.utc_valid(value["created_utc"]), "invalid identity UTC")
    parts = reference.rapp.rappid_parts(value["rappid"])
    require(parts["hash"] != digest((parts["owner"] + "/" + parts["slug"]).encode()),
            "name-hashed identities are forbidden")
    return value


def init_store(store, owner, slug, reference):
    store = root_path(store, create=True)
    with exclusive_lock(store / ".init.lock"):
        if (store / "rappid.json").exists():
            identity = load_identity(store, reference)
            parts = reference.rapp.rappid_parts(identity["rappid"])
            require((parts["owner"], parts["slug"]) == (owner, slug), "stored identity owner/slug mismatch")
            return {"status": "reused", **identity}
        require({p.name for p in store.iterdir()} == {".init.lock"},
                "nonempty store has no identity; refusing to mint over existing state")
        rappid = reference.rapp.mint_rappid(owner, slug)
        directory(store / "runs", create=True)
        directory(store / "objects" / "sha256", create=True)
        identity = {"schema": "rapp/1", "rappid": rappid, "created_utc": utc_now(),
                    "identity_kind": "keyless-uuid", "reference": reference.identity}
        immutable_write(store / "rappid.json", json_bytes(identity))
        return {"status": "initialized", **identity}


def stream_id(rappid, run_id, worker):
    # This is a directory-to-instance binding, not a name-derived RAPPID mint.
    instance = digest((label(run_id) + "/" + label(worker)).encode("ascii"))
    return rappid + ":" + instance


def frame_location(value):
    path = relative_path(value)
    parts = path.parts
    require(len(parts) == 5 and parts[0] == "runs" and parts[3] == "frames"
            and FRAME_NAME.fullmatch(parts[4]), "parent must name a numeric frame inside this store")
    label(parts[1])
    label(parts[2])
    return parts[1], parts[2]


def check_argv(argv):
    require(isinstance(argv, list) and 1 <= len(argv) <= 64, "check must be a nonempty JSON argv array")
    for arg in argv:
        public_text(arg, 2048)
    require(sum(len(arg) for arg in argv) <= 8192, "check argv exceeds size limit")
    require(not argv[0].startswith("-"), "invalid check executable")
    return argv


def check_passed(check):
    return check["exit_code"] == 0 and not check["timed_out"] and check["capture_complete"] \
        and check["launch_error"] is None


def outcome(checks, changed_artifacts, base_commit_unchanged):
    if changed_artifacts or not base_commit_unchanged:
        return "inputs_changed"
    if not checks:
        return "recorded_unchecked"
    return "checks_passed" if all(check_passed(check) for check in checks) else "checks_failed"


def run_check(argv, repo, timeout):
    require(os.name == "posix", "bounded check execution currently requires POSIX process groups")
    start = time.monotonic()
    hashes = {"stdout": hashlib.sha256(), "stderr": hashlib.sha256()}
    sizes = {"stdout": 0, "stderr": 0}
    result = {"argv": argv, "exit_code": None, "timed_out": False, "launch_error": None,
              "capture_complete": True, "timeout_seconds": timeout}
    try:
        process = subprocess.Popen(argv, cwd=repo, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=False, start_new_session=True)
    except OSError as exc:
        result["launch_error"] = type(exc).__name__
    else:
        with selectors.DefaultSelector() as selector:
            for name, pipe in (("stdout", process.stdout), ("stderr", process.stderr)):
                os.set_blocking(pipe.fileno(), False)
                selector.register(pipe, selectors.EVENT_READ, name)
            deadline = start + timeout
            try:
                while selector.get_map() or process.poll() is None:
                    if time.monotonic() >= deadline:
                        if result["timed_out"]:
                            result["capture_complete"] = not selector.get_map()
                            break
                        result["timed_out"] = True
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        deadline = time.monotonic() + 1
                    for key, _ in selector.select(0.05):
                        chunk = os.read(key.fileobj.fileno(), 65536)
                        if chunk:
                            hashes[key.data].update(chunk)
                            sizes[key.data] += len(chunk)
                        else:
                            selector.unregister(key.fileobj)
                result["exit_code"] = process.wait(timeout=2)
            finally:
                # Only this command's newly created process group is touched.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.stdout.close()
                process.stderr.close()
                if process.poll() is None:
                    process.wait(timeout=2)
    result["duration_ms"] = int((time.monotonic() - start) * 1000)
    for name in ("stdout", "stderr"):
        result[name + "_sha256"] = hashes[name].hexdigest()
        result[name + "_bytes"] = sizes[name]
    return result


def repo_commit(repo):
    environment = {key: value for key, value in os.environ.items()
                   if key not in {"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE"}}
    result = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-prefix", "HEAD"],
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False, timeout=10, env=environment)
    lines = result.stdout.decode("ascii", errors="replace").splitlines()
    require(result.returncode == 0 and len(lines) == 2 and lines[0] == ""
            and COMMIT.fullmatch(lines[1]), "--repo must be the root of a Git worktree with a commit")
    return lines[1]


def read_artifacts(repo, paths):
    require(len(paths) <= MAX_ARTIFACTS and len(set(paths)) == len(paths),
            "too many or duplicate artifacts")
    artifacts, blobs, total = [], {}, 0
    for name in paths:
        path = artifact_path(name)
        data = read_bytes(repo / path, MAX_ARTIFACT_BYTES)
        require(not PRIVATE_TEXT.search(data.decode("utf-8")),
                "artifact contains a secret-shaped value; refusing public copy")
        sha = digest(data)
        total += len(data)
        require(total <= MAX_TOTAL_ARTIFACT_BYTES, "artifact batch exceeds byte limit")
        artifacts.append({"path": name, "sha256": sha, "bytes": len(data)})
        blobs[sha] = data
    return artifacts, blobs


def valid_uint(value, maximum=2**53 - 1):
    return type(value) is int and 0 <= value <= maximum


def validate_payload(payload, reference, run_id, worker):
    require(isinstance(payload, dict) and set(payload) == {
        "schema", "run_id", "worker", "phase", "summary", "outcome", "repository", "reference",
        "artifacts", "checks", "references", "changed_artifacts", "base_commit_unchanged",
    }, "invalid evidence payload shape")
    require(payload["schema"] == RECORD_SCHEMA and payload["run_id"] == run_id
            and payload["worker"] == worker and payload["phase"] in PHASES, "payload/stream binding mismatch")
    public_text(payload["summary"], 2048)
    require(payload["reference"] == reference.identity, "frame reference pin mismatch")
    repository = payload["repository"]
    require(isinstance(repository, dict) and set(repository) == {"base_commit", "artifact_source"}
            and isinstance(repository["base_commit"], str) and COMMIT.fullmatch(repository["base_commit"])
            and repository["artifact_source"] == "working-tree", "invalid working-tree provenance")
    artifacts = payload["artifacts"]
    require(isinstance(artifacts, list) and len(artifacts) <= MAX_ARTIFACTS, "invalid artifact count")
    require(artifacts or payload["phase"] == "plan", "non-plan evidence must include source artifacts")
    paths = set()
    for item in artifacts:
        require(isinstance(item, dict) and set(item) == {"path", "sha256", "bytes"}, "invalid artifact")
        artifact_path(item["path"])
        require(item["path"] not in paths, "duplicate artifact path")
        paths.add(item["path"])
        require(isinstance(item["sha256"], str) and HEX64.fullmatch(item["sha256"])
                and valid_uint(item["bytes"], MAX_ARTIFACT_BYTES), "invalid artifact digest/size")
    require(sum(item["bytes"] for item in artifacts) <= MAX_TOTAL_ARTIFACT_BYTES,
            "artifact batch exceeds byte limit")
    checks = payload["checks"]
    require(isinstance(checks, list) and len(checks) <= MAX_CHECKS, "invalid check count")
    for check in checks:
        require(isinstance(check, dict) and set(check) == {
            "argv", "exit_code", "timed_out", "launch_error", "capture_complete",
            "timeout_seconds", "duration_ms", "stdout_sha256", "stdout_bytes", "stderr_sha256", "stderr_bytes",
        }, "invalid check record")
        check_argv(check["argv"])
        require(check["exit_code"] is None or type(check["exit_code"]) is int, "invalid exit code")
        require(type(check["timed_out"]) is bool and type(check["capture_complete"]) is bool,
                "invalid check status")
        require(check["launch_error"] is None or check["launch_error"] in {
            "FileNotFoundError", "PermissionError", "OSError", "NotADirectoryError", "IsADirectoryError",
            "BlockingIOError", "InterruptedError", "ProcessLookupError",
        }, "invalid launch error")
        require(valid_uint(check["timeout_seconds"], 300) and check["timeout_seconds"] >= 1
                and valid_uint(check["duration_ms"]), "invalid check duration")
        require((check["exit_code"] is None) == (check["launch_error"] is not None),
                "missing actual command exit status")
        for name in ("stdout", "stderr"):
            require(isinstance(check[name + "_sha256"], str) and HEX64.fullmatch(check[name + "_sha256"])
                    and valid_uint(check[name + "_bytes"]), "invalid check output digest/size")
    changed = payload["changed_artifacts"]
    require(isinstance(changed, list) and all(isinstance(p, str) and p in paths for p in changed)
            and len(set(changed)) == len(changed), "invalid changed-artifact report")
    require(type(payload["base_commit_unchanged"]) is bool, "invalid baseline stability report")
    require(payload["outcome"] == outcome(checks, changed, payload["base_commit_unchanged"]),
            "outcome does not follow actual checks and input stability")
    references = payload["references"]
    require(isinstance(references, list) and len(references) <= MAX_REFERENCES, "invalid reference count")
    seen = set()
    for item in references:
        require(isinstance(item, dict) and set(item) ==
                {"type", "relation", "path", "stream_id", "seq", "payload_hash", "frame_hash"},
                "invalid typed frame reference")
        require(item["type"] == "rapp/1-frame-reference" and item["relation"] == "context",
                "unsupported reference relation")
        require(isinstance(item["stream_id"], str) and valid_uint(item["seq"])
                and all(isinstance(item[key], str) and HEX64.fullmatch(item[key])
                        for key in ("payload_hash", "frame_hash")), "invalid frame reference fields")
        frame_location(item["path"])
        require(item["path"] not in seen, "duplicate frame reference")
        seen.add(item["path"])


def read_stream(store, reference, rappid, run_id, worker, allow_busy=False):
    worker_path = store / "runs" / label(run_id) / label(worker)
    if not worker_path.exists():
        no_symlinks(worker_path)
        return {}
    directory(worker_path)
    for entry in worker_path.iterdir():
        no_symlinks(entry)
        require(entry.name in {"frames", ".append.lock"}, "unexpected stream entry")
        if entry.name == ".append.lock":
            require(allow_busy, "busy or stale stream lock; verification requires quiescent writers")
            directory(entry)
    frames_dir = worker_path / "frames"
    if not frames_dir.exists():
        return {}
    directory(frames_dir)
    files = []
    for entry in frames_dir.iterdir():
        no_symlinks(entry)
        if entry.name.startswith(".pending-") and allow_busy and (worker_path / ".append.lock").is_dir():
            continue
        require(FRAME_NAME.fullmatch(entry.name), "unexpected or noncanonical frame filename")
        files.append(entry)
    require(len(files) <= MAX_FRAMES, "stream frame limit exceeded")
    frames, head = {}, None
    expected_stream = stream_id(rappid, run_id, worker)
    for seq, file in enumerate(sorted(files, key=lambda p: int(p.stem))):
        require(int(file.stem) == seq, "missing or noncontiguous frame filename")
        frame = read_json(file)
        require(isinstance(frame, dict), "frame is not an object")
        require(frame.get("kind") == "memory.save" and frame.get("stream_id") == expected_stream
                and frame.get("sig") is None and frame.get("prev_wave") is None,
                "registered memory.save kind or memory stream binding mismatch")
        require(isinstance(frame.get("payload"), dict), "payload is not an object")
        require(len(reference.rapp.canonical(frame["payload"]).encode("utf-8")) <= MAX_PAYLOAD_BYTES,
                "payload exceeds 1 MiB")
        ok, step, reason = reference.rapp.verify_frame(frame, head=head, stream_id_of_record=expected_stream)
        require(ok, "canonical frame rejection at " + str(step) + ": " + reason)
        validate_payload(frame["payload"], reference, run_id, worker)
        frames[file.relative_to(store).as_posix()] = frame
        head = frame
    return frames


def verify_references(frames):
    for path, frame in frames.items():
        for item in frame["payload"]["references"]:
            target = frames.get(item["path"])
            require(target is not None and item["path"] != path, "missing or self-referential frame reference")
            require(all(item[key] == target[key] for key in
                        ("stream_id", "seq", "payload_hash", "frame_hash")), "frame reference mismatch")
            require(target["stream_id"] != frame["stream_id"] or target["seq"] < frame["seq"],
                    "same-stream references must point backwards")


def verify_objects(store, frames):
    objects = {}
    for frame in frames.values():
        for item in frame["payload"]["artifacts"]:
            sha, size = item["sha256"], item["bytes"]
            if sha not in objects:
                data = read_bytes(store / "objects" / "sha256" / sha, MAX_ARTIFACT_BYTES)
                require(digest(data) == sha, "stored artifact SHA-256 mismatch")
                objects[sha] = len(data)
            require(objects[sha] == size, "stored artifact size mismatch")
    return objects


def load_context(store, reference, rappid, run_id, worker, parents):
    frames = read_stream(store, reference, rappid, run_id, worker, allow_busy=True)
    loaded = {(run_id, worker)}
    pending = list(parents) + [
        item["path"] for frame in frames.values() for item in frame["payload"]["references"]
    ]
    while pending:
        path = pending.pop()
        location = frame_location(path)
        if location not in loaded:
            added = read_stream(store, reference, rappid, *location, allow_busy=True)
            loaded.add(location)
            frames.update(added)
            require(len(frames) <= MAX_FRAMES, "context frame limit exceeded")
            pending.extend(item["path"] for frame in added.values()
                           for item in frame["payload"]["references"])
        require(path in frames, "referenced frame does not exist")
    verify_references(frames)
    verify_objects(store, frames)
    return frames


def store_layout(store, allow_publishing=False):
    require(not os.path.lexists(store / ".init.lock"), "busy or stale initialization lock")
    for entry in store.iterdir():
        no_symlinks(entry)
        require(entry.name in {"rappid.json", "runs", "objects", "index.json", ".publication.lock"},
                "unexpected store entry")
        if entry.name == ".publication.lock":
            require(allow_publishing, "busy or stale publication lock; verification requires quiescent writers")
        if entry.name in {"rappid.json", "index.json"}:
            require(entry.is_file(), "store metadata must be regular files")
    directory(store / "runs")
    directory(store / "objects" / "sha256")
    require({p.name for p in (store / "objects").iterdir()} == {"sha256"}, "unexpected object directory")


def require_frame_capacity(store):
    """Count committed frames while holding the cross-worker publication lock."""
    count = 0
    for run in (store / "runs").iterdir():
        label(run.name)
        directory(run)
        for worker in run.iterdir():
            label(worker.name)
            directory(worker)
            frames = worker / "frames"
            if not os.path.lexists(frames):
                continue
            directory(frames)
            for frame in frames.iterdir():
                no_symlinks(frame)
                require(FRAME_NAME.fullmatch(frame.name) and frame.is_file(),
                        "unexpected or unfinished frame entry")
                count += 1
                require(count < MAX_FRAMES, "store frame limit reached; append was not published")


def record(args, reference):
    store, repo = root_path(args.store), root_path(args.repo)
    store_layout(store, allow_publishing=True)
    identity = load_identity(store, reference)
    label(args.run_id)
    label(args.worker)
    public_text(args.summary, 2048)
    require(args.artifact or args.phase == "plan", "non-plan evidence requires --artifact")
    require(len(args.check) <= MAX_CHECKS and len(args.parent) <= MAX_REFERENCES
            and len(set(args.parent)) == len(args.parent), "too many checks or duplicate/too many parents")
    require(1 <= args.check_timeout <= 300, "check timeout must be 1-300 seconds")
    checks_argv = [check_argv(json.loads(value)) for value in args.check]
    require(not checks_argv or os.name == "posix", "checks currently require POSIX process groups")
    base_commit = repo_commit(repo)
    artifacts, blobs = read_artifacts(repo, args.artifact)
    worker_path = store / "runs" / args.run_id / args.worker
    directory(worker_path, create=True)
    with exclusive_lock(worker_path / ".append.lock"):
        directory(worker_path / "frames", create=True)
        context = load_context(store, reference, identity["rappid"], args.run_id, args.worker, args.parent)
        sid = stream_id(identity["rappid"], args.run_id, args.worker)
        own = [frame for frame in context.values() if frame["stream_id"] == sid]
        head = max(own, key=lambda f: f["seq"]) if own else None
        require(head is None or head["seq"] + 1 < MAX_FRAMES, "stream frame limit reached")
        with exclusive_lock(store / ".publication.lock", wait_seconds=5):
            require_frame_capacity(store)
        references = [
            {"type": "rapp/1-frame-reference", "relation": "context", "path": path,
             **{key: context[path][key] for key in ("stream_id", "seq", "payload_hash", "frame_hash")}}
            for path in args.parent
        ]
        directory(store / "objects" / "sha256")
        for sha, data in blobs.items():
            immutable_write(store / "objects" / "sha256" / sha, data, deduplicate=True)
        changed_paths = set()
        same_commit = True

        def observe_inputs():
            nonlocal same_commit
            for artifact in artifacts:
                try:
                    after = read_bytes(repo / artifact["path"], MAX_ARTIFACT_BYTES)
                    stable = digest(after) == artifact["sha256"] and len(after) == artifact["bytes"]
                except (EvidenceError, OSError):
                    stable = False
                if not stable:
                    changed_paths.add(artifact["path"])
            try:
                same_commit = repo_commit(repo) == base_commit and same_commit
            except (EvidenceError, OSError, subprocess.TimeoutExpired):
                same_commit = False

        observe_inputs()
        checks = []
        for argv in checks_argv:
            checks.append(run_check(argv, repo, args.check_timeout))
            observe_inputs()
        changed = [artifact["path"] for artifact in artifacts if artifact["path"] in changed_paths]
        payload = {
            "schema": RECORD_SCHEMA, "run_id": args.run_id, "worker": args.worker, "phase": args.phase,
            "summary": args.summary, "outcome": outcome(checks, changed, same_commit),
            "repository": {"base_commit": base_commit, "artifact_source": "working-tree"},
            "reference": reference.identity, "artifacts": artifacts, "checks": checks,
            "references": references, "changed_artifacts": changed, "base_commit_unchanged": same_commit,
        }
        validate_payload(payload, reference, args.run_id, args.worker)
        require(len(reference.rapp.canonical(payload).encode("utf-8")) <= MAX_PAYLOAD_BYTES,
                "payload exceeds 1 MiB")
        frame = reference.rapp.build_frame("memory.save", sid, head["seq"] + 1 if head else 0,
                                          utc_now(), payload, head["payload_hash"] if head else None)
        ok, step, reason = reference.rapp.verify_frame(frame, head=head, stream_id_of_record=sid)
        require(ok, "canonical frame rejection at " + str(step) + ": " + reason)
        location = worker_path / "frames" / (str(frame["seq"]) + ".json")
        # Checks run in parallel; only capacity admission and atomic publication serialize.
        with exclusive_lock(store / ".publication.lock", wait_seconds=5):
            require_frame_capacity(store)
            immutable_write(location, json_bytes(frame))
        result = {"path": location.relative_to(store).as_posix(), "outcome": payload["outcome"],
                  "stream_id": sid, "seq": frame["seq"], "payload_hash": frame["payload_hash"],
                  "frame_hash": frame["frame_hash"]}
        return result, 1 if payload["outcome"] in {"checks_failed", "inputs_changed"} else 0


def scan_store(store, reference):
    store_layout(store)
    identity = load_identity(store, reference)
    frames = {}
    for run in sorted((store / "runs").iterdir()):
        label(run.name)
        directory(run)
        for worker in sorted(run.iterdir()):
            label(worker.name)
            frames.update(read_stream(store, reference, identity["rappid"], run.name, worker.name))
            require(len(frames) <= MAX_FRAMES, "store frame limit exceeded")
    require(frames, "zero frames: an identity-only or empty store is not implementation evidence")
    verify_references(frames)
    objects = verify_objects(store, frames)
    for path in (store / "objects" / "sha256").iterdir():
        require(HEX64.fullmatch(path.name), "unexpected or unfinished object entry")
        if path.name not in objects:
            require(digest(read_bytes(path, MAX_ARTIFACT_BYTES)) == path.name, "orphan object hash mismatch")
    verdict, findings, evidence = reference.checker.check_repo(str(store))
    scanned = sum(int(match.group(1)) for entry in evidence
                  if (match := re.fullmatch(r"([0-9]+) frames conform to §7 envelope", entry.get("ok", ""))))
    require(verdict == "COMPLIANT" and not findings and scanned == len(frames) and scanned > 0,
            "canonical store checker did not return COMPLIANT with the same positive frame count")
    return identity, frames, objects, scanned


def compare_current(repo, events):
    latest = {}
    for event in events:
        for artifact in event["artifacts"]:
            prior = latest.get(artifact["path"])
            candidate = {**artifact, "event_path": event["path"], "seq": event["seq"]}
            if prior is None or prior["utc"] < event["utc"]:
                latest[artifact["path"]] = {"utc": event["utc"], "streams": {event["stream_id"]: candidate}}
            elif prior["utc"] == event["utc"]:
                previous = prior["streams"].get(event["stream_id"])
                if previous is None or candidate["seq"] > previous["seq"]:
                    prior["streams"][event["stream_id"]] = candidate
    results = []
    for path, candidates in sorted(latest.items()):
        heads = list(candidates["streams"].values())
        artifact = heads[0]
        row = {"path": path, "recorded_sha256": artifact["sha256"], "event_path": artifact["event_path"],
               "current_sha256": None, "matches": False, "error": None}
        if len({head["sha256"] for head in heads}) > 1:
            row["error"] = "ambiguous_local_clock_order"
        else:
            try:
                data = read_bytes(repo / path, MAX_ARTIFACT_BYTES)
                row["current_sha256"] = digest(data)
                row["matches"] = row["current_sha256"] == artifact["sha256"] and len(data) == artifact["bytes"]
            except (EvidenceError, OSError):
                row["error"] = "missing_unreadable_or_unsafe_path"
        results.append(row)
    return {"scope": "latest-per-path-by-local-utc", "matches": all(row["matches"] for row in results),
            "artifacts": results}


def presentation_key(event):
    return event["utc"], event["frame_hash"]


def evidence_index(store, reference, repo=None):
    identity, frames, objects, scanned = scan_store(store, reference)
    events = []
    for path, frame in frames.items():
        payload = frame["payload"]
        events.append({
            **{key: payload[key] for key in ("run_id", "worker", "phase", "outcome", "summary",
                                           "artifacts", "checks", "references", "repository",
                                           "changed_artifacts", "base_commit_unchanged")},
            **{key: frame[key] for key in ("utc", "stream_id", "seq", "payload_hash", "frame_hash")},
            "path": path,
        })
    events.sort(key=presentation_key)
    result = {
        "schema": EVIDENCE_SCHEMA, "generated_at": utc_now(), "rappid": identity["rappid"],
        "reference": reference.identity,
        "counts": {"streams": len({event["stream_id"] for event in events}),
                   "frames": len(events), "artifacts": len(objects)},
        "verification": {"verdict": "COMPLIANT", "canonical_scanned_frames": scanned},
        "runs": [{"run_id": run, "workers": sorted({event["worker"] for event in events if event["run_id"] == run})}
                 for run in sorted({event["run_id"] for event in events})],
        "events": events,
        "claims": {"integrity_verified": True, "authenticated_authorship": False, "trusted_timestamp": False,
                   "correctness_proven": False, "novelty_or_legal_priority_proven": False,
                   "checked_implementation_frames": sum(event["phase"] == "implementation"
                                                        and event["outcome"] == "checks_passed" for event in events),
                   "failed_frames": sum(event["outcome"] in {"checks_failed", "inputs_changed"} for event in events)},
        "limitations": LIMITATIONS,
    }
    if repo is not None:
        result["current_artifacts"] = compare_current(root_path(repo), events)
    return result


def write_index(output, store, value):
    path = Path(os.path.abspath(output))
    no_symlinks(path)
    require(path != store and (not path.is_relative_to(store) or path == store / "index.json"),
            "index may only overwrite index.json inside an evidence store")
    directory(path.parent, create=True)
    staged = path.parent / (".index-" + uuid.uuid4().hex)
    try:
        with staged.open("xb") as handle:
            handle.write(json_bytes(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="command", required=True)
    for command in ("init", "record", "verify", "index"):
        child = sub.add_parser(command)
        child.add_argument("--store", required=True, help="dedicated evidence directory, not a repository root")
        child.add_argument("--rapp-dir", required=True, help="explicit checkout/export of the byte-pinned RAPP reference")
        if command == "init":
            child.add_argument("--owner", required=True)
            child.add_argument("--slug", required=True)
        elif command == "record":
            child.add_argument("--run-id", required=True)
            child.add_argument("--worker", required=True)
            child.add_argument("--repo", required=True)
            child.add_argument("--phase", choices=PHASES, required=True)
            child.add_argument("--summary", required=True, help="public text; never include credentials or local absolute paths")
            child.add_argument("--artifact", action="append", default=[], help="explicit relative public source path")
            child.add_argument("--check", action="append", default=[], help='trusted argv JSON, e.g. ["python3","-m","unittest"]')
            child.add_argument("--check-timeout", type=int, default=60, help="per-command seconds, 1-300; POSIX only")
            child.add_argument("--parent", action="append", default=[], help="store-relative frame path; typed context reference only")
        elif command == "verify":
            child.add_argument("--repo", help="optional separate latest-vs-current artifact comparison")
        elif command == "index":
            child.add_argument("--output", required=True, help="derived JSON summary, outside store or store/index.json")
    return cli


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        reference = Reference(args.rapp_dir)
        code = 0
        if args.command == "init":
            value = init_store(args.store, args.owner, args.slug, reference)
        elif args.command == "record":
            value, code = record(args, reference)
        else:
            store = root_path(args.store)
            value = evidence_index(store, reference, getattr(args, "repo", None))
            if args.command == "index":
                write_index(args.output, store, value)
            elif "current_artifacts" in value and not value["current_artifacts"]["matches"]:
                code = 1
        print(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False))
        return code
    except (EvidenceError, ValueError, TypeError, RecursionError, UnicodeError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        return 2
    except (OSError, subprocess.TimeoutExpired) as exc:
        print("error: filesystem or process operation failed (" + type(exc).__name__ + ")", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
