#!/usr/bin/env python3
"""
dogg-companion-lens-terminal.py — the SAME "Canvas Companion Lens" concept
(rappid:@kody-w/dogg-lens-canvas-companion:80efc70ff840a43f703a035ebf153f62d6e9da8562984acc452de5a5258d5311),
JIT-adapted to a second, completely different medium: the terminal.

Proves the lens pattern generalizes rather than being a one-off browser trick.
The four companions and their DOGG-grounded content are IDENTICAL to the
browser version - only the render surface (ANSI terminal vs DOM) and each
companion's "local action" (medium-appropriate: git/system-load here,
save-function/FPS there) change.

Stdlib only, matching the DOGG ethos: keyless, public, small, verifiable
with stdlib code alone. Vendors the *exact* rapp/1 canonicalization + hashing
(H, canonical) from kody-w/dogg's own tools/rapp.py rather than a reimplementation,
so there is zero risk of a byte-for-byte mismatch with the reference verifier.

Usage:
    python3 dogg-companion-lens-terminal.py summon overwatch
    python3 dogg-companion-lens-terminal.py summon scout
    python3 dogg-companion-lens-terminal.py summon forge
    python3 dogg-companion-lens-terminal.py summon sentinel
    python3 dogg-companion-lens-terminal.py ledger        # show the local GODD ledger
    python3 dogg-companion-lens-terminal.py ledger export <file.json>
"""
from __future__ import annotations
import sys, os, json, hashlib, urllib.request, subprocess, datetime, pathlib

DOGG_RAW = "https://raw.githubusercontent.com/kody-w/dogg/main"
GODD_PATH = pathlib.Path.home() / ".rapp_godd_ledger.json"
GODD_MAX_ENTRIES = 500
UA = {"User-Agent": "dogg-companion-lens-terminal"}

# ---------- vendored verbatim from kody-w/dogg tools/rapp.py (rapp/1 §4-5) ----------
def canonical(v):
    if v is None or isinstance(v, bool):
        return json.dumps(v)
    if isinstance(v, int):
        return json.dumps(v)
    if isinstance(v, float):
        raise ValueError("floats require full-JCS number serialization; use ints/strings")
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        return "[" + ",".join(canonical(x) for x in v) + "]"
    if isinstance(v, dict):
        keys = sorted(v.keys())
        return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + canonical(v[k]) for k in keys) + "}"
    raise ValueError(f"non-I-JSON value: {type(v)}")

def H(space, v):
    return hashlib.sha256(space.encode() + b"\x0a" + canonical(v).encode("utf-8")).hexdigest()

def verify_frame_minimal(frame):
    """Just the two hash checks (§7.5 steps 2-3) - enough for a read-only
    consumer that isn't walking the whole chain, only trusting HEAD.json's
    published head_frame for the tip it just fetched."""
    payload_hash = H("rapp/1:particle", frame["payload"])
    if payload_hash != frame["payload_hash"]:
        return False, "payload_hash mismatch"
    pre = {k: frame[k] for k in frame if k not in ("frame_hash", "sig")}
    frame_hash = H("rapp/1:wave", pre)
    if frame_hash != frame["frame_hash"]:
        return False, "frame_hash mismatch"
    return True, "ok"

# ---------- network ----------
def get_json(url, timeout=6):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return json.loads(r.read().decode())

def get_text(url, timeout=6):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return r.read().decode()

def fetch_latest_verified_world_frame():
    head = get_json(f"{DOGG_RAW}/world/HEAD.json")
    count = head["count"]
    E = head.get("epoch_size", 288)
    sealed = head.get("sealed_epochs", 0)
    last_seq = count - 1
    if last_seq < sealed * E:
        k = last_seq // E
        lines = get_text(f"{DOGG_RAW}/world/epochs/{k}.jsonl").strip().split("\n")
        frame = json.loads(lines[last_seq - k * E])
    else:
        frame = get_json(f"{DOGG_RAW}/world/{last_seq}.json")
    ok, reason = verify_frame_minimal(frame)
    if not ok:
        raise ValueError(f"world frame failed verification: {reason}")
    if frame["frame_hash"] != head["head_frame"]:
        raise ValueError("world frame_hash does not match HEAD.json head_frame")
    return frame

# ---------- GODD ledger (same schema as the browser version) ----------
def godd_load():
    if not GODD_PATH.exists():
        return []
    try:
        return json.loads(GODD_PATH.read_text()).get("entries", [])
    except Exception:
        return []

def godd_save(entries):
    GODD_PATH.write_text(json.dumps({"schema": "godd/0-ledger", "entries": entries[-GODD_MAX_ENTRIES:]}, indent=2))

