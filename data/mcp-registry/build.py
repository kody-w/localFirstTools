#!/usr/bin/env python3
"""Rebuild the local catalog, verified RAPP chain, and append-only static API offline."""

import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
import rapp


ROOT = Path(__file__).resolve().parent
META = "io.modelcontextprotocol.registry/publisher-provided"


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def write(path, data, immutable=False):
    target = ROOT / path
    if not target.resolve().is_relative_to(ROOT):
        raise ValueError(f"Output escapes the data folder: {path}")
    if target.exists():
        current = target.read_bytes()
        if current == data:
            return
        if immutable:
            raise ValueError(f"Content-address collision: {path}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def build():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    reference = hashlib.sha256((ROOT / "rapp.py").read_bytes()).hexdigest()
    if reference != manifest["reference"]["sha256"]:
        raise ValueError("Vendored RAPP reference does not match its pinned hash")
    generated = manifest["generated"]
    if not rapp.utc_valid(generated):
        raise ValueError("Manifest generated timestamp must be a fixed-form UTC timestamp")

    inputs = []
    names = set()
    for path in sorted((ROOT / "servers").glob("*.json")):
        server = json.loads(path.read_text())
        name = server["name"]
        if not re.fullmatch(r"[a-zA-Z0-9.-]+/[a-zA-Z0-9._-]+", name):
            raise ValueError(f"Invalid canonical server name: {name}")
        if any(part in (".", "..") for part in name.split("/")) or name in names:
            raise ValueError(f"Duplicate or unsafe canonical server name: {name}")
        if not server["_meta"][META]["tools"]:
            raise ValueError(f"Server has no discovery tools: {name}")
        names.add(name)
        inputs.append((server, path.relative_to(ROOT).as_posix()))
    inputs.sort(key=lambda item: item[0]["name"])
    if not inputs:
        raise ValueError("No server inputs")

    identity_path = ROOT / "rappid.json"
    if identity_path.exists():
        stream_id = json.loads(identity_path.read_text())["rappid"]
    else:
        stream_id = rapp.mint_rappid("kody-w", "mcp-registry")
        write("rappid.json", json_bytes({"schema": "mcp-registry-identity/1.0", "rappid": stream_id}))
    if not rapp.rappid_valid(stream_id):
        raise ValueError("Stored registry identity is invalid; refusing to re-mint")

    frames = []
    head = None
    for seq, (server, _) in enumerate(inputs):
        frame = rapp.build_frame(
            "body.pulse", stream_id, seq, generated, server,
            None if head is None else head["payload_hash"],
        )
        ok, step, why = rapp.verify_frame(frame, head, stream_id)
        if not ok:
            raise ValueError(f"Chain verification failed at {seq}, step {step}: {why}")
        frames.append(frame)
        head = frame
    write("chain.jsonl", ("\n".join(rapp.canonical(frame) for frame in frames) + "\n").encode())
    write("orient.json", json_bytes({
        "schema": "mcp-registry-orient/1.0",
        "stream_id": stream_id,
        "chain": "chain.jsonl",
        "head": {"seq": head["seq"], "frame_hash": head["frame_hash"]},
    }))
    servers = [server for server, _ in inputs]
    summary = {
        "servers": len(servers),
        "categories": len({server["_meta"][META]["category"] for server in servers}),
        "tools": len({tool["name"] for server in servers for tool in server["_meta"][META]["tools"]}),
    }
    write("api/v1/servers.json", json_bytes({"schema": "mcp-registry-servers/1.0", "servers": servers}))
    write("api/v1/status.json", json_bytes({
        "schema": "mcp-registry-status/1.0",
        "generated": generated,
        "status": "ok",
        "summary": summary,
        "head": {"seq": head["seq"], "frame_hash": head["frame_hash"]},
    }))
    write("api/v1/badge.json", json_bytes({
        "schemaVersion": 1, "label": "MCP servers", "message": str(len(servers)), "color": "blue",
    }))
    indexed = [(server["name"], path, server["repository"]["url"]) for server, path in inputs]
    indexed.extend([
        ("servers", "api/v1/servers.json", None),
        ("status", "api/v1/status.json", None),
        ("badge", "api/v1/badge.json", None),
        ("chain", "chain.jsonl", None),
        ("orient", "orient.json", None),
        ("identity", "rappid.json", None),
        ("manifest", "manifest.json", None),
    ])
    entries = []
    for name, path, source in indexed:
        data = (ROOT / path).read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        version_path = f"versions/{name}/{sha[:12]}{Path(path).suffix}"
        write(version_path, data, immutable=True)
        entry = {"name": name, "path": path, "sha8": sha[:12], "sha256": sha, "version_path": version_path}
        if source:
            entry["source"] = source
        entries.append(entry)
    write("registry.json", json_bytes({
        "schema": "rapp-static-api/1.1",
        "generated": generated,
        "pages_base": manifest["pages_base"],
        "raw_base": manifest["raw_base"],
        "summary": summary,
        "entries": sorted(entries, key=lambda entry: entry["name"]),
    }))
    write("llms.txt", (
        "# LocalFirst Tools MCP Registry\n\n"
        "Public MCP server discovery; no servers are executed by this catalog.\n"
        f"Pages base: {manifest['pages_base']}\n"
        f"Raw fallback: {manifest['raw_base']}\n"
        "API directory: data/mcp-registry/\n"
        "Index: registry.json\nServers: api/v1/servers.json\n"
        "Status: api/v1/status.json\nBadge: api/v1/badge.json\n"
        "Verified chain: chain.jsonl\nHead: orient.json\n"
        "Offline rebuild: python3 data/mcp-registry/build.py\n"
        "Inputs: manifest.json, rappid.json (minted once), servers/*.json\n"
        "Immutable snapshots: versions/<name>/<first-12-sha256-hex><extension>\n"
        "Tool metadata is a reviewed discovery subset, not a live tools/list response.\n"
    ).encode())
    write(".nojekyll", b"")
    print(f"Built {len(servers)} servers; verified head {head['frame_hash']}")


if __name__ == "__main__":
    build()
