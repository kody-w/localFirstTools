#!/usr/bin/env python3
"""Rebuild the Dynamics 365 RAPP/static API surface from its local JSON sources."""

import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timedelta, timezone

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
import rapp

NAME = "dynamics365-frame-machine"
PAGES_BASE = "https://kody-w.github.io/localFirstTools"
RAW_BASE = "https://raw.githubusercontent.com/kody-w/localFirstTools/main"
DATA_PATH = "data/frame-machines/dynamics365"
# Minted once with the pinned rapp.mint_rappid; rebuilding never changes identity.
STREAM_ID = "rappid:@kody-w/dynamics365-frame-machine:bfa2ac03232da545996901f44bc5f56a0147b2bb1d1de31514c64787de28d404"
SOURCES = (
    ("machine", "machine.json"),
    ("overlay", "active-system-data.json"),
    ("liquid", "liquid-dimension.json"),
)


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Source timestamps must include a UTC offset")
    return parsed.astimezone(timezone.utc)


def iso_z(value):
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def write(relative, content, immutable=False):
    target = (ROOT / relative).resolve()
    if ROOT not in target.parents:
        raise ValueError(f"Output path escapes the data folder: {relative}")
    if target.exists():
        if target.read_bytes() == content:
            return
        if immutable:
            raise ValueError(f"Refusing to change an immutable version: {relative}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


def write_json(relative, value):
    content = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    write(relative, (content + "\n").encode("utf-8"))


def build():
    if not rapp.rappid_valid(STREAM_ID):
        raise ValueError("The stored stream identity is not a rappid")
    contents = {name: (ROOT / path).read_bytes() for name, path in SOURCES}
    documents = {name: json.loads(content) for name, content in contents.items()}
    machine, overlay, liquid = (documents[name] for name in ("machine", "overlay", "liquid"))
    if not isinstance(machine["frames"], list) or not machine["frames"]:
        raise ValueError("machine.json must contain frames")
    frame_ids = [frame["id"] for frame in machine["frames"]]
    if len(set(frame_ids)) != len(frame_ids):
        raise ValueError("Machine frame ids must be unique")
    interval_ms = machine["runtime"]["frameIntervalMs"]
    if isinstance(interval_ms, bool) or not isinstance(interval_ms, int) or interval_ms <= 0:
        raise ValueError("frameIntervalMs must be a positive integer")
    start = timestamp(overlay["lastUpdated"])
    generated = iso_z(max(start, timestamp(liquid["lastUpdated"])))
    chain = []
    for seq, frame in enumerate(machine["frames"]):
        payload = dict(frame)
        payload["activeSystemData"] = overlay["frames"][frame["id"]]["activeSystemData"]
        payload["dimensionData"] = liquid["frames"][frame["id"]]["dimensionData"]
        payload["surfaceUpdated"] = {
            "overlay": overlay["lastUpdated"],
            "liquid": liquid["lastUpdated"],
        }
        chain.append(rapp.build_frame(
            kind="body.pulse",
            stream_id=STREAM_ID,
            seq=seq,
            utc=iso_z(start + timedelta(milliseconds=seq * interval_ms)),
            payload=payload,
            prev=chain[-1]["payload_hash"] if chain else None,
        ))
    chain_bytes = "".join(rapp.canonical(frame) + "\n" for frame in chain).encode("utf-8")
    write("chain.jsonl", chain_bytes)
    contents["chain"] = chain_bytes
    head = {key: chain[-1][key] for key in ("seq", "frame_hash", "payload_hash", "utc")}
    write_json("rappid.json", {"schema": "rapp/1", "rappid": STREAM_ID})
    write_json("orient.json", {
        "schema": "rapp/1",
        "generated": generated,
        "stream_id": STREAM_ID,
        "chain": "chain.jsonl",
        "registered_kinds": ["body.pulse"],
        "head": head,
    })

    pages = f"{PAGES_BASE}/{DATA_PATH}"
    raw = f"{RAW_BASE}/{DATA_PATH}"
    entries = []
    for name, path in (*SOURCES, ("chain", "chain.jsonl")):
        content = contents[name]
        digest = hashlib.sha256(content).hexdigest()
        sha8 = digest[:12]
        version_path = f"versions/{name}/{sha8}{Path(path).suffix}"
        write(version_path, content, immutable=True)
        entries.append({
            "name": name,
            "path": path,
            "sha8": sha8,
            "sha256": digest,
            "bytes": len(content),
            "source": f"{pages}/{path}",
            "raw_url": f"{raw}/{path}",
            "version_path": version_path,
            "version_url": f"{pages}/{version_path}",
            "version_raw_url": f"{raw}/{version_path}",
        })
    write_json("registry.json", {
        "schema": "rapp-static-api/1.1",
        "generated": generated,
        "pages_base": PAGES_BASE,
        "raw_base": RAW_BASE,
        "data_path": DATA_PATH,
        "summary": {"name": NAME, "frames": len(chain), "entries": len(entries), "head": head},
        "entries": entries,
    })
    write_json("api/v1/frames.json", {
        "schema": f"{NAME}-frames/1.0",
        "generated": generated,
        "stream_id": STREAM_ID,
        "head": head,
        "frames": chain,
    })
    write_json("api/v1/status.json", {
        "schema": f"{NAME}-status/1.0",
        "generated": generated,
        "status": "ready",
        "frames": len(chain),
        "stream_id": STREAM_ID,
        "head": head,
        "sources": {entry["name"]: entry["sha8"] for entry in entries},
    })
    write_json("api/v1/badge.json", {
        "schema": f"{NAME}-badge/1.0",
        "schemaVersion": 1,
        "label": "Dynamics 365 frames",
        "message": f"{len(chain)} frames / {head['frame_hash'][:8]}",
        "color": "blue",
    })
    lines = [
        "# Dynamics 365 Frame Machine",
        "",
        f"A local simulated CRM with {len(chain)} RAPP/1 frames. As of {generated}.",
        f"Pages base (primary): {PAGES_BASE}",
        f"Raw base (external fallback): {RAW_BASE}",
        "",
        f"Discovery and content hashes: {pages}/registry.json",
        f"Selected chain head: {pages}/orient.json",
        f"Verify the body.pulse chain: {pages}/chain.jsonl",
        f"Frame API: {pages}/api/v1/frames.json",
        f"Status: {pages}/api/v1/status.json",
        f"Shields badge: {pages}/api/v1/badge.json",
        f"Page: {PAGES_BASE}/apps/uncategorized/dynamics365-frame-machine.html",
        f"Local agent: agents/dynamics365_frame_machine.py (stream {STREAM_ID})",
        "",
        "Pin a version and compare SHA-256 with its registry entry before consuming it.",
    ]
    for entry in entries:
        lines.extend([
            f"{entry['name']}: {entry['source']}",
            f"Immutable Pages version: {entry['version_url']}",
            f"Immutable raw fallback: {entry['version_raw_url']}",
        ])
    lines.extend([
        "",
        "Rebuild: python3 build.py from this folder; stdlib only, no network calls.",
        "The source JSON is never modified. Published versions are append-only.",
        "Timestamps come from the source data, not the build clock.",
    ])
    write("llms.txt", ("\n".join(lines) + "\n").encode("utf-8"))
    write(".nojekyll", b"")
    print(f"{NAME}: {len(chain)} frames; head {head['frame_hash'][:8]}")


if __name__ == "__main__":
    build()
