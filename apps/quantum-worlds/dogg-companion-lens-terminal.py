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
with stdlib code alone. Vendors the *exact* RAPP/1 rev-17 strict parser, canonical
form, H and §7.5 frame verifier from kody-w/rapp-1 rapp.py (f6bafe7) rather than a
reimplementation, so there is zero risk of a mismatch with the reference verifier.

Usage:
    python3 dogg-companion-lens-terminal.py summon overwatch
    python3 dogg-companion-lens-terminal.py summon scout
    python3 dogg-companion-lens-terminal.py summon forge
    python3 dogg-companion-lens-terminal.py summon sentinel
    python3 dogg-companion-lens-terminal.py ledger        # show the local GODD ledger
    python3 dogg-companion-lens-terminal.py ledger export <file.json>
"""
from __future__ import annotations
import sys, os, re, json, base64, decimal, hashlib, urllib.request, subprocess, datetime, pathlib

DOGG_RAW = "https://raw.githubusercontent.com/kody-w/dogg/main"
GODD_PATH = pathlib.Path.home() / ".rapp_godd_ledger.json"
GODD_MAX_ENTRIES = 500
UA = {"User-Agent": "dogg-companion-lens-terminal"}

# ---------- vendored verbatim from kody-w/rapp-1 rapp.py @ f6bafe76735ba73510518810c8bc8cd133dcf527 (RAPP/1 rev-17) ----------
# §4 strict JSON and canonical form, §5 H, §6.1.1 grammar, §7.4 utc, the §10 detached-JWS form and the §7.5
# consumer checklist, copied byte-for-byte from the reference (never re-typed).
SPEC = "rapp/1"

_HEX64 = re.compile(r"[0-9a-f]{64}")

_UTC = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})\.[0-9]{3}Z", re.ASCII)

_LCLABEL = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")

_RAPPID = re.compile(r"rappid:@([a-z0-9]+(?:-[a-z0-9]+)*)/([a-z0-9]+(?:-[a-z0-9]+)*):([0-9a-f]{64})")

MAX_CANONICAL_BYTES = 1024 * 1024

MAX_JSON_INPUT_BYTES = 64 * 1024 * 1024   # a DoS guard on raw input only; §4 (d) bounds the canonical form

_B64URL = re.compile(r"^[A-Za-z0-9_-]*$")

FRAME_KEYS = {"spec", "kind", "stream_id", "seq", "utc", "payload",
              "payload_hash", "frame_hash", "prev", "prev_wave", "sig"}

_NOT_IJSON_CHAR = re.compile(
    "[\ud800-\udfff\ufdd0-\ufdef"
    + "".join(chr(plane << 16 | 0xFFFE) + chr(plane << 16 | 0xFFFF) for plane in range(17))
    + "]"
)

def _ijson_string(s):
    """A §4 string or member name in JCS form; refuses a surrogate or a noncharacter (§4 (b))."""
    bad = _NOT_IJSON_CHAR.search(s)
    if bad:
        raise ValueError(
            f"string holds U+{ord(bad.group()):04X}, a surrogate or noncharacter outside I-JSON (§4 (b))"
        )
    return json.dumps(s, ensure_ascii=False)

def _number_to_string(x):
    """ECMA-262 Number::toString of a finite binary64 value: the RFC 8785 §3.2.2.3 number form."""
    if x != x or x in (float("inf"), float("-inf")):
        raise ValueError("NaN and infinities are outside the §4 domain")
    if x == 0:
        return "0"                          # both zeros; -0 serializes as 0
    # repr() is the shortest digit string that round-trips (nearest, ties to even), the
    # digits Number::toString picks; only the layout differs, so re-lay it out here.
    mantissa, _, exponent = repr(abs(x)).partition("e")
    whole, _, fraction = mantissa.partition(".")
    digits = (whole + fraction).lstrip("0")
    n = len(whole) + int(exponent or 0) - (len(whole) + len(fraction) - len(digits))
    digits = digits.rstrip("0")
    k = len(digits)                         # value = 0.digits * 10**n
    if k <= n <= 21:
        text = digits + "0" * (n - k)
    elif 0 < n <= 21:
        text = digits[:n] + "." + digits[n:]
    elif -6 < n <= 0:
        text = "0." + "0" * -n + digits
    else:
        text = digits[0] + ("." + digits[1:] if k > 1 else "") + "e" + ("+" if n > 0 else "-") + str(abs(n - 1))
    return ("-" if x < 0 else "") + text

def canonical(v):
    """RFC 8785 JCS over the §4 I-JSON domain. Returns the canonical form as a str (encode as UTF-8)."""
    if v is None or isinstance(v, bool):
        return json.dumps(v)
    if isinstance(v, int):
        if abs(v) <= 2**53 - 1:
            return json.dumps(v)
        # §4 (c): a number is a binary64 value; an int outside +/-(2^53-1) is admitted only
        # when it is one exactly (2**53 is, 2**53 + 1 is not), and then serializes as JCS does.
        try:
            as_binary64 = float(v)
        except OverflowError:
            as_binary64 = None
        if as_binary64 != v:
            raise ValueError("int is not exactly representable as binary64 (§4 (c)); carry it as a string")
        return _number_to_string(as_binary64)
    if isinstance(v, float):
        return _number_to_string(v)
    if isinstance(v, str):
        return _ijson_string(v)
    if isinstance(v, list):
        return "[" + ",".join(canonical(x) for x in v) + "]"
    if isinstance(v, dict):
        if not all(isinstance(k, str) for k in v):
            raise ValueError("member names must be strings")
        # RFC 8785 orders member names by UTF-16 code units; plain sorted()
        # is code-POINT order and diverges for non-BMP keys.
        keys = sorted(v.keys(), key=lambda k: k.encode("utf-16-be", "surrogatepass"))
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate keys")
        return "{" + ",".join(_ijson_string(k) + ":" + canonical(v[k]) for k in keys) + "}"
    raise ValueError(f"non-I-JSON value: {type(v)}")

_H_SPACES = frozenset({"rapp/1:particle", "rapp/1:wave", "rapp/1:egg-manifest",
                       "rapp/1:sealed-aad", "rapp/1:sealed-key-request"})

def H(space, v):
    if not (isinstance(space, str) and space in _H_SPACES):
        raise ValueError(f"§5: H (a value hash) is used only with the tags {sorted(_H_SPACES)}; refused {space!r}")
    return hashlib.sha256(space.encode() + b"\x0a" + canonical(v).encode("utf-8")).hexdigest()

def rappid_valid(s):
    if not isinstance(s, str):
        return False
    match = _RAPPID.fullmatch(s)
    return bool(
        match
        and 1 <= len(match.group(1)) <= 39
        and 1 <= len(match.group(2)) <= 100
    )

_KIND = re.compile(r"([a-z0-9]+(?:-[a-z0-9]+)*)\.([a-z0-9]+(?:-[a-z0-9]+)*)")

def kind_valid(kind):
    """§6.1.1 `kind = lclabel "." lclabel`, each label 1–64 characters."""
    match = _KIND.fullmatch(kind) if isinstance(kind, str) else None
    return bool(match and 1 <= len(match.group(1)) <= 64 and 1 <= len(match.group(2)) <= 64)

def stream_form(stream_id):
    """§6.1.1: "memory-stream", "body-stream" or "swarm-stream", or None if the string is none of them."""
    if not isinstance(stream_id, str):
        return None
    if stream_id.startswith("net:"):
        return "swarm-stream" if _LCLABEL.fullmatch(stream_id[4:]) else None
    if rappid_valid(stream_id):
        return "body-stream"
    head, sep, instance = stream_id.rpartition(":")
    if sep and rappid_valid(head) and _LCLABEL.fullmatch(instance) and 1 <= len(instance) <= 64:
        return "memory-stream"
    return None

def utc_valid(value):
    """§7.4 (rev-17 E-1): exactly the 24-octet form YYYY-MM-DDTHH:MM:SS.mmmZ in ASCII digits,
    calendar-valid on the proleptic Gregorian calendar for years 0000-9999, seconds 00-59."""
    if not isinstance(value, str) or len(value) != 24 or not value.isascii():
        return False
    match = _UTC.fullmatch(value)
    if not match:
        return False
    year, month, day, hour, minute, second = (int(group) for group in match.groups())
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    days = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    return 1 <= month <= 12 and 1 <= day <= days[month - 1] and hour <= 23 and minute <= 59 and second <= 59

def _b64url_decode(value):
    if (
        not isinstance(value, str)
        or "=" in value
        or not _B64URL.fullmatch(value)
        or len(value) % 4 == 1
    ):
        raise ValueError("base64url value must be unpadded")
    decoded = base64.b64decode(
        value + "=" * (-len(value) % 4),
        altchars=b"-_",
        validate=True,
    )
    if base64.urlsafe_b64encode(decoded).rstrip(b"=").decode("ascii") != value:
        raise ValueError("base64url value is not canonical")
    return decoded

def parse_detached_jws(sig):
    parts = sig.split(".") if isinstance(sig, str) else []
    if len(parts) != 3 or parts[1] != "":
        raise ValueError("JWS must use detached compact serialization")
    header_octets = _b64url_decode(parts[0])
    header = _strict_json(header_octets)
    if not isinstance(header, dict) or set(header) != {"alg", "b64", "crit", "kid"}:
        raise ValueError("JWS protected header must have exactly alg,b64,crit,kid")
    if header["alg"] not in {"EdDSA", "ES256"}:
        raise ValueError("JWS alg must be EdDSA or ES256")
    if header["b64"] is not False or header["crit"] != ["b64"]:
        raise ValueError("JWS must use b64=false with crit=['b64']")
    if not rappid_valid(header["kid"]):
        raise ValueError("JWS kid must be a valid keyed RAPPID")
    if header_octets != canonical(header).encode("utf-8"):
        raise ValueError("JWS protected header is not canonical")
    signature = _b64url_decode(parts[2])
    if len(signature) != 64:
        raise ValueError("JWS signature must be exactly 64 octets (§7.5 step 1, §10)")
    return header, parts[0], signature

def _uint53(value):
    """§7.4 `uint53`: an int (never a bool or a float) from 0 to 2^53-1."""
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 2**53 - 1

def _hex64_or_null(value):
    return value is None or (isinstance(value, str) and bool(_HEX64.fullmatch(value)))

def _is_regenesis(kind):
    """§12.1: a `*.re-genesis` kind, whose second label is exactly "re-genesis"."""
    return isinstance(kind, str) and kind.partition(".")[2] == "re-genesis"

def _regenesis_payload_error(payload):
    """§12.1 step 2 (rev-17 E-22): None if `payload` is the one re-genesis shape, else the reason."""
    if not isinstance(payload, dict) or set(payload) != {"migrated_from"}:
        return 're-genesis payload must be exactly {"migrated_from": {...}} (§12.1 step 2)'
    moved = payload["migrated_from"]
    if not isinstance(moved, dict) or set(moved) != {"stream_id", "terminal_seal", "terminal_seq"}:
        return "re-genesis migrated_from must be exactly stream_id, terminal_seal, terminal_seq (§12.1 step 2)"
    if stream_form(moved["stream_id"]) is None:
        return "re-genesis migrated_from.stream_id is not a §6.1.1 stream_id"
    if not (isinstance(moved["terminal_seal"], str) and _HEX64.fullmatch(moved["terminal_seal"])):
        return "re-genesis migrated_from.terminal_seal is not 64 lowercase hex"
    if not _uint53(moved["terminal_seq"]):
        return "re-genesis migrated_from.terminal_seq is not a uint53"
    return None

def verify_frame(
    frame,
    head=None,
    stream_id_of_record=None,
    signature_verifier=None,
    *,
    registry=None,
):
    """§7.5 consumer checklist. Returns (ok, failing_step_or_None, reason).

    `registry` (optional) is a duck-typed §13 registry such as rapp_registry.Registry:
    check_frame_binding(frame) -> (ok, reason) joins step 1, registered_genesis(stream_id)
    -> entry or None joins step 4, and owner_at(utc) -> rappid names the step-6 signer a
    `*.re-genesis` frame requires."""
    # 1 shape & types
    if not isinstance(frame, dict):
        return False, "1", "frame is not a JSON object"
    if set(frame.keys()) != FRAME_KEYS:
        return False, "1", f"key set != 11 ({sorted(frame.keys())})"
    if frame["spec"] != SPEC:
        return False, "1", "spec != rapp/1"
    if not kind_valid(frame["kind"]):
        return False, "1", "kind grammar (§6.1.1: two lclabels of 1-64 characters)"
    form = stream_form(frame["stream_id"])
    if form is None:
        return False, "1", "stream_id grammar (§6.1.1; a provisional tail is never a stream_id, §6.3)"
    if not _uint53(frame["seq"]):
        return False, "1", "seq not uint53"
    if not utc_valid(frame["utc"]):
        return False, "1", "utc not fixed form"
    if not isinstance(frame["payload"], dict):
        return False, "1", "payload not object"
    for k in ("payload_hash", "frame_hash"):
        if not (isinstance(frame[k], str) and _HEX64.fullmatch(frame[k])):
            return False, "1", f"{k} not 64hex"
    for k in ("prev", "prev_wave"):
        if not _hex64_or_null(frame[k]):
            return False, "1", f"{k} not null|64hex"
    if frame["sig"] is not None:
        try:
            parse_detached_jws(frame["sig"])
        except Exception as exc:
            return False, "1", f"sig is not null or a §10 detached JWS: {exc}"
    regenesis = _is_regenesis(frame["kind"])
    if regenesis:
        why = _regenesis_payload_error(frame["payload"])
        if why:
            return False, "1", why
    if registry is not None:
        try:
            bound, why = registry.check_frame_binding(frame)
        except Exception as exc:
            bound, why = False, f"binding check failed: {exc}"
        if not bound:
            return False, "1", f"registry binding: {why}"
    # 1a stream binding
    if stream_id_of_record is not None and frame["stream_id"] != stream_id_of_record:
        return False, "1a", "stream_id mismatch (cross-stream replay)"
    # 2 particle
    if frame["payload_hash"] != H("rapp/1:particle", frame["payload"]):
        return False, "2", "payload_hash mismatch"
    # 3 wave
    pre = {k: frame[k] for k in frame if k not in ("frame_hash", "sig")}
    if frame["frame_hash"] != H("rapp/1:wave", pre):
        return False, "3", "frame_hash mismatch"
    # 4 chain
    if regenesis and (frame["seq"] != 0 or frame["prev"] is not None):
        return False, "4", "a re-genesis frame must be a genesis: seq=0 prev=null (§12.1 step 2)"
    if head is None:
        if not (frame["seq"] == 0 and frame["prev"] is None):
            return False, "4", "genesis must be seq=0 prev=null"
        if registry is not None:
            try:
                entry = registry.registered_genesis(frame["stream_id"])
                registered = None if entry is None else entry["frame_hash"]
            except Exception as exc:
                return False, "4", f"registered genesis lookup failed: {exc}"
            if registered is not None and registered != frame["frame_hash"]:
                return False, "4", "genesis is not the stream's registered genesis (§7.5 step 4, §13.3)"
    else:
        if frame["seq"] != head["seq"] + 1:
            return False, "4", "seq not contiguous"
        if frame["prev"] != head["payload_hash"]:
            return False, "4", "prev != head payload_hash"
        if frame["utc"] < head["utc"]:
            return False, "4", "utc < head utc"
    # 5 wire
    is_swarm = form == "swarm-stream"
    if is_swarm and frame["seq"] > 0:
        if head is not None and frame["prev_wave"] != head["frame_hash"]:
            return False, "5", "prev_wave != head frame_hash"
    else:
        if frame["prev_wave"] is not None:
            return False, "5", "prev_wave must be null off swarm"
    # 6 signature
    if is_swarm and frame["sig"] is None:
        return False, "6", "swarm frame must be signed"
    if regenesis and frame["sig"] is None:
        return False, "6", "a re-genesis frame must be owner-signed (§12.1 step 2)"
    if frame["sig"] is not None:
        expected_signer = None
        if regenesis and registry is not None:
            try:
                expected_signer = registry.owner_at(frame["utc"])
            except Exception as exc:
                return False, "6", f"owner in effect at utc is unresolvable: {exc}"
            if expected_signer is None:
                return False, "6", "no estate owner in effect at the re-genesis utc (§13.2)"
        ok, why = _signature_ok(frame, signature_verifier, expected_signer)
        if not ok:
            return False, "6", why
    return True, None, "ok"

def _json_number(token):
    """§4 (c): parse a number token as its nearest binary64 d; refuse unless d is finite and
    Number::toString(d) denotes exactly the token's value (so 0.1 passes, 0.10000000000000001 does not)."""
    d = float(token)                                   # correctly rounded, ties to even; overlong -> +/-inf
    if d != d or d in (float("inf"), float("-inf")):
        raise ValueError(f"number token {token[:40]} is not a finite binary64 value (§4 (c))")
    try:
        same = decimal.Decimal(token) == decimal.Decimal(_number_to_string(d))
    except ArithmeticError:
        # An exponent beyond decimal's range. d is finite, so it is a zero, and the token
        # denotes the same value iff every digit of its significand is zero.
        same = not any(c in "123456789" for c in token.lower().partition("e")[0])
    if not same:
        raise ValueError(f"number token {token[:40]} does not survive the binary64 round trip (§4 (c))")
    return d

