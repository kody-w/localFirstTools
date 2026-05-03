# Copilot instructions for localFirstTools

This repo is a collection of self-contained HTML "apps" launched from a gallery. There is **no build system, no package manager, no test runner, and no lint config**. Treat each app as an independent artifact.

## Architecture (read this first)

- **Each app is a single HTML file** with all CSS and JavaScript inlined. Never split an app into separate `.css`/`.js`/asset files. If you need an image, base64-encode it inline.
- Apps live under `apps/<category>/<name>.html`. Categories in active use: `games/`, `productivity/`, `business/`, `development/`, `media/`, `education/`, `ai-tools/`, `health/`, `utilities/`, `p2p-world/`, `quantum-worlds/`, `index-variants/`.
- **The gallery launcher discovers apps from `data/config/utility_apps_config.json`** (`apps[]` array of `{id, title, description, tags, path, icon, category, aliases?}`). Paths look like `./apps/<category>/<file>.html`. Regenerate via `python3 scripts/regenerate_registry.py` (read-only directory scan); do not hand-edit it.
- The launcher fetches that JSON at runtime (root `index.html` ~line 1820). That `fetch` is why the project must be served over HTTP for the gallery to work — opening it via `file://` will silently fail to list apps.
- Persistence is **always** `localStorage` keyed per-app. There is no backend. Every app should expose JSON **import/export** so users can move data between devices/browsers.
- `data/games/*.json` are game-config cartridges loaded by certain game shells; when adding a game-config-driven app, follow the existing JSON shape rather than inventing a new one.

## Root `index.html` IS the gallery

The root `index.html` is the gallery launcher. The previous P2P-world content was moved to `apps/p2p-world/networked-world.html` to free up root for the gallery. Old share links of shape `/index.html?room=…` still work via a redirect shim at the top of the gallery's first `<script>` block — leave that shim alone when editing the launcher.

The launcher reads metadata directly from the registry. `generateArtworkMetadata()` (around line 1330) prefers `_registryEntry.title / description / icon / tags` when the local-config branch loaded successfully, and falls back to filename-hash synthesis only when running against the live GitHub tree. **When you edit the launcher, preserve this preference order** — otherwise users see synthesized "Vibe coding at its finest" text instead of real titles.

The old path `apps/utilities/index_sorting.html` is now a thin redirect stub that forwards to `../../index.html`. Don't restore real launcher code there.

## "Local-first" — the rule and the real exceptions

`CLAUDE.md` states "no CDN links, no npm packages." That holds for the **vast majority** of apps and any new productivity/utility/business app you add. However, a handful of 3D/P2P apps in this repo (`apps/p2p-world/*`, `apps/quantum-worlds/quantum-worlds-store.html`, `apps/quantum-worlds/portal-hub.html`, several `apps/games/*` worlds, plus three new showcase apps that depend on WebGPU/Yjs/sql.js: `apps/ai-tools/local-llm.html`, `apps/productivity/mesh-board.html`, `apps/development/sql-time-capsule.html`) **do** load Three.js, PeerJS, jsQR, qrcodejs, WebLLM, Yjs, or sql.js from CDNs because there is no practical inline alternative. When editing those files, leave the existing `<script src="https://cdn.jsdelivr.net/...">` tags alone; when creating a new generic app, do **not** add CDN links.

## Adding or moving an app

1. Save the file as `apps/<category>/<descriptive-kebab-case>.html` (lowercase, hyphenated — e.g. `task-tracker.html`, not `TaskTracker.html`).
2. Add a real `<title>` and `<meta name="description" content="…">` inside `<head>`. The regenerator extracts these directly from your HTML — without them you get a fallback like `"Local-first <category> app: <Humanized Name>."`. Optional: `<meta name="keywords" content="comma,separated,tags">` and `<meta name="icon" content="🎯">`.
3. Include inline import/export JSON controls. The canonical pattern (used across most apps):
   - A constant `APP_NAME` used as the `localStorage` key.
   - `exportData()` builds a `Blob` and triggers a download named `${APP_NAME}-data-${YYYY-MM-DD}.json`.
   - `importData(event)` reads the file, `JSON.parse`s it, writes to `localStorage`, and `location.reload()`s.
   - See `.claude/agents/local-first-app-builder.md` for the full template.
4. Regenerate the registry: `python3 scripts/regenerate_registry.py`. Add `--dry-run` to preview, `--check` to assert zero duplicate IDs without writing.

## Registry IDs are path-based and unique

Registry entries use `id = "<category>__<filename-stem>"` (double underscore separator). This **guarantees uniqueness** across categories and prevents the silent overwrite bug in `apps/utilities/gallery-foryou.html`'s recommender map when two apps share a filename. The previous flat filename is preserved as `aliases: ["<old-id>"]` for any consumer that needs to translate old `localStorage` keys.

If you ever rename a file, run the regenerator immediately so cross-references in `apps/quantum-worlds/portal-hub.html` and similar iframe-loaders stay in sync.

## Running and verifying

There is no test suite, no linter, no CI. "Verifying" means:

```bash
# from repo root
python3 -m http.server 8000
# open http://localhost:8000/                                — the gallery
# open http://localhost:8000/?room=abc                        — redirects to P2P world
# open http://localhost:8000/apps/<category>/<your-file>.html — your app in isolation
```

Manually exercise: offline behavior (DevTools → Network → Offline), `localStorage` persistence across reload, and the import/export round-trip. Anything that requires `fetch()` (like the gallery loading the config JSON) **must** be served over HTTP, not opened via `file://`. The gallery's "Save" button uses `fetch` against the local config path and triggers a browser download — confirm it works after any registry change.

## Auxiliary code paths

- `edgeAddons/xbox-mkb-extension/` is a real Chromium MV3 extension. Build with `./create-xbox-mkb-extension.sh` from inside that directory. Not part of the gallery; not scanned by the registry generator.
- `vibe_templates/` is a separate sub-project of bootstrap templates with its own conventions (including its own `CLAUDE.md` and `BOOTSTRAP.md`). Don't apply localFirstTools' single-file rule there.
- `artifacts/setup-artifacts-bash.sh` expects `artifacts/` at repo root — leave that folder where it is.
- `.claude/agents/*.md` define Claude Code subagents. They encode similar conventions and are good references when generating new apps from scratch.
- `archive/intelligent_organizer.py.deprecated` and `archive/organize_files.py.deprecated` are kept for provenance only. **Do not run them** — their `--execute` modes reshuffle files based on filename heuristics regardless of current placement, which silently corrupts a working layout. Use `scripts/regenerate_registry.py` instead.
- `scripts/forge-bridge.py` runs on `127.0.0.1:7711` and is paired with `apps/ai-tools/app-forge.html` for natural-language scaffolding. Stdlib-only; no external dependencies.

## File-naming conventions

- Apps: `lowercase-with-hyphens.html`
- Game cartridges in `data/games/`: `<game-name>-game.json` or `<game-name>.json`
- Shell scripts: `purpose-description.sh` (kebab-case)
- Python scripts: `purpose_description.py` (snake_case)
- When two apps would collide by filename across categories, suffix the less-canonical copy (e.g. `-world.html` for the immersive 3D variant of a game). The registry generator already de-duplicates by category, but cross-references (iframe loaders) won't — keep filenames unique to be safe.
