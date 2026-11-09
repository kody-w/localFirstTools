"""Build the local Dynamics 365 RAPP chain and static API (stdlib only)."""

import sys

sys.dont_write_bytecode = True

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import rapp


PAGES = "https://kody-w.github.io/localFirstTools"
RAW = "https://raw.githubusercontent.com/kody-w/localFirstTools"
PREFIX = "data/frame-machines/dynamics365"


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode(
        "utf-8"
    )


def write(relative, content, immutable=False):
    path = ROOT / relative
    if path.exists():
        old = path.read_bytes()
        if old == content:
            return
        if immutable:
            raise ValueError(f"Refusing to mutate immutable version: {relative}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def build():
    machine = read_json("machine.json")
    overlay = read_json("active-system-data.json")
    liquid = read_json("liquid-dimension.json")
    identity_path = ROOT / "rappid.json"
    if identity_path.exists():
        identity = read_json("rappid.json")
        if identity["schema"] != "rapp/1" or not rapp.rappid_valid(identity["rappid"]):
            raise ValueError("Invalid stored RAPP identity; refusing to re-mint.")
    else:
        identity = {
            "schema": "rapp/1",
            "rappid": rapp.mint_rappid("kody-w", "dynamics365-frame-machine"),
        }
        write("rappid.json", json_bytes(identity))
    stream_id = identity["rappid"]
    # Source time, not wall-clock time, keeps clean rebuilds reproducible.
    updated = max(
        datetime.fromisoformat(source["lastUpdated"].replace("Z", "+00:00"))
        for source in (overlay, liquid)
    )
    generated = updated.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )
    frames = []
    prev = None
    for seq, state in enumerate(machine["frames"]):
        payload = {
            **state,
            "activeSystemData": overlay["frames"][state["id"]]["activeSystemData"],
            "liquidDimension": liquid["frames"][state["id"]],
        }
        frame = rapp.build_frame(
            "body.pulse", stream_id, seq, generated, payload, prev
        )
        frames.append(frame)
        prev = frame["payload_hash"]
        write(f"frames/{seq:06d}.json", json_bytes(frame))
    if not frames:
        raise ValueError("The machine must contain at least one frame.")
    chain = "".join(rapp.canonical(frame) + "\n" for frame in frames).encode("utf-8")
    write("chain.jsonl", chain)
    head = {"seq": frames[-1]["seq"], "frame_hash": frames[-1]["frame_hash"]}
    write(
        "orient.json",
        json_bytes({
            "schema": "rapp/1-anchor",
            "generated_utc": generated,
            "stream_id": stream_id,
            "chain": "chain.jsonl",
            "head": head,
        }),
    )
    write(
        "rapp-frame-index.json",
        json_bytes({
            "schema": "rapp-frame-index/1",
            "stream_id": stream_id,
            "frames": [f"frames/{seq:06d}.json" for seq in range(len(frames))],
            "head": head,
        }),
    )
    sources = (
        ("machine", "machine.json", "Canonical CRM frame ledger."),
        ("overlay", "active-system-data.json", "Active system data for each frame."),
        ("liquid", "liquid-dimension.json", "Alternative fork dimension for each frame."),
        ("chain", "chain.jsonl", "Ordered rapp/1 body.pulse chain."),
    )
    entries = []
    for name, relative, description in sources:
        content = (ROOT / relative).read_bytes()
        sha256 = hashlib.sha256(content).hexdigest()
        sha8 = sha256[:12]
        version = f"versions/{name}/{sha8}{Path(relative).suffix}"
        write(version, content, immutable=True)
        entries.append({
            "name": name,
            "description": description,
            "path": relative,
            "sha8": sha8,
            "sha256": sha256,
            "version": version,
            "pages_url": f"{PAGES}/{PREFIX}/{relative}",
            "raw_url": f"{RAW}/main/{PREFIX}/{relative}",
            "version_pages_url": f"{PAGES}/{PREFIX}/{version}",
            "version_raw_url": f"{RAW}/main/{PREFIX}/{version}",
        })
    summary = {"entries": len(entries), "frames": len(frames)}
    write(
        "registry.json",
        json_bytes({
            "schema": "rapp-static-api/1.1",
            "generated": generated,
            "summary": summary,
            "pages_base": PAGES,
            "raw_base": RAW + "/main",
            "base": f"{PAGES}/{PREFIX}",
            "stream_id": stream_id,
            "head": head,
            "entries": entries,
        }),
    )
    write(
        "api/v1/frames.json",
        json_bytes({
            "schema": "dynamics365-frames/1.0",
            "generated": generated,
            "stream_id": stream_id,
            "head": head,
            "frames": frames,
        }),
    )
    write(
        "api/v1/status.json",
        json_bytes({
            "schema": "dynamics365-status/1.0",
            "generated": generated,
            "status": "ready",
            "summary": summary,
            "stream_id": stream_id,
            "head": head,
        }),
    )
    write(
        "api/v1/badge.json",
        json_bytes({
            "schemaVersion": 1,
            "label": "Dynamics 365 RAPP",
            "message": f"{len(frames)} frames | {head['frame_hash'][:8]}",
            "color": "blue",
        }),
    )
    links = "\n".join(
        f"- {entry['name']}: {entry['pages_url']}\n"
        f"  Immutable fallback: {entry['version_raw_url']}"
        for entry in entries
    )
    write(
        "llms.txt",
        (
            "# Dynamics 365 frame machine\n\n"
            "A local-first simulated CRM, not a connection to a live Dynamics tenant.\n"
            f"Pages base (primary): {PAGES}\n"
            f"Raw base (cross-origin fallback): {RAW}/main\n"
            f"Registry: {PAGES}/{PREFIX}/registry.json\n"
            f"Frames: {PAGES}/{PREFIX}/api/v1/frames.json\n"
            f"Status: {PAGES}/{PREFIX}/api/v1/status.json\n"
            f"Badge: {PAGES}/{PREFIX}/api/v1/badge.json\n"
            f"Orientation: {PAGES}/{PREFIX}/orient.json\n\n"
            f"{links}\n\n"
            "Verify SHA-256 bytes against registry entries (sha8 is 12 hex digits).\n"
            "The chain uses rapp/1 body.pulse; prev links to the prior payload_hash.\n"
            "Rebuild offline with python3 build.py; the three source JSON files stay unchanged.\n"
        ).encode("utf-8"),
    )
    write(".nojekyll", b"")


if __name__ == "__main__":
    build()
