#!/usr/bin/env python3
"""Rebuild the offline catalog, RAPP chain, index and append-only content store."""

import hashlib
import json
from pathlib import Path

import rapp


ROOT = Path(__file__).resolve().parent
META = "io.modelcontextprotocol.registry/publisher-provided"


def load(path):
    return rapp._strict_json(path.read_bytes())


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode()


def write(relative, content, immutable=False):
    path = ROOT / relative
    if not path.resolve().is_relative_to(ROOT) or path.is_symlink():
        raise ValueError(f"Output escapes the data folder: {relative}")
    if path.exists():
        if path.read_bytes() == content:
            return
        if immutable:
            raise ValueError(f"Refusing to overwrite a published blob: {relative}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def build():
    manifest = load(ROOT / "manifest.json")
    paths = sorted((ROOT / "servers").glob("*.json"))
    if not paths:
        raise ValueError("No server inputs found")
    servers = sorted((load(path) for path in paths), key=lambda server: server["name"])
    names = [server["name"] for server in servers]
    if len(set(names)) != len(names):
        raise ValueError("Duplicate canonical server names")
    for server in servers:
        name = server["name"]
        if not isinstance(name, str) or len(name.split("/")) != 2 or any(
            part in ("", ".", "..") for part in name.split("/")
        ) or "\\" in name:
            raise ValueError(f"Unsafe server name: {name!r}")
        if not server.get("packages") and not server.get("remotes"):
            raise ValueError(f"No installation transport for {name}")
        if not server["_meta"][META]["tools"]:
            raise ValueError(f"No discovery tools for {name}")

    frames = []
    head = None
    for seq, server in enumerate(servers):
        frame = rapp.build_frame(
            kind=manifest["kind"],
            stream_id=manifest["stream_id"],
            seq=seq,
            utc=manifest["generated"],
            payload=server,
            prev=head["payload_hash"] if head else None,
        )
        ok, step, reason = rapp.verify_frame(
            frame, head=head, stream_id_of_record=manifest["stream_id"]
        )
        if not ok:
            raise ValueError(f"Frame {seq} failed verification at {step}: {reason}")
        frames.append(frame)
        head = frame

    head_pointer = {"seq": head["seq"], "frame_hash": head["frame_hash"]}
    categories = sorted({server["_meta"][META]["category"] for server in servers})
    summary = {
        "servers": len(servers),
        "tools": sum(len(server["_meta"][META]["tools"]) for server in servers),
        "categories": len(categories),
    }
    outputs = {
        "api/v1/servers.json": encoded({"schema": "mcp-registry-servers/1.0", "servers": servers}),
        "chain.jsonl": "".join(rapp.canonical(frame) + "\n" for frame in frames).encode(),
        "orient.json": encoded({
            "schema": "rapp/1",
            "stream_id": manifest["stream_id"],
            "chain": "chain.jsonl",
            "registered_kinds": [manifest["kind"]],
            "head": head_pointer,
        }),
        "api/v1/status.json": encoded({
            "schema": "mcp-registry-status/1.0",
            "generated": manifest["generated"],
            "summary": summary,
            "head": head_pointer,
            "status": "catalog-built",
            "description": "Local catalog integrity, not remote server availability.",
        }),
        "api/v1/badge.json": encoded({
            "schemaVersion": 1, "label": "MCP servers",
            "message": str(len(servers)), "color": "blue",
        }),
        ".nojekyll": b"",
        "llms.txt": (
            "# MCP Registry\n\n"
            "Public MCP server discovery; a read-only, offline-buildable catalog.\n"
            f"Pages base: {manifest['pages_base']}\n"
            f"Raw fallback base: {manifest['raw_base']}\n"
            "Data folder: data/mcp-registry/\n"
            "Catalog: api/v1/servers.json (complete MCP server entries)\n"
            "Index: registry.json (SHA-256 first 12 hex and immutable versions)\n"
            "Chain: chain.jsonl (rapp/1); discovery head: orient.json\n"
            "Status: api/v1/status.json; badge: api/v1/badge.json\n"
            "Inputs: manifest.json and servers/*.json\n"
            "Build offline: python3 -B data/mcp-registry/build.py\n"
            "Agent: agents/mcp_registry.py; perform(tool=...) returns exact tool matches.\n"
            "Tools are curated discovery subsets; consult upstream for the full inventory.\n"
            "No installation or remote execution occurs during discovery.\n"
        ).encode(),
    }
    for relative, content in outputs.items():
        write(relative, content)

    indexed = {server["name"]: path.relative_to(ROOT).as_posix()
               for path in paths for server in [load(path)]}
    indexed.update({
        "catalog": "api/v1/servers.json",
        "chain": "chain.jsonl",
        "orient": "orient.json",
        "status": "api/v1/status.json",
        "badge": "api/v1/badge.json",
        "manifest": "manifest.json",
        "llms": "llms.txt",
    })
    entries = []
    for name, relative in sorted(indexed.items()):
        source = ROOT / relative
        content = source.read_bytes()
        sha8 = hashlib.sha256(content).hexdigest()[:12]
        write(f"versions/{name}/{sha8}{source.suffix}", content, immutable=True)
        entries.append({"name": name, "path": relative, "sha8": sha8})
    write("registry.json", encoded({
        "schema": "rapp-static-api/1.1",
        "generated": manifest["generated"],
        "pages_base": manifest["pages_base"],
        "raw_base": manifest["raw_base"],
        "summary": summary,
        "entries": entries,
    }))


if __name__ == "__main__":
    build()
