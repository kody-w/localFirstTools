/*
 * dogg-companion-lens.js — reference implementation of the "Canvas Companion Lens"
 * (DOGG dimension rappid:@kody-w/dogg-lens-canvas-companion:80efc70ff840a43f703a035ebf153f62d6e9da8562984acc452de5a5258d5311,
 *  registered at https://github.com/kody-w/dogg/tree/main/lens-canvas-companion)
 *
 * Summons four companions — Overwatch, Scout, Forge, Sentinel — into any single-file
 * HTML canvas world. Every word each companion says is a real, hash-verified slice of
 * DOGG's public world/<tick> telemetry chain. Nothing here is fabricated: if the data
 * can't be fetched or doesn't verify, the companion says so instead of making something
 * up (fail closed, matching the DOGG protocol's own ethos).
 *
 * GODD ledger: every VERIFIED summon is appended to a small local log
 * (localStorage key 'rapp_godd_ledger'), capped and export/import-able — the actual
 * accumulating asset this whole thing is for. It only ever records what really
 * happened (companion, world, tick, frame_hash), never a fabricated "learning".
 *
 * Self-contained. No build step. Safe to drop into any Quantum World with one
 * <script src="../../apps/quantum-worlds/dogg-companion-lens.js"></script> tag
 * (or inlined) right before </body>.
 */
