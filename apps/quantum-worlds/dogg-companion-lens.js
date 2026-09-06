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

    // -------- rapp/1 canonical hashing (validated byte-for-byte against the real
    // Python reference implementation on live ASCII, unicode, and tampered frames
    // before this file was ever deployed) --------
    function canonical(v) {
        if (v === null || typeof v === 'boolean') return JSON.stringify(v);
        if (typeof v === 'number') {
            if (!Number.isInteger(v)) throw new Error('floats not supported in this profile');
            return JSON.stringify(v);
        }
        if (typeof v === 'string') return JSON.stringify(v);
        if (Array.isArray(v)) return '[' + v.map(canonical).join(',') + ']';
        if (typeof v === 'object') {
            const keys = Object.keys(v).sort();
            return '{' + keys.map(k => JSON.stringify(k) + ':' + canonical(v[k])).join(',') + '}';
        }
        throw new Error('non-serializable value: ' + typeof v);
    }

    async function sha256Hex(str) {
        const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
        return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
    }

    async function H(space, v) {
        return sha256Hex(space + '\n' + canonical(v));
    }

    async function verifyFrame(frame) {
        try {
            const payloadHash = await H('rapp/1:particle', frame.payload);
            if (payloadHash !== frame.payload_hash) return { ok: false, reason: 'payload_hash mismatch' };
            const pre = {};
            for (const k of Object.keys(frame)) if (k !== 'frame_hash' && k !== 'sig') pre[k] = frame[k];
            const frameHash = await H('rapp/1:wave', pre);
            if (frameHash !== frame.frame_hash) return { ok: false, reason: 'frame_hash mismatch' };
            return { ok: true };
        } catch (e) {
            return { ok: false, reason: 'verify threw: ' + e.message };
        }
    }

    async function fetchJson(url) {
        const controller = new AbortController();
        const t = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
        try {
            const res = await fetch(url, { signal: controller.signal, cache: 'no-store' });
            if (!res.ok) throw new Error('HTTP ' + res.status);
            return await res.json();
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
            frame = JSON.parse(lines[lastSeq - k * E]);
        } else {
            frame = await fetchJson(`${DOGG_RAW}/world/${lastSeq}.json`);
        }
        const v = await verifyFrame(frame);
        if (!v.ok) throw new Error('world frame failed verification: ' + v.reason);
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