def _json_int(token):
    if token == "-0":
        return -0.0          # E-9: -0 is not an integer token a field rule may take for 0; canonical(-0.0) is "0"
    d = _json_number(token)  # refuses 9007199254740993 and overlong tokens before int() runs
    value = int(token)
    # 10**23 passes §4 (c) (its d prints as "1e+23") but is not d; the value parsed is d itself.
    return value if value == d else int(d)

def _json_constant(token):
    raise ValueError(f"{token} is not a JSON number (§4 (c))")

def _strict_json(blob):
    """Parse one §4 JSON text (octets or str) and return its value, or raise ValueError."""
    if isinstance(blob, (bytes, bytearray)):
        if len(blob) > MAX_JSON_INPUT_BYTES:
            raise ValueError("JSON text exceeds the 64 MiB input guard")
        if blob.startswith(b"\xef\xbb\xbf"):
            raise ValueError("JSON text starts with a byte-order mark; §4 refuses it (never strips it)")
        try:
            text = bytes(blob).decode("utf-8")        # strict: UTF-16/UTF-32 text is never transcoded
        except UnicodeDecodeError as exc:
            raise ValueError(f"JSON text is not well-formed UTF-8 (§4): {exc}") from None
    elif isinstance(blob, str):
        if len(blob) > MAX_JSON_INPUT_BYTES:          # a str is bounded by its code points
            raise ValueError("JSON text exceeds the 64 MiB input guard")
        text = blob
    else:
        raise ValueError("JSON text must be octets or a str")
    if text.startswith("\ufeff"):
        raise ValueError("JSON text starts with a byte-order mark; §4 refuses it (never strips it)")

    def pairs(values):
        result = {}
        for key, value in values:
            if key in result:
                raise ValueError(f"duplicate JSON member: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(
            text,
            object_pairs_hook=pairs,
            parse_float=_json_number,
            parse_int=_json_int,
            parse_constant=_json_constant,
        )
    except RecursionError:
        raise ValueError("JSON nesting depth exceeds 64 (§4 (d))") from None
    # §4 (d): the root is depth 1 and only objects and arrays add a level; scalars never do.
    stack = [(value, 1)]
    while stack:
        current, depth = stack.pop()
        children = current.values() if isinstance(current, dict) else current if isinstance(current, list) else ()
        for item in children:
            if isinstance(item, (dict, list)):
                if depth + 1 > 64:
                    raise ValueError("JSON nesting depth exceeds 64 (§4 (d))")
                stack.append((item, depth + 1))
    if len(canonical(value).encode("utf-8")) > MAX_CANONICAL_BYTES:
        raise ValueError("canonical JSON exceeds the 1 MiB ceiling (§4 (d))")
    return value

def _signature_ok(manifest, signature_verifier, expected_signer=None):
    if signature_verifier is None:
        return False, "trusted signature verifier is required"
    unsigned = {k: v for k, v in manifest.items() if k != "sig"}
    try:
        if expected_signer is None:
            result = signature_verifier(unsigned, manifest["sig"])
        else:
            result = signature_verifier(
                unsigned,
                manifest["sig"],
                expected_signer,
            )
    except Exception as exc:
        return False, f"signature verifier failed: {exc}"
    if isinstance(result, tuple):
        return bool(result[0]), str(result[1]) if len(result) > 1 else ""
    return bool(result), "signature refused"

# ---------- network ----------
def get_json(url, timeout=6):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        return _strict_json(r.read())

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
        frame = _strict_json(lines[last_seq - k * E])
    else:
        frame = get_json(f"{DOGG_RAW}/world/{last_seq}.json")
    ok, step, reason = verify_frame(frame, stream_id_of_record=head.get("stream_id"))
    if not ok:
        raise ValueError(f"world frame failed §7.5 step {step}: {reason}")
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