(function () {
    'use strict';

    const DOGG_RAW = 'https://raw.githubusercontent.com/kody-w/dogg/main';
    const FETCH_TIMEOUT_MS = 6000;
    const GODD_KEY = 'rapp_godd_ledger';
    const GODD_MAX_ENTRIES = 500; // defensive cap, same lesson as the monument-import cap

    // -------- rapp/1 (rev-17) §4 strict JSON, canonical form and §5 hashing --------
    // The lens parses every octet it fetches itself: res.json() would repair what §4 refuses (duplicate
    // names, lone surrogates, numbers that do not survive binary64, over-deep nesting).
    const MAX_CANONICAL_BYTES = 1024 * 1024;
    const NON_INTEGER_TOKEN = new WeakMap(); // object -> names of members whose number token was not an integer token

    function checkString(s) {
        for (const ch of s) {
            const cp = ch.codePointAt(0);
            if ((cp >= 0xD800 && cp <= 0xDFFF) || (cp >= 0xFDD0 && cp <= 0xFDEF) || (cp & 0xFFFE) === 0xFFFE) {
                throw new Error('string holds U+' + cp.toString(16).toUpperCase().padStart(4, '0') + ', a surrogate or noncharacter outside I-JSON (§4 (b))');
            }
        }
        return s;
    }

    // The exact decimal value of a number token (or of a Number::toString result), as sign, digits and exponent.
    function decimalValue(text) {
        const m = /^(-?)(\d+)(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/.exec(text);
        const all = (m[2] + (m[3] || '')).replace(/^0+/, '');
        if (!all) return '0';
        const digits = all.replace(/0+$/, '');
        return m[1] + digits + 'e' + (BigInt(m[4] || 0) - BigInt((m[3] || '').length) + BigInt(all.length - digits.length));
    }

    function parseStrict(octets) {
        const bytes = new Uint8Array(octets);
        if (bytes[0] === 0xEF && bytes[1] === 0xBB && bytes[2] === 0xBF) throw new Error('JSON text starts with a byte-order mark; §4 refuses it');
        const text = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(bytes);
        const ESC = { '"': '"', '\\': '\\', '/': '/', b: '\b', f: '\f', n: '\n', r: '\r', t: '\t' };
        let i = 0, integerToken = false;
        const ws = () => { while (text[i] === ' ' || text[i] === '\t' || text[i] === '\n' || text[i] === '\r') i++; };
        const fail = (what) => { throw new Error('not a §4 JSON text: ' + what + ' at offset ' + i); };
        function string() {
            let out = '';
            for (i++; ;) {
                if (i >= text.length) fail('unterminated string');
                const c = text[i++];
                if (c === '"') return checkString(out);
                if (c < ' ') fail('control character in a string');
                if (c !== '\\') { out += c; continue; }
                const e = text[i++];
                if (Object.prototype.hasOwnProperty.call(ESC, e)) out += ESC[e];
                else if (e === 'u' && /^[0-9a-fA-F]{4}$/.test(text.slice(i, i + 4))) { out += String.fromCharCode(parseInt(text.slice(i, i + 4), 16)); i += 4; }
                else fail('bad escape');
            }
        }
        function number() {
            const re = /-?(?:0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?/y;
            re.lastIndex = i;
            const m = re.exec(text);
            if (!m) fail('bad value');
            i = re.lastIndex;
            const d = Number(m[0]);
            if (!Number.isFinite(d)) throw new Error('number token ' + m[0].slice(0, 40) + ' is not a finite binary64 value (§4 (c))');
            if (decimalValue(m[0]) !== decimalValue(String(d))) throw new Error('number token ' + m[0].slice(0, 40) + ' does not survive the binary64 round trip (§4 (c))');
            integerToken = !m[1] && !m[2] && m[0] !== '-0';
            return d;
        }
        function value(depth) {
            ws();
            const c = text[i];
            if (c === '{' || c === '[') {
                if (depth > 64) throw new Error('JSON nesting depth exceeds 64 (§4 (d))');
                i++; ws();
                const close = c === '{' ? '}' : ']';
                const out = c === '{' ? {} : [];
                let nonInteger = null;
                if (text[i] === close) { i++; return out; }
                for (;;) {
                    if (c === '[') out.push(value(depth + 1));
                    else {
                        ws();
                        if (text[i] !== '"') fail('expected a member name');
                        const key = string();
                        if (Object.prototype.hasOwnProperty.call(out, key)) throw new Error('duplicate JSON member: ' + key);
                        ws();
                        if (text[i++] !== ':') fail('expected :');
                        const v = value(depth + 1);
                        if (typeof v === 'number' && !integerToken) (nonInteger || (nonInteger = new Set())).add(key);
                        Object.defineProperty(out, key, { value: v, enumerable: true, writable: true, configurable: true });
                    }
                    ws();
                    if (text[i] === ',') { i++; continue; }
                    if (text[i++] === close) break;
                    fail('expected , or ' + close);
                }
                if (nonInteger) NON_INTEGER_TOKEN.set(out, nonInteger);
                return out;
            }
            if (c === '"') return string();
            for (const [word, v] of [['true', true], ['false', false], ['null', null]]) {
                if (text.startsWith(word, i)) { i += word.length; return v; }
            }
            return number();
        }
        const root = value(1);
        ws();
        if (i !== text.length) fail('trailing data');
        if (new TextEncoder().encode(canonical(root)).length > MAX_CANONICAL_BYTES) throw new Error('canonical JSON exceeds the 1 MiB ceiling (§4 (d))');
        return root;
    }

    function canonical(v) {
        if (v === null || typeof v === 'boolean') return JSON.stringify(v);
        if (typeof v === 'number') {
            if (!Number.isFinite(v)) throw new Error('NaN and infinities are outside the §4 domain');
            return JSON.stringify(v); // ECMA-262 Number::toString, the RFC 8785 number form (-0 serializes as 0)
        }
        if (typeof v === 'string') return JSON.stringify(checkString(v));
        if (Array.isArray(v)) return '[' + v.map((x) => canonical(x)).join(',') + ']';
        if (typeof v === 'object') {
            const keys = Object.keys(v).sort(); // UTF-16 code-unit order, as RFC 8785 requires
            return '{' + keys.map(k => JSON.stringify(checkString(k)) + ':' + canonical(v[k])).join(',') + '}';
        }
        throw new Error('non-serializable value: ' + typeof v);
    }

    async function sha256Hex(str) {
        const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
        return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
    }

    // §5 (rev-17 E-7): H takes only its own tags; every other tag is refused.
    const H_SPACES = ['rapp/1:particle', 'rapp/1:wave', 'rapp/1:egg-manifest', 'rapp/1:sealed-aad', 'rapp/1:sealed-key-request'];
    async function H(space, v) {
        if (!H_SPACES.includes(space)) throw new Error('§5: H is used only with the tags ' + H_SPACES.join(', ') + '; refused ' + JSON.stringify(space));
        return sha256Hex(space + '\n' + canonical(v));
    }

    // -------- rapp/1 (rev-17) §7.5 consumer checklist (registry-less, no signature verifier) --------
    const LCLABEL = '[a-z0-9]+(?:-[a-z0-9]+)*';
    const LCLABEL_RE = new RegExp('^' + LCLABEL + '$');
    const RAPPID_RE = new RegExp('^rappid:@(' + LCLABEL + ')/(' + LCLABEL + '):([0-9a-f]{64})$');
    const KIND_RE = new RegExp('^(' + LCLABEL + ')\\.(' + LCLABEL + ')$');
    const UTC_RE = /^([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})\.[0-9]{3}Z$/;
    const HEX64_RE = /^[0-9a-f]{64}$/;
    const FRAME_KEYS = ['spec', 'kind', 'stream_id', 'seq', 'utc', 'payload', 'payload_hash', 'frame_hash', 'prev', 'prev_wave', 'sig'];
    const isObject = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
    const hasExactly = (o, keys) => Object.keys(o).length === keys.length && keys.every(k => Object.prototype.hasOwnProperty.call(o, k));
    const isHex64 = (v) => typeof v === 'string' && HEX64_RE.test(v);

    function rappidValid(s) {
        const m = typeof s === 'string' ? RAPPID_RE.exec(s) : null;
        return !!m && m[1].length <= 39 && m[2].length <= 100;
    }
    function kindValid(k) {
        const m = typeof k === 'string' ? KIND_RE.exec(k) : null;
        return !!m && m[1].length <= 64 && m[2].length <= 64;
    }
    // §6.1.1: 'memory-stream', 'body-stream', 'swarm-stream', or null.
    function streamForm(id) {
        if (typeof id !== 'string') return null;
        if (id.startsWith('net:')) return LCLABEL_RE.test(id.slice(4)) ? 'swarm-stream' : null;
        if (rappidValid(id)) return 'body-stream';
        const at = id.lastIndexOf(':');
        const instance = id.slice(at + 1);
        return at >= 0 && rappidValid(id.slice(0, at)) && LCLABEL_RE.test(instance) && instance.length <= 64 ? 'memory-stream' : null;
    }
    // §7.4 (rev-17 E-1): the 24-octet ASCII form, calendar-valid for years 0000-9999, seconds 00-59.
    function utcValid(v) {
        const m = typeof v === 'string' && v.length === 24 ? UTC_RE.exec(v) : null;
        if (!m) return false;
        const [y, mo, d, h, mi, s] = m.slice(1).map(Number);
        const leap = y % 4 === 0 && (y % 100 !== 0 || y % 400 === 0);
        const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
        return mo >= 1 && mo <= 12 && d >= 1 && d <= days[mo - 1] && h <= 23 && mi <= 59 && s <= 59;
    }
    // §7.4 uint53: an integer number token (never -0, a fraction or an exponent) from 0 to 2^53-1 (rev-17 E-2, E-9).
    function uint53(obj, key) {
        const v = obj[key];
        return typeof v === 'number' && Number.isSafeInteger(v) && v >= 0 && !(NON_INTEGER_TOKEN.get(obj) || new Set()).has(key);
    }
    function b64urlDecode(s) {
        if (typeof s !== 'string' || !/^[A-Za-z0-9_-]*$/.test(s) || s.length % 4 === 1) throw new Error('base64url value must be unpadded');
        const bin = atob(s.replace(/-/g, '+').replace(/_/g, '/') + '='.repeat((4 - s.length % 4) % 4));
        if (btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '') !== s) throw new Error('base64url value is not canonical');
        return Uint8Array.from(bin, (c) => c.charCodeAt(0));
    }
    // §10 detached JWS form and protected-header profile (checked at §7.5 step 1; no cryptography).
    function checkDetachedJws(sig) {
        const parts = typeof sig === 'string' ? sig.split('.') : [];
        if (parts.length !== 3 || parts[1] !== '') throw new Error('JWS must use detached compact serialization');
        const headerOctets = b64urlDecode(parts[0]);
        const header = parseStrict(headerOctets);
        if (!isObject(header) || !hasExactly(header, ['alg', 'b64', 'crit', 'kid'])) throw new Error('JWS protected header must have exactly alg,b64,crit,kid');
        if (header.alg !== 'EdDSA' && header.alg !== 'ES256') throw new Error('JWS alg must be EdDSA or ES256');
        if (header.b64 !== false || !Array.isArray(header.crit) || header.crit.length !== 1 || header.crit[0] !== 'b64') throw new Error("JWS must use b64=false with crit=['b64']");
        if (!rappidValid(header.kid)) throw new Error('JWS kid must be a valid keyed RAPPID');
        if (new TextEncoder().encode(canonical(header)).join() !== headerOctets.join()) throw new Error('JWS protected header is not canonical');
        if (b64urlDecode(parts[2]).length !== 64) throw new Error('JWS signature must be exactly 64 octets');
    }
    // §12.1 step 2 (rev-17 E-22): the one re-genesis payload shape.
    function regenesisPayloadError(p) {
        if (!hasExactly(p, ['migrated_from'])) return 're-genesis payload must be exactly {"migrated_from": {...}}';
        const m = p.migrated_from;
        if (!isObject(m) || !hasExactly(m, ['stream_id', 'terminal_seal', 'terminal_seq'])) return 're-genesis migrated_from must be exactly stream_id, terminal_seal, terminal_seq';
        if (streamForm(m.stream_id) === null) return 're-genesis migrated_from.stream_id is not a §6.1.1 stream_id';
        if (!isHex64(m.terminal_seal)) return 're-genesis migrated_from.terminal_seal is not 64 lowercase hex';
        if (!uint53(m, 'terminal_seq')) return 're-genesis migrated_from.terminal_seq is not a uint53';
        return null;
    }

    // Returns { ok, step, reason }; step is the first failing §7.5 step. `head` is the last frame this consumer
    // verified on the stream (null: the frame must be a genesis); `streamIdOfRecord` is the stream being read.
    async function verifyFrame(frame, head, streamIdOfRecord) {
        const no = (step, reason) => ({ ok: false, step, reason });
        try {
            // 1 shape & types
            if (!isObject(frame)) return no('1', 'frame is not a JSON object');
            if (!hasExactly(frame, FRAME_KEYS)) return no('1', 'key set is not the eleven §7.1 keys');
            if (frame.spec !== 'rapp/1') return no('1', 'spec != rapp/1');
            if (!kindValid(frame.kind)) return no('1', 'kind grammar (§6.1.1)');
            const form = streamForm(frame.stream_id);
            if (form === null) return no('1', 'stream_id grammar (§6.1.1)');
            if (!uint53(frame, 'seq')) return no('1', 'seq not uint53');
            if (!utcValid(frame.utc)) return no('1', 'utc not the §7.4 fixed form');
            if (!isObject(frame.payload)) return no('1', 'payload not object');
            if (!isHex64(frame.payload_hash) || !isHex64(frame.frame_hash)) return no('1', 'payload_hash/frame_hash not 64hex');
            if ((frame.prev !== null && !isHex64(frame.prev)) || (frame.prev_wave !== null && !isHex64(frame.prev_wave))) return no('1', 'prev/prev_wave not null|64hex');
            if (frame.sig !== null) {
                try { checkDetachedJws(frame.sig); } catch (e) { return no('1', 'sig is not null or a §10 detached JWS: ' + e.message); }
            }
            const regenesis = frame.kind.split('.')[1] === 're-genesis';
            if (regenesis) {
                const why = regenesisPayloadError(frame.payload);
                if (why) return no('1', why);
            }
            // 1a stream binding
            if (streamIdOfRecord != null && frame.stream_id !== streamIdOfRecord) return no('1a', 'stream_id mismatch (cross-stream replay)');
            // 2 particle
            if (frame.payload_hash !== await H('rapp/1:particle', frame.payload)) return no('2', 'payload_hash mismatch');
            // 3 wave
            const pre = {};
            for (const k of Object.keys(frame)) if (k !== 'frame_hash' && k !== 'sig') pre[k] = frame[k];
            if (frame.frame_hash !== await H('rapp/1:wave', pre)) return no('3', 'frame_hash mismatch');
            // 4 chain
            if (regenesis && (frame.seq !== 0 || frame.prev !== null)) return no('4', 'a re-genesis frame must be a genesis');
            if (head == null) {
                if (frame.seq !== 0 || frame.prev !== null) return no('4', 'no verified head: only a genesis (seq=0, prev=null) can be accepted');
            } else {
                if (frame.seq !== head.seq + 1) return no('4', 'seq not contiguous');
                if (frame.prev !== head.payload_hash) return no('4', 'prev != head payload_hash');
                if (frame.utc < head.utc) return no('4', 'utc < head utc');
            }
            // 5 wire
            const swarm = form === 'swarm-stream';
            if (swarm && frame.seq > 0) {
                if (head != null && frame.prev_wave !== head.frame_hash) return no('5', 'prev_wave != head frame_hash');
            } else if (frame.prev_wave !== null) return no('5', 'prev_wave must be null off swarm');
            // 6 signature
            if (swarm && frame.sig === null) return no('6', 'swarm frame must be signed');
            if (regenesis && frame.sig === null) return no('6', 'a re-genesis frame must be owner-signed');
            if (frame.sig !== null) return no('6', 'signed frame: this lens has no §13 key discovery or §10 verifier');
            return { ok: true, step: null, reason: 'ok' };
        } catch (e) {
            return no(null, 'verify threw: ' + e.message);
        }
    }

    async function fetchJson(url) {
        const controller = new AbortController();
        const t = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
        try {
            const res = await fetch(url, { signal: controller.signal, cache: 'no-store' });
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return parseStrict(await res.arrayBuffer());
        } finally {
            clearTimeout(t);
        }
    }

    // -------- Fetch + verify the latest world/<tick> frame from the live chain --------
    async function fetchLatestVerifiedWorldFrame() {
        const head = await fetchJson(`${DOGG_RAW}/world/HEAD.json`);
        const count = head.count;
        const E = head.epoch_size || 288;
        const sealed = head.sealed_epochs || 0;
        const lastSeq = count - 1;
        let frame;
        if (lastSeq < sealed * E) {
            // Inside a sealed epoch bundle (rare for "latest", but handle it honestly)
            const k = Math.floor(lastSeq / E);
            const text = await (await fetch(`${DOGG_RAW}/world/epochs/${k}.jsonl`, { cache: 'no-store' })).text();
            const lines = text.trim().split('\n');
            frame = parseStrict(new TextEncoder().encode(lines[lastSeq - k * E]));
        } else {
            frame = await fetchJson(`${DOGG_RAW}/world/${lastSeq}.json`);
        }
        const v = await verifyFrame(frame, null, head.stream_id);
        if (!v.ok) throw new Error('world frame failed §7.5 step ' + v.step + ': ' + v.reason);
        if (frame.frame_hash !== head.head_frame) {
            throw new Error('world frame_hash does not match HEAD.json head_frame (possible tamper or race)');
        }
        return frame;
    }

    // -------- GODD ledger: the real accumulating record --------
    function goddLoad() {
        try {
            const raw = localStorage.getItem(GODD_KEY);
            return raw ? JSON.parse(raw) : [];
        } catch (e) {
            console.warn('DOGG Companion Lens: localStorage unavailable, GODD ledger is session-only', e);
            return [];
        }
    }
    function goddSave(entries) {
        try {
            localStorage.setItem(GODD_KEY, JSON.stringify(entries.slice(-GODD_MAX_ENTRIES)));
        } catch (e) {
            console.warn('DOGG Companion Lens: could not persist GODD ledger', e);
        }
    }
    function goddRecord(entry) {
        const entries = goddLoad();
        entries.push({ ...entry, at: new Date().toISOString() });
        goddSave(entries);
        return entries.length;
    }
    function goddExport() {
        const entries = goddLoad();
        const blob = new Blob([JSON.stringify({ schema: 'godd/0-ledger', entries }, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `godd-ledger-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
    function goddImport(file, onDone) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);
                const incoming = Array.isArray(data.entries) ? data.entries : (Array.isArray(data) ? data : null);
                if (!incoming) throw new Error('no entries array in file');
                const merged = goddLoad().concat(incoming);
                goddSave(merged);
                onDone({ ok: true, count: merged.length });
            } catch (err) {
                onDone({ ok: false, error: err.message });
            }
        };
        reader.onerror = () => onDone({ ok: false, error: 'could not read file' });
        reader.readAsText(file);
    }

    // -------- Companion role definitions (mirrors the published lens frame) --------
    const WORLD_ID = (document.title || location.pathname).slice(0, 60);

    const COMPANIONS = {
        overwatch: {
            icon: '🛰️', name: 'Overwatch', role: 'observer',
            render(world) {
                const hn = world.hn_top, pm = world.prediction_markets;
                const lines = [];
                if (hn) lines.push(`Top of human attention right now: "${hn.title}"`);
                if (pm && pm.top_by_volume && pm.top_by_volume[0]) {
                    const m = pm.top_by_volume[0];
                    lines.push(`Highest-volume belief market: "${m.question}" — yes @ ${m.yes_price}`);
                }
                return lines.length ? lines : ['No attention data in this frame.'];
            },
        },
        scout: {
            icon: '🐾', name: 'Scout', role: 'pathfinder',
            render(world) {
                const iss = world.iss, eq = world.earthquakes_past_hour;
                const lines = [];
                if (iss) lines.push(`ISS right now: ${iss.lat}, ${iss.lon}`);
                if (eq) lines.push(`Earthquakes in the past hour: ${eq.count} (strongest M${eq.max_mag})`);
                return lines.length ? lines : ['No planetary position data in this frame.'];
            },
        },
        forge: {
            icon: '🔨', name: 'Forge', role: 'builder',
            render(world) {
                const btc = world.btc_usd, fx = world.fx_usd, mcap = world.crypto_market, fees = world.btc_fees;
                const lines = [];
                if (btc) lines.push(`BTC/USD: $${btc.spot}`);
                if (mcap) lines.push(`Total crypto market cap: $${Number(mcap.total_mcap_usd).toLocaleString()}`);
                if (fees) lines.push(`Cheapest confirm right now: ${fees.hour_sat_vb} sat/vB`);
                if (fx) lines.push(`USD buys: €${fx.EUR} / £${fx.GBP} / ¥${fx.JPY}`);
                return lines.length ? lines : ['No economic data in this frame.'];
            },
            localAction() {
                // Each candidate returns undefined if not applicable (try the next one),
                // or true/false for an actual attempted call's real result. A previous
                // version conflated "not applicable" (undefined) with "success" here -
                // caught by testing before this ever shipped: it reported "saved" without
                // ever calling anything. Never repeat that shortcut.
                function tryCandidate(applicable, invoke) {
                    if (!applicable()) return undefined;
                    try {
                        const r = invoke();
                        return r !== false;
                    } catch (e) {
                        return false;
                    }
                }
                const candidates = [
                    () => tryCandidate(() => window.dataManager && typeof window.dataManager.save === 'function', () => window.dataManager.save()),
                    () => tryCandidate(() => window.__agentSwarmEngine && typeof window.__agentSwarmEngine.saveState === 'function', () => window.__agentSwarmEngine.saveState()),
                    () => tryCandidate(() => typeof window.saveState === 'function', () => window.saveState()),
                    () => tryCandidate(() => typeof window.save === 'function', () => window.save()),
                    () => tryCandidate(() => typeof window.saveData === 'function', () => window.saveData()),
                ];
                for (const c of candidates) {
                    const r = c();
                    if (r === undefined) continue;
                    return { attempted: true, ok: r };
                }
                return { attempted: true, ok: false };
            },
        },
        sentinel: {
            icon: '🛡️', name: 'Sentinel', role: 'guardian',
            render(world) {
                const kp = world.space_weather, carbon = world.grid_carbon_gb;
                const lines = [];
                if (kp) lines.push(`Planetary Kp index: ${kp.kp} (space weather, as of ${kp.at})`);
                if (carbon) lines.push(`UK grid carbon intensity: ${carbon.gco2_kwh} gCO2/kWh (${carbon.index})`);
                return lines.length ? lines : ['No environmental data in this frame.'];
            },
            localAction(state) {
                const fps = state.fps != null ? Math.round(state.fps) : '—';
                const peers = state.peerCount != null ? state.peerCount : '—';
                return { fps, peers };
            },
        },
    };

    // -------- Real local FPS measurement (Sentinel's own signal, no world hook needed) --------
    let liveFps = 0;
    (function trackFps() {
        let last = performance.now(), frames = 0;
        function tick(now) {
            frames++;
            if (now - last >= 1000) { liveFps = frames * 1000 / (now - last); frames = 0; last = now; }
            requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
    })();

    // -------- Real peer-presence signal, if the host Portal Hub relays one --------
    let livePeerCount = null;
    window.addEventListener('message', (ev) => {
        if (ev.data && ev.data.type === 'rapp-peers-update' && Array.isArray(ev.data.peers)) {
            livePeerCount = ev.data.peers.length;
        }
    });

    // -------- UI --------
    let panelOpen = null;
    let cachedWorldFrame = null;
    let cachedError = null;

    function injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            #rapp-companion-bar { position: fixed; bottom: 16px; right: 16px; z-index: 999999;
                display: flex; flex-direction: column; gap: 8px; font-family: 'Segoe UI', system-ui, sans-serif; }
            #rapp-companion-bar button.rapp-companion-btn {
                width: 44px; height: 44px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.35);
                background: rgba(10,10,20,0.85); color: #fff; font-size: 20px; cursor: pointer;
                display: flex; align-items: center; justify-content: center; transition: transform 0.15s;
            }
            #rapp-companion-bar button.rapp-companion-btn:hover { transform: scale(1.1); }
            #rapp-companion-bar button.rapp-companion-btn.active { border-color: #00e5ff; box-shadow: 0 0 12px rgba(0,229,255,0.6); }
            #rapp-companion-panel { position: fixed; bottom: 16px; right: 72px; z-index: 999998;
                width: 300px; max-width: 70vw; background: rgba(10,10,20,0.94); color: #eee;
                border: 1px solid rgba(255,255,255,0.25); border-radius: 10px; padding: 14px 16px;
                font-family: 'Segoe UI', system-ui, sans-serif; font-size: 13px; line-height: 1.5;
            }
            #rapp-companion-panel h4 { margin: 0 0 6px 0; font-size: 15px; }
            #rapp-companion-panel .rapp-status { font-size: 11px; opacity: 0.7; margin-bottom: 8px; }
            #rapp-companion-panel .rapp-line { margin: 4px 0; }
            #rapp-companion-panel button.rapp-action { margin-top: 8px; font-size: 11px; padding: 4px 8px;
                background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3); color: #eee;
                border-radius: 5px; cursor: pointer; }
        `;
        document.head.appendChild(style);
    }

    function buildBar() {
        const bar = document.createElement('div');
        bar.id = 'rapp-companion-bar';
        for (const [id, c] of Object.entries(COMPANIONS)) {
            const btn = document.createElement('button');
            btn.className = 'rapp-companion-btn';
            btn.title = `Summon ${c.name}`;
            btn.textContent = c.icon;
            btn.addEventListener('click', () => togglePanel(id, btn));
            bar.appendChild(btn);
        }
        document.body.appendChild(bar);
        avoidCollisions(bar);
        window.addEventListener('resize', () => avoidCollisions(bar));
    }

    // Every host world reserves ITS OWN corner for its native HUD, and which
    // corner varies per world (checked across all 11 - no single fixed corner
    // is universally free; one world's own Export/Import/Reset row sat exactly
    // where this bar defaulted to). Rather than guess or hardcode a per-world
    // exception, detect a real visual collision at runtime and nudge clear of
    // it - this stays correct for worlds this lens hasn't been checked against
    // yet, including future ones.
    function avoidCollisions(bar) {
        const MAX_ITERATIONS = 6;
        const MARGIN = 12;
        for (let i = 0; i < MAX_ITERATIONS; i++) {
            const barRect = bar.getBoundingClientRect();
            const blocker = [...document.body.querySelectorAll('*')].find(el => {
                if (el === bar || bar.contains(el)) return false;
                const style = getComputedStyle(el);
                if (style.position !== 'fixed' && style.position !== 'absolute') return false;
                const r = el.getBoundingClientRect();
                // Ignore near-full-viewport containers (overlay wrappers) - a real
                // HUD control is a small, bounded element, not a screen-sized div.
                if (r.width === 0 || r.height === 0) return false;
                if (r.width > window.innerWidth * 0.6 && r.height > window.innerHeight * 0.6) return false;
                return !(r.right < barRect.left || r.left > barRect.right || r.bottom < barRect.top || r.top > barRect.bottom);
            });
            if (!blocker) return;
            const bRect = blocker.getBoundingClientRect();
            // Push the bar up just enough that its bottom edge clears the
            // blocker's top edge, with a margin. Computed directly in viewport
            // coordinates rather than accumulated deltas - much easier to get
            // right and to verify.
            const neededBottom = Math.round(window.innerHeight - bRect.top + MARGIN);
            const currentBottom = parseFloat(getComputedStyle(bar).bottom) || 16;
            if (neededBottom <= currentBottom) return; // already clear; avoid drifting further
            bar.style.bottom = neededBottom + 'px';
        }
    }

    async function togglePanel(id, btn) {
        document.querySelectorAll('#rapp-companion-bar button').forEach(b => b.classList.remove('active'));
        const existing = document.getElementById('rapp-companion-panel');
        if (existing) existing.remove();
        if (panelOpen === id) { panelOpen = null; return; }
        panelOpen = id;
        btn.classList.add('active');

        const panel = document.createElement('div');
        panel.id = 'rapp-companion-panel';
        const c = COMPANIONS[id];
        panel.innerHTML = `<h4>${c.icon} ${c.name}</h4><div class="rapp-status">verifying live DOGG data…</div>`;
        document.body.appendChild(panel);

        try {
            if (!cachedWorldFrame && !cachedError) {
                try {
                    cachedWorldFrame = await fetchLatestVerifiedWorldFrame();
                } catch (e) {
                    cachedError = e.message;
                }
            }
            const statusEl = panel.querySelector('.rapp-status');
            if (cachedWorldFrame) {
                statusEl.textContent = `✅ verified live — tick ${cachedWorldFrame.payload.tick}, frame ${cachedWorldFrame.frame_hash.slice(0, 10)}…`;
                const lines = c.render(cachedWorldFrame.payload.world);
                for (const line of lines) {
                    const div = document.createElement('div');
                    div.className = 'rapp-line';
                    div.textContent = line;
                    panel.appendChild(div);
                }
                const count = goddRecord({
                    companion: id, world: WORLD_ID, tick: cachedWorldFrame.payload.tick,
                    frame_hash: cachedWorldFrame.frame_hash,
                });
                const goddLine = document.createElement('div');
                goddLine.className = 'rapp-status';
                goddLine.style.marginTop = '8px';
                goddLine.textContent = `GODD ledger: ${count} verified summons recorded on this device.`;
                panel.appendChild(goddLine);

                const goddRow = document.createElement('div');
                goddRow.style.display = 'flex';
                goddRow.style.gap = '6px';
                const exportBtn = document.createElement('button');
                exportBtn.className = 'rapp-action';
                exportBtn.textContent = 'Export ledger';
                exportBtn.addEventListener('click', () => goddExport());
                const importBtn = document.createElement('button');
                importBtn.className = 'rapp-action';
                importBtn.textContent = 'Import ledger';
                importBtn.addEventListener('click', () => {
                    const input = document.createElement('input');
                    input.type = 'file';
                    input.accept = '.json';
                    input.addEventListener('change', () => {
                        if (!input.files[0]) return;
                        goddImport(input.files[0], (r) => {
                            importBtn.textContent = r.ok ? `✅ merged (${r.count} total)` : '⚠️ ' + r.error;
                        });
                    });
                    input.click();
                });
                goddRow.appendChild(exportBtn);
                goddRow.appendChild(importBtn);
                panel.appendChild(goddRow);
            } else {
                statusEl.textContent = `⚠️ could not verify live DOGG data (${cachedError}). ${c.name} has nothing real to say right now.`;
            }

            if (id === 'forge') {
                const btnEl = document.createElement('button');
                btnEl.className = 'rapp-action';
                btnEl.textContent = 'Ask Forge to save this world';
                btnEl.addEventListener('click', () => {
                    const r = c.localAction();
                    btnEl.textContent = r.ok ? '✅ saved' : '⚠️ no save function found in this world';
                });
                panel.appendChild(btnEl);
            }
            if (id === 'sentinel') {
                const div = document.createElement('div');
                div.className = 'rapp-line';
                const r = c.localAction({ fps: liveFps, peerCount: livePeerCount });
                div.textContent = `Local session: ${r.fps} fps, ${r.peers === null ? 'no hub presence signal' : r.peers + ' peer(s) in this world'}`;
                panel.appendChild(div);
            }
        } catch (e) {
            panel.querySelector('.rapp-status').textContent = 'Sentinel-visible error: ' + e.message;
        }
    }

    function init() {
        injectStyles();
        buildBar();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
