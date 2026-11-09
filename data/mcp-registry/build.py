#!/usr/bin/env python3
"""Offline materialization: python3 -B data/mcp-registry/build.py."""

import hashlib
import json
from pathlib import Path

import rapp


ROOT = Path(__file__).resolve().parent
META = "io.modelcontextprotocol.registry/publisher-provided"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def write(relative, content, immutable=False):
    path = ROOT / relative
    if ROOT not in path.resolve().parents:
        raise ValueError(f"Output escapes data folder: {relative}")
    if path.exists():
        previous = path.read_bytes()
        if previous == content:
            return
        if immutable:
            raise ValueError(f"Content-address collision: {relative}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def build():
    manifest = read_json(ROOT / "manifest.json")
    if not rapp.rappid_valid(manifest["stream_id"]):
        raise ValueError("Manifest must carry the original minted stream_id")
    if not rapp.utc_valid(manifest["generated"]):
        raise ValueError("Manifest generated must be a RAPP UTC timestamp")
    paths = sorted((ROOT / "servers").glob("*.json"))
    servers = sorted((read_json(path) for path in paths), key=lambda server: server["name"])
    if not servers or len({server["name"] for server in servers}) != len(servers):
        raise ValueError("Catalog must have nonempty, unique canonical server names")

    frames = []
    for seq, server in enumerate(servers):
        frame = rapp.build_frame(
            kind="body.pulse",
            stream_id=manifest["stream_id"],
            seq=seq,
            utc=manifest["generated"],
            payload=server,
            prev=frames[-1]["payload_hash"] if frames else None,
        )
        frames.append(frame)
    head = {"seq": frames[-1]["seq"], "frame_hash": frames[-1]["frame_hash"]}
    write("chain.jsonl", ("\n".join(rapp.canonical(frame) for frame in frames) + "\n").encode("utf-8"))
    write("orient.json", json_bytes({
        "schema": "mcp-registry-orient/1.0",
        "spec": "rapp/1",
        "stream_id": manifest["stream_id"],
        "chain": "chain.jsonl",
        "registered_kinds": ["body.pulse"],
        "head": head,
    }))
    write("api/v1/servers.json", json_bytes({
        "schema": "mcp-registry-servers/1.0",
        "servers": servers,
    }))
    summary = {
        "servers": len(servers),
        "tools": sum(len(server["_meta"][META]["tools"]) for server in servers),
        "categories": len({server["_meta"][META]["category"] for server in servers}),
    }
    write("api/v1/status.json", json_bytes({
        "schema": "mcp-registry-status/1.0",
        "generated": manifest["generated"],
        "summary": summary,
        "head": head,
    }))
    write("api/v1/badge.json", json_bytes({
        "schemaVersion": 1,
        "label": "MCP servers",
        "message": str(len(servers)),
        "color": "blue",
    }))
    write("llms.txt", (
        "# MCP Registry\n\n"
        f"Pages base: {manifest['pages_base']}\n"
        f"Raw fallback base: {manifest['raw_base']}\n"
        "Same-origin catalog: data/mcp-registry/api/v1/servers.json\n"
        "Index: data/mcp-registry/registry.json\n"
        "Chain: data/mcp-registry/chain.jsonl\n"
        "Head: data/mcp-registry/orient.json\n"
        "Each catalog entry uses the official dated MCP server schema.\n"
        "Capabilities are curated, not an exhaustive inventory of every upstream tool.\n"
        "Rebuild offline with python3 -B data/mcp-registry/build.py.\n"
        "manifest.json records the fixed release timestamp and mint-once stream identity.\n"
        "Edit servers/*.json for catalog updates; advance the manifest timestamp for a new release.\n"
        "versions/<name>/<sha8><ext> retains immutable content-addressed historical bytes.\n"
    ).encode("utf-8"))
    write(".nojekyll", b"")

    sources = [(read_json(path)["name"], "servers/" + path.name) for path in paths]
    sources.extend([
        ("mcp-registry/servers", "api/v1/servers.json"),
        ("mcp-registry/chain", "chain.jsonl"),
        ("mcp-registry/orient", "orient.json"),
        ("mcp-registry/status", "api/v1/status.json"),
        ("mcp-registry/badge", "api/v1/badge.json"),
    ])
    entries = []
    for name, relative in sorted(sources):
        source = ROOT / relative
        content = source.read_bytes()
        sha8 = hashlib.sha256(content).hexdigest()[:12]
        write(f"versions/{name}/{sha8}{source.suffix}", content, immutable=True)
        entries.append({"name": name, "path": relative, "sha8": sha8})
    write("registry.json", json_bytes({
        "schema": "rapp-static-api/1.1",
        "generated": manifest["generated"],
        "summary": summary,
        "pages_base": manifest["pages_base"],
        "raw_base": manifest["raw_base"],
        "entries": entries,
    }))


if __name__ == "__main__":
    build()
