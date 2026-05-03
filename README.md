# localFirstTools

A growing collection of **single-file HTML applications** that run entirely in your browser, with no servers and no build step. Plenty of apps freely use external libraries via CDN (Three.js, PeerJS, sql.js, WebLLM, qrcodejs, Yjs, HTMX, etc.) — that's exactly what CDNs are for. The "local-first" name describes where your *data* lives (in your browser, not on a server), not a ban on libraries.

Open the gallery, pick an app, and press **Save** to download the HTML for fully-offline use. Your data stays in `localStorage`; every app exposes JSON import/export so you can move it between devices.

## Run it

```bash
git clone https://github.com/kody-w/localFirstTools.git
cd localFirstTools
python3 -m http.server 8000
# then open http://localhost:8000
```

Opening `index.html` directly with `file://` won't list the apps, because the gallery uses `fetch()` to load the registry. Any HTTP server works; the Python one-liner is just the smallest.

## What's in here

| Category | Examples |
|---|---|
| `apps/games/` | Snake-3D, Balatro clone, retro consoles, P2P battle arena |
| `apps/productivity/` | Mesh-board (collaborative whiteboard), Pomodoro timers, todo lists |
| `apps/ai-tools/` | Local LLM chat (WebGPU, fully offline after first load), agent dashboards, NL→app forge |
| `apps/development/` | Session recorder, SQL time-capsule with Merkle-chain tamper detection, DB viewer |
| `apps/utilities/` | "For You" recommender, cross-app pub/sub bus, NL patcher, telepathy bus |
| `apps/quantum-worlds/` | Three.js + PeerJS shared 3D experiences, with a portal hub |
| `apps/p2p-world/` | The original P2P networked world (root `?room=…` links redirect here) |
| `apps/media/`, `apps/health/`, `apps/business/`, `apps/education/` | More single-file experiments |

The registry at `data/config/utility_apps_config.json` is the source of truth — currently 156+ apps.

## Add an app

1. Save your HTML to `apps/<category>/<descriptive-kebab-case-name>.html`. Keep all CSS/JS inline.
2. Add a real `<title>` and `<meta name="description" content="…">` (and optionally `<meta name="keywords" content="…">`, `<meta name="icon" content="🎯">`). The registry generator extracts these directly.
3. Include JSON import/export controls (see [`.claude/agents/local-first-app-builder.md`](.claude/agents/local-first-app-builder.md) for the canonical pattern).
4. Run `python3 scripts/regenerate_registry.py` to refresh the gallery. Add `--check` to fail on duplicate IDs, `--dry-run` to preview.

## Architecture in one breath

- **One HTML file = one app.** No build, no bundler, no `node_modules`.
- **Persistence is `localStorage`**, scoped per app. No backend exists.
- **Every app must offer JSON import/export.** That's the only "cloud sync."
- **CDN exceptions are explicit and minimal** — see `.github/copilot-instructions.md` for the full list. New utility/productivity/business apps must be CDN-free.

## Repo layout

```
.
├── index.html                            ← the gallery launcher
├── apps/<category>/<name>.html           ← every app
├── data/
│   ├── config/utility_apps_config.json   ← gallery registry (auto-generated)
│   └── games/*.json                      ← game cartridges
├── scripts/
│   ├── regenerate_registry.py            ← read-only registry generator
│   └── forge-bridge.py                   ← optional NL→app forge server (port 7711)
├── archive/                              ← deprecated experiments, kept for provenance
├── edgeAddons/xbox-mkb-extension/        ← real Chromium MV3 extension
├── notes/                                ← brainstorming + dev notes (not shipped to gallery)
├── vibe_templates/                       ← unrelated bootstrap-template subproject
├── .claude/agents/                       ← Claude Code subagent definitions
├── CLAUDE.md                             ← Claude-Code-specific guidance
└── .github/copilot-instructions.md       ← Copilot-specific guidance
```

## License

Personal collection; see individual files for any embedded notices.
