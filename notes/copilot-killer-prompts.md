# 10 Copilot CLI prompts that show off this repo

Each prompt is paste-ready into `copilot` (autopilot mode recommended). They're tuned to this repo's superpowers: single-file HTML, ~100 existing apps, the gallery registry at `data/config/utility_apps_config.json`, PeerJS+Three.js already in use, and the Copilot subagents in `.claude/agents/`.

---

## 1. Recursive Gallery Singularity
> Make the gallery learn me. In `apps/utilities/index_sorting.html`, instrument every app open/close with a 1ms localStorage event log. On gallery load, build a TF-IDF + cosine-similarity recommender from each app's title/description/tags, weight it by my dwell-time history, and prepend a "For You" row. The whole pipeline must run offline in <50ms cold and rebuild incrementally on every click. Export my taste profile as JSON. No external libraries.

**Why it's mind-blowing:** A self-improving local-first recommender that works in airplane mode and never phones home.

---

## 2. Cross-App Telepathy Bus
> Add a single hidden file `apps/utilities/telepathy-bus.html` that exposes `window.bus.publish(channel, data)` / `window.bus.subscribe(channel, fn)` to any embedded gallery app via `BroadcastChannel` + a localStorage fallback. Then patch three existing games (`apps/games/snake3.html`, `apps/games/balatro-clone.html`, `apps/games/gameoflife.html`) to broadcast their score on `score` channel. Build `apps/business/unified-leaderboard.html` that subscribes and shows live rankings across all three games running in adjacent tabs. Update the registry.

**Why it's mind-blowing:** Turns the existing 100 apps into a programmable, message-passing operating system without touching the build system (there isn't one).

---

## 3. Hub of 10 Quantum Worlds
> Stitch every file in `apps/quantum-worlds/` into one P2P meta-universe. Create `apps/quantum-worlds/portal-hub.html`: a Three.js scene with 10 portals, each lazy-loading the corresponding world into an iframe when entered. Avatars and chat sync via PeerJS mesh (use the same pattern as `apps/p2p-world/p2p-battle-arena.html`). Crossing a portal teleports your peer presence into that world's scene. The hub itself is a quantum world too, listed in `quantum-worlds-store.html`.

**Why it's mind-blowing:** 10 separate 3D universes become one navigable multiverse, all single-file, all peer-to-peer.

---

## 4. App-Forge: NL → working HTML app
> Create `apps/ai-tools/app-forge.html`. User types a one-line idea ("a vampire pomodoro timer where blood drips during breaks"). The page shells out to `copilot` via a `child_process` bridge (write a tiny `scripts/forge-bridge.py` server on `localhost:7711`), invokes the `local-first-app-builder` subagent from `.claude/agents/`, streams the LLM's reasoning into the page as a typewriter, and on completion drops the new HTML into the right `apps/<category>/` folder, runs `python3 scripts/intelligent_organizer.py --execute` to update the registry, and pops a "Open it now" button.

**Why it's mind-blowing:** A web app that builds web apps, using the agent infrastructure already shipped in this repo.

---

## 5. Session Time Machine
> Build `apps/development/session-recorder.html`. Loads any other gallery app in a sandboxed iframe, hooks `localStorage`, `IndexedDB`, mouse, keyboard, and `MutationObserver` events, and writes a delta-compressed event stream to IndexedDB. Provide a Figma-style timeline scrubber that replays any recording at 0.25×–8× speed. Export = a single JSON, importable on any other machine to reproduce the session pixel-for-pixel offline. Use it to record yourself beating a level of `apps/games/snake3.html` and ship the .json as proof.

**Why it's mind-blowing:** Turns every existing app into a replayable demo with zero modifications to the apps themselves.

---

## 6. Local LLM in the browser, no server
> Create `apps/ai-tools/local-llm.html` using WebGPU + a vendored quantized model (Phi-3-mini-q4 via WebLLM, fetched once and stored in OPFS). All inference happens on-device. Conversation history persists in IndexedDB. If WebGPU isn't available, fall back to a 3MB ggml WASM build. After the first load the app must work in airplane mode forever. Add a "private" badge that lights up only when `navigator.onLine === false` to prove it.

**Why it's mind-blowing:** A real LLM chat in a single self-contained HTML file. The "private" badge proving offline operation is the punchline.

---

## 7. Mesh Whiteboard Workspace
> Create `apps/productivity/mesh-board.html`: an infinite canvas where I can drag *any* gallery app from a side panel onto the board as a live interactive iframe widget. Position, size, z-order, and each iframe's `localStorage` snapshot are CRDT-synced over a PeerJS mesh — vendor Automerge inline (~80KB minified, base64-embed it). JSON export captures the layout AND a snapshot of every embedded app's storage so I can hand a teammate a single `workspace.json` that recreates my entire desk including in-progress game states.

**Why it's mind-blowing:** A multi-user collaborative OS where the windows are real apps, not mockups, and the whole workspace is one portable JSON.

---

## 8. Webcam Synesthesia Engine
> Build `apps/media/synesthesia.html`: getUserMedia → analyze every frame with a 32×32 RGB histogram + Sobel edges + frame-diff motion. Map: dominant hue → oscillator frequency, saturation → filter cutoff, edge density → percussion intensity, motion magnitude → reverb wet. All Web Audio, all real-time, all offline, no libraries. Save "compositions" as 2KB/min JSON deltas. On replay, regenerate the audio from the deltas without needing the camera again.

**Why it's mind-blowing:** Your webcam becomes an instrument. The composition format is so lean it fits in a tweet.

---

## 9. Natural-Language Patch Overlay System
> Make every gallery app live-tweakable from inside itself. Inject a tiny floating "✏️ tweak" button into any app loaded through the gallery. Click it, type plain English ("make the snake purple and 2x bigger", "add a dark mode toggle"). A rule engine in `apps/utilities/nl-patcher.html` translates the request into a CSS+regex+JS overlay, saves it to localStorage as `${appId}.patch`, and applies it on every future load. The original HTML on disk is never touched. Export `.patch.json` to share patches with friends. Bonus: a "patch marketplace" page that lists everyone's shared patches.

**Why it's mind-blowing:** The entire gallery becomes user-modifiable without ever editing source files. Patches are portable, shareable, stackable.

---

## 10. SQL Time-Capsule
> Create `apps/development/sql-time-capsule.html` using vendored sql.js. Full SQL editor with schema designer, query history, CSV/JSON import. Killer feature: every executed query is appended to a Merkle-chained log (each entry hashes the previous), making the history tamper-evident. Export = one self-contained HTML file with the database state AND the signed query log embedded as base64. Recipient opens the exported file offline and can press "replay" to watch every query execute in order, with the data evolving in real time. Verify integrity on replay; refuse to replay tampered logs.

**Why it's mind-blowing:** A database, its history, and the means to verifiably replay that history — all in one HTML file you can email.

---

## How to use these

```bash
copilot --experimental    # then Shift+Tab into autopilot
> [paste any prompt above]
```

For the most ambitious ones (#3, #4, #6, #7, #10), expect 30–90 minutes of agent work and several MB of vendored assets. For #1, #2, #5, #8, #9, expect to see results in 5–15 minutes.

Each prompt deliberately:
- stays inside this repo's single-file HTML constraint,
- updates `data/config/utility_apps_config.json` via the existing scanner,
- uses tech the repo already ships (PeerJS, Three.js, localStorage import/export),
- produces something that genuinely couldn't exist as a single file in any other architecture.
