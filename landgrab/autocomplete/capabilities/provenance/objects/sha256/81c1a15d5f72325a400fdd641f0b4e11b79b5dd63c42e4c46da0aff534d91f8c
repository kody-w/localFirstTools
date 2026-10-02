"""Shared, dependency-free contracts for qualified reusable capabilities."""

import json
import os
from pathlib import Path
import re
import uuid

if __package__:
    from .autocomplete_frames import artifact_path, check_argv, digest, no_symlinks, read_bytes, read_json
else:
    from autocomplete_frames import artifact_path, check_argv, digest, no_symlinks, read_bytes, read_json


CAPABILITY_SCHEMA = "localfirst-capability/v1"
CAPSULE_SCHEMA = "localfirst-source-capsule/v1"
QUALIFICATION_SCHEMA = "localfirst-capability-qualification/v1"
REGISTRY_SCHEMA = "localfirst-capability-registry/v1"
PLAN_SCHEMA = "localfirst-capability-plan/v1"
MAX_JSON_BYTES = 8 * 1024 * 1024
MAX_MANIFEST_BYTES = 256 * 1024
PERMISSIONS = {"repository.read", "artifact.write", "process.execute"}
IDENTIFIER = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
HEX64 = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")


class ContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def text(value, label, maximum=4096):
    require(isinstance(value, str) and 0 < len(value) <= maximum, f"invalid {label}")
    require(not any(ord(character) < 32 for character in value), f"control characters in {label}")
    return value


def identifier(value):
    require(isinstance(value, str) and len(value) <= 80 and IDENTIFIER.fullmatch(value),
            "invalid capability identifier")
    return value


def sha256(value):
    require(isinstance(value, str) and HEX64.fullmatch(value), "expected a complete SHA-256")
    return value


def committed_ref(value):
    require(isinstance(value, str) and COMMIT.fullmatch(value), "expected a complete Git commit")
    return value


def script_entrypoint(value):
    artifact_path(value)
    require(not value.startswith("-"), "option-like script entrypoints are forbidden")
    return value


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                       allow_nan=False) + "\n").encode("utf-8")


def load_json(path, limit=MAX_JSON_BYTES):
    value = read_json(Path(path), limit)
    require(isinstance(value, dict), "JSON document must be an object")
    return value


def source_path(root, relative):
    selected = artifact_path(relative)
    base = Path(root).resolve()
    path = base.joinpath(*selected.parts)
    no_symlinks(path)
    require(path.is_file(), f"missing source artifact: {relative}")
    return path


def atomic_json(path, value):
    destination = Path(path).absolute()
    no_symlinks(destination)
    body = json_bytes(value)
    require(len(body) <= MAX_JSON_BYTES, "JSON output exceeds 8 MiB")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.parent / (".capability-" + uuid.uuid4().hex)
    try:
        with temporary.open("xb") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return digest(body)


def validate_source_replay(argv, entrypoint):
    script_entrypoint(entrypoint)
    check_argv(argv)
    require(len(argv) == 15 and argv[:3] == ["python3", entrypoint, "verify"],
            "not a complete source qualification replay")
    require(argv[3:13:2] == ["--root", "--manifest", "--repo", "--capsule", "--report"]
            and argv[4] == "." and argv[13:] == ["--replay", "--allow-checks"],
            "unexpected or missing source replay options")
    values = {"manifest": argv[6], "repo": argv[8], "capsule": argv[10], "report": argv[12]}
    require(all(not value.startswith("-") for value in values.values()),
            "option-like replay values are forbidden")
    for name in ("manifest", "capsule", "report"):
        artifact_path(values[name])
    source = values["repo"]
    require(not source.startswith("/") and "\\" not in source and ":" not in source
            and (source == "." or all(part not in {"", "."} for part in source.split("/"))),
            "source replay checkout must be a normalized relative path")
    return values


def source_replay_argv(entrypoint, manifest, repo, capsule, report):
    argv = [
        "python3", entrypoint, "verify", "--root", ".", "--manifest", manifest,
        "--repo", repo, "--capsule", capsule, "--report", report, "--replay", "--allow-checks",
    ]
    validate_source_replay(argv, entrypoint)
    return argv