def godd_record(entry):
    entries = godd_load()
    entry = {**entry, "at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    entries.append(entry)
    godd_save(entries)
    return len(entries)

# ---------- terminal colors (ANSI, no deps) ----------
def c(code, s):
    return f"\033[{code}m{s}\033[0m"
BOLD = "1"; DIM = "2"; CYAN = "36"; YELLOW = "33"; GREEN = "32"; RED = "31"

# ---------- companions: identical DOGG-grounded content to the browser lens ----------
def render_overwatch(world):
    lines = []
    if world.get("hn_top"):
        lines.append(f'Top of human attention right now: "{world["hn_top"]["title"]}"')
    pm = world.get("prediction_markets", {}).get("top_by_volume")
    if pm:
        m = pm[0]
        lines.append(f'Highest-volume belief market: "{m["question"]}" — yes @ {m["yes_price"]}')
    return lines or ["No attention data in this frame."]

def render_scout(world):
    lines = []
    if world.get("iss"):
        lines.append(f'ISS right now: {world["iss"]["lat"]}, {world["iss"]["lon"]}')
    if world.get("earthquakes_past_hour"):
        eq = world["earthquakes_past_hour"]
        lines.append(f'Earthquakes in the past hour: {eq["count"]} (strongest M{eq["max_mag"]})')
    return lines or ["No planetary position data in this frame."]

def render_forge(world):
    lines = []
    if world.get("btc_usd"):
        lines.append(f'BTC/USD: ${world["btc_usd"]["spot"]}')
    if world.get("crypto_market"):
        lines.append(f'Total crypto market cap: ${int(float(world["crypto_market"]["total_mcap_usd"])):,}')
    if world.get("btc_fees"):
        lines.append(f'Cheapest confirm right now: {world["btc_fees"]["hour_sat_vb"]} sat/vB')
    if world.get("fx_usd"):
        fx = world["fx_usd"]
        lines.append(f'USD buys: €{fx["EUR"]} / £{fx["GBP"]} / ¥{fx["JPY"]}')
    return lines or ["No economic data in this frame."]

def render_sentinel(world):
    lines = []
    if world.get("space_weather"):
        kp = world["space_weather"]
        lines.append(f'Planetary Kp index: {kp["kp"]} (space weather, as of {kp["at"]})')
    if world.get("grid_carbon_gb"):
        gc = world["grid_carbon_gb"]
        lines.append(f'UK grid carbon intensity: {gc["gco2_kwh"]} gCO2/kWh ({gc["index"]})')
    return lines or ["No environmental data in this frame."]

# ---------- medium-appropriate local actions (terminal, not browser) ----------
def forge_local_action():
    """Terminal's equivalent of 'ask the host world to save its own state':
    if cwd is inside a git repo, record a REAL snapshot (branch + short SHA +
    dirty flag) - not a fabricated 'saved!'. If there's no repo, say so."""
    try:
        branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                 capture_output=True, text=True, timeout=3)
        if branch.returncode != 0:
            return {"ok": False, "detail": "not inside a git repository"}
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=3)
        dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, timeout=3)
        return {
            "ok": True,
            "detail": f"snapshot recorded: {branch.stdout.strip()}@{sha.stdout.strip()}"
                      f"{' (dirty)' if dirty.stdout.strip() else ' (clean)'}",
        }
    except Exception as e:
        return {"ok": False, "detail": f"git not available: {e}"}

def sentinel_local_action():
    """Terminal's equivalent of FPS/peer-count: real local system load."""
    try:
        load1, load5, load15 = os.getloadavg()
        return {"load1": round(load1, 2), "load5": round(load5, 2), "load15": round(load15, 2)}
    except (AttributeError, OSError):
        return {"load1": None, "load5": None, "load15": None}

COMPANIONS = {
    "overwatch": ("🛰️", "Overwatch", "observer", render_overwatch, None),
    "scout": ("🐾", "Scout", "pathfinder", render_scout, None),
    "forge": ("🔨", "Forge", "builder", render_forge, forge_local_action),
    "sentinel": ("🛡️", "Sentinel", "guardian", render_sentinel, sentinel_local_action),
}

def summon(name):
    if name not in COMPANIONS:
        print(c(RED, f"Unknown companion '{name}'. Choose from: {', '.join(COMPANIONS)}"))
        return 1
    icon, label, role, render, local_action = COMPANIONS[name]
    print(c(BOLD, f"{icon}  {label}") + c(DIM, f"  ({role})"))
    try:
        frame = fetch_latest_verified_world_frame()
    except Exception as e:
        print(c(YELLOW, f"⚠️  could not verify live DOGG data ({e}). {label} has nothing real to say right now."))
        return 1
    print(c(GREEN, f"✅ verified live — tick {frame['payload']['tick']}, frame {frame['frame_hash'][:10]}…"))
    for line in render(frame["payload"]["world"]):
        print("   " + line)
    count = godd_record({"companion": name, "medium": "terminal", "tick": frame["payload"]["tick"],
                          "frame_hash": frame["frame_hash"]})
    print(c(DIM, f"GODD ledger: {count} verified summons recorded on this machine ({GODD_PATH})."))
    if local_action:
        result = local_action()
        if name == "forge":
            tag = c(GREEN, "✅") if result["ok"] else c(YELLOW, "⚠️")
            print(f"   {tag} {result['detail']}")
        elif name == "sentinel":
            print(f"   Local system load (1/5/15 min): {result['load1']} / {result['load5']} / {result['load15']}")
    return 0

def ledger_cmd(args):
    entries = godd_load()
    if args and args[0] == "export":
        dest = pathlib.Path(args[1] if len(args) > 1 else f"godd-ledger-{int(datetime.datetime.now().timestamp())}.json")
        dest.write_text(json.dumps({"schema": "godd/0-ledger", "entries": entries}, indent=2))
        print(c(GREEN, f"Exported {len(entries)} entries to {dest}"))
        return 0
    print(c(BOLD, f"GODD ledger — {len(entries)} verified summons on this machine"))
    for e in entries[-10:]:
        print(f"  {e['at']}  {e['companion']:10s}  tick {e['tick']}  {e['frame_hash'][:10]}…")
    return 0

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd = sys.argv[1]
    if cmd == "summon" and len(sys.argv) >= 3:
        return summon(sys.argv[2].lower())
    if cmd == "ledger":
        return ledger_cmd(sys.argv[2:])
    print(__doc__)
    return 1

if __name__ == "__main__":
    sys.exit(main())