def validate_manifest(value):
    required = {
        "schema", "id", "version", "title", "job", "entrypoint", "artifacts",
        "contract", "checks", "failure_cases", "reuses", "visibility",
    }
    require(isinstance(value, dict) and set(value) == required, "invalid capability manifest fields")
    require(value["schema"] == CAPABILITY_SCHEMA, "unsupported capability schema")
    identifier(value["id"])
    require(isinstance(value["version"], str) and
            re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", value["version"]),
            "version must contain three nonnegative integers")
    text(value["title"], "title", 160)
    text(value["job"], "job")
    script_entrypoint(value["entrypoint"])
    require(value["visibility"] in {"private", "public"}, "invalid visibility")
    contract = value["contract"]
    require(isinstance(contract, dict) and set(contract) ==
            {"inputs", "outputs", "permissions", "network"}, "invalid input/output contract")
    for name in ("inputs", "outputs"):
        require(isinstance(contract[name], dict) and contract[name].get("type") == "object",
                f"{name} must describe an object-shaped input/output schema")
    permissions = contract["permissions"]
    require(isinstance(permissions, list) and all(isinstance(item, str) for item in permissions)
            and len(set(permissions)) == len(permissions) and set(permissions) <= PERMISSIONS,
            "unsupported or duplicate capability permissions")
    require(contract["network"] == "none", "this capability profile has no network permission")
    artifacts = value["artifacts"]
    require(isinstance(artifacts, list) and 1 <= len(artifacts) <= 64, "invalid artifact inventory")
    paths = set()
    for artifact in artifacts:
        require(isinstance(artifact, dict) and set(artifact) == {"path", "sha256", "bytes"},
                "invalid artifact record")
        artifact_path(artifact["path"])
        require(artifact["path"] not in paths, "duplicate artifact path")
        paths.add(artifact["path"])
        sha256(artifact["sha256"])
        require(type(artifact["bytes"]) is int and 0 <= artifact["bytes"] <= MAX_JSON_BYTES,
                "invalid artifact byte count")
    require(value["entrypoint"] in paths, "entrypoint must be byte-pinned in artifacts")
    checks = value["checks"]
    require(isinstance(checks, list) and 1 <= len(checks) <= 8, "nonempty bounded checks required")
    names = set()
    for check in checks:
        require(isinstance(check, dict) and set(check) == {"id", "argv", "timeout_seconds"},
                "invalid check record")
        identifier(check["id"])
        require(check["id"] not in names, "duplicate check identifier")
        names.add(check["id"])
        require(isinstance(check["argv"], list) and 1 <= len(check["argv"]) <= 64,
                "check must contain bounded argv")
        for argument in check["argv"]:
            text(argument, "check argument", 2048)
        require(type(check["timeout_seconds"]) is int and 1 <= check["timeout_seconds"] <= 300,
                "check timeout must be 1-300 seconds")
    failures = value["failure_cases"]
    require(isinstance(failures, list) and 1 <= len(failures) <= 128,
            "a capability must identify reproducible failure cases")
    for failure in failures:
        text(failure, "failure case", 512)
    dependencies = value["reuses"]
    require(isinstance(dependencies, list) and len(dependencies) <= 64, "invalid dependencies")
    seen = set()
    for dependency in dependencies:
        require(isinstance(dependency, dict) and set(dependency) == {"id", "manifest_sha256"},
                "dependencies must pin identity and manifest bytes")
        identifier(dependency["id"])
        sha256(dependency["manifest_sha256"])
        require(dependency["id"] != value["id"] and dependency["id"] not in seen,
                "self-dependency or duplicate dependency")
        seen.add(dependency["id"])
    return value


def load_manifest(path, root):
    manifest_path = Path(path).absolute()
    no_symlinks(manifest_path)
    raw = read_bytes(manifest_path, MAX_MANIFEST_BYTES)
    manifest = validate_manifest(load_json(manifest_path, MAX_MANIFEST_BYTES))
    for artifact in manifest["artifacts"]:
        body = read_bytes(source_path(root, artifact["path"]), MAX_JSON_BYTES)
        require(len(body) == artifact["bytes"] and digest(body) == artifact["sha256"],
                f"artifact changed since manifest was pinned: {artifact['path']}")
    return manifest, digest(raw)
