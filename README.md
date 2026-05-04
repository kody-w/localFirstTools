# Local First Tools 🛠️

A curated collection of **100+ self-contained HTML applications**. Every tool is one HTML file you can open directly in your browser, with no build step. Data stays local in your browser; everything keeps working when you're offline.

**CDNs are welcome.** "Local-first" describes where your *data* lives — not a ban on libraries. Apps freely pull Three.js, PeerJS, sql.js, WebLLM, qrcodejs, HTMX, etc. from CDNs when those libraries make the app dramatically better.

https://kody-w.github.io/localFirstTools/index.html


[![License](https://img.shields.io/badge/License-MIT-8338ec?style=for-the-badge)](LICENSE)

![Local First Tools Gallery](https://via.placeholder.com/1200x400/0a0a0a/06ffa5?text=Local+First+Tools+Gallery)

## ✨ Features

- **🔒 Local-First Data**: Every app stores your data in your browser, not on a server
- **📦 Self-Contained**: Each HTML file is a complete application — open and go
- **⚡ Zero Build Step**: No npm, no webpack, no compilation
- **🌐 CDN-Powered When Useful**: Three.js, PeerJS, WebLLM, sql.js, etc. via CDN when they make the app better
- **🎨 Beautiful Gallery**: Browse tools in a modern, animated gallery interface
- **🪐 3D Experience**: Walk through the collection in an immersive Three.js gallery
- **📥 Import/Export**: Full JSON import/export for data portability
- **🎮 100+ Tools**: Games, creative tools, productivity apps, P2P experiments, AI tools, and more

## 🆕 Recently added (May 2026)

A sister fork's parallel-build session landed in [PR #11](https://github.com/kody-w/localFirstTools/pull/11) with 16 new showcase apps + a systematic bug fix for 60 occurrences of an `<a href="../../${url}">` href construction bug across 26 existing apps.

**Showcase apps:**

| Try it | What it is |
|---|---|
| [🌀 Portal Hub](https://kody-w.github.io/localFirstTools/apps/quantum-worlds/portal-hub.html) | Three.js + PeerJS meta-universe linking 10 quantum worlds. Walk through portals, see other peers as glowing capsules, share rooms via QR. |
| [🤖 Local LLM](https://kody-w.github.io/localFirstTools/apps/ai-tools/local-llm.html) | WebGPU + WebLLM. First load downloads & caches the model in OPFS (~1.5GB, takes a few minutes); after that it's fully offline. |
| [🛠️ App-Forge](https://kody-w.github.io/localFirstTools/apps/ai-tools/app-forge.html) | Natural language → single-file app. Pair with `scripts/forge-bridge.py` (run on `127.0.0.1:7711`) for end-to-end agent build. |
| [🎨 Mesh-Board](https://kody-w.github.io/localFirstTools/apps/productivity/mesh-board.html) | Yjs CRDT over PeerJS — infinite canvas with embedded iframe widgets. Two browsers, one shared whiteboard, no server. |
| [📼 Session Recorder](https://kody-w.github.io/localFirstTools/apps/development/session-recorder.html) | Records any iframe-loaded app at 30Hz mutation deltas; replays frame-by-frame. |
| [🔐 SQL Time-Capsule](https://kody-w.github.io/localFirstTools/apps/development/sql-time-capsule.html) | sql.js + SHA-256 Merkle-chained query log. Tamper-evident replayable database history. |
| [🎵 Symphonic Defense](https://kody-w.github.io/localFirstTools/apps/games/symphonic-defense.html) | Tower defense where waves and tower abilities are driven by audio-synth tracks. |
| [⚔️ P2P Battle Arena](https://kody-w.github.io/localFirstTools/apps/p2p-world/p2p-battle-arena.html) | Real-time browser-to-browser battle game over PeerJS, no server required. |
| [🎉 Party Planner Network](https://kody-w.github.io/localFirstTools/apps/p2p-world/party-planner-network.html) | Distributed party planning with shared state synced over PeerJS. |
| [👁️ Synesthesia](https://kody-w.github.io/localFirstTools/apps/media/synesthesia.html) | Webcam → Web Audio synth; 750 B–1.5 KB per minute streamed audio-visual feed. |
| [🏆 Unified Leaderboard](https://kody-w.github.io/localFirstTools/apps/business/unified-leaderboard.html) | Subscribes to the `'score'` telepathy channel (BroadcastChannel + localStorage fallback) and persists best scores cross-tab. |
| [🎯 Gallery — For You](https://kody-w.github.io/localFirstTools/apps/utilities/gallery-foryou.html) | TF-IDF + dwell-time-weighted recommender. Surfaces relevant apps as you browse. |
| [🪄 NL Patcher](https://kody-w.github.io/localFirstTools/apps/utilities/nl-patcher.html) | Natural-language → CSS/text patches persisted to localStorage; live re-apply. |
| [📡 Telepathy Bus](https://kody-w.github.io/localFirstTools/apps/utilities/telepathy-bus.html) | Cross-app pub/sub demo via BroadcastChannel + localStorage fallback. |
| [🗄️ DB Viewer](https://kody-w.github.io/localFirstTools/apps/development/db-viewer.html) | Browse/query in-browser databases (IndexedDB, OPFS, sql.js). |
| [🎨 Vibe Coding Gallery](https://kody-w.github.io/localFirstTools/apps/index-variants/vibe-coding-gallery.html) | Alternative experimental gallery layout with a vibe-driven discovery flow. |

**Try the cross-app pub/sub demo:** open [`/snake3.html`](https://kody-w.github.io/localFirstTools/snake3.html) and [`/apps/business/unified-leaderboard.html`](https://kody-w.github.io/localFirstTools/apps/business/unified-leaderboard.html) side-by-side. Play snake; the leaderboard updates live via `BroadcastChannel('score')` with no shared backend.

**Backwards-compat:** old `?room=<id>` P2P share links (`/index.html?room=abc`) still work — the gallery has a JS shim that redirects them to `apps/p2p-world/networked-world.html` with the room param preserved.

## 🚀 Quick Start

### Option 1: Use Online
Visit the live gallery: **[kody-w.github.io/localFirstTools](https://kody-w.github.io/localFirstTools)**

### Option 2: Run Locally
```bash
# Clone the repository
git clone https://github.com/kody-w/localFirstTools.git
cd localFirstTools

# Start a local server
python3 -m http.server 8000

# Open in browser
open http://localhost:8000
```

### Option 3: Use Individual Tools
Each HTML file can be opened directly in your browser without any server. Just download and double-click!

## 📂 Project Structure

```
localFirstTools/
├── index.html                    # Main gallery launcher
├── vibe_gallery_config.json      # Auto-generated app registry
├── tools-manifest.json           # Simple tool listing
├── [100+ HTML apps]              # Self-contained applications
├── vibe_gallery_updater.py       # Gallery metadata extractor
├── update-tools-manifest.py      # Manifest generator
└── CLAUDE.md                     # Developer guide
```

## 🎨 Application Categories

The gallery organizes applications into 9 thematic categories:

| Category | Description | Examples |
|----------|-------------|----------|
| 🎨 **Visual Art** | Interactive visual experiences and design tools | Drawing apps, SVG editors, color palettes |
| 🌌 **3D & Immersive** | Three-dimensional and WebGL experiences | 3D worlds, VR experiences, games |
| 🎵 **Audio & Music** | Sound synthesis and music creation | Drum machines, synthesizers, audio tools |
| 🎮 **Games & Puzzles** | Interactive games and playful experiences | Card games, arcade games, puzzles |
| 🤖 **Experimental AI** | AI-powered interfaces and demos | Chatbots, AI assistants, automation |
| 🛠️ **Creative Tools** | Productivity and creative utilities | Text editors, todo apps, converters |
| 🌀 **Generative Art** | Algorithmic art generation systems | Procedural art, fractals, patterns |
| ⚛️ **Particle & Physics** | Physics simulations and particle systems | Physics engines, particle effects |
| 📚 **Educational** | Learning resources and tutorials | Interactive tutorials, demos |

## 🛠️ Development

### Adding a New Application

1. **Create a self-contained HTML file** following the structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your App Name</title>
    <meta name="description" content="Brief description">
    <style>
        /* All CSS inline here */
    </style>
</head>
<body>
    <!-- Your app UI -->
    <script>
        /* All JavaScript inline here */
    </script>
</body>
</html>
```

2. **Save to the root directory** with a descriptive name: `my-awesome-tool.html`

3. **Update the gallery**:
```bash
python3 vibe_gallery_updater.py
```

4. **Refresh the gallery** to see your new tool!

### Key Principles

- ✅ **Self-Contained**: Each app is one HTML file (CSS and JavaScript inline)
- ✅ **No Build Step**: Open in any browser; no npm install, no webpack
- ✅ **External Libraries via CDN are fine**: Use Three.js, PeerJS, WebLLM, sql.js, qrcodejs, HTMX, etc. when they help
- ✅ **Local-First Data**: User data lives in localStorage / IndexedDB / OPFS — not on a server
- ✅ **Data Import/Export**: Include JSON import/export so users can move state between devices
- ✅ **Responsive Design**: Works on desktop and mobile devices

### Development Commands

```bash
# Update gallery configuration (extracts metadata from all HTML files)
python3 vibe_gallery_updater.py

# Quick shell wrapper
./update-gallery.sh

# Update tools manifest
python3 update-tools-manifest.py

# Watch for changes and auto-update
python3 vibe_gallery_watcher.py

# Run once and exit
python3 vibe_gallery_watcher.py --once

# Organize files into categories
python3 vibe_gallery_organizer.py

# Preview mode (shows what would be organized)
python3 vibe_gallery_organizer.py --dry-run
```



## 🧱 Frame machine surfaces

The repo now includes two frame-pattern tools that treat raw JSON pulled from the public repo as globally accessible state:

- **`dynamics365-frame-machine.html`** — the Dynamics 365 proof, now living here as a portable frame machine with GitHub raw overlays from the public repo, liquid fork dimensions, import/export backups, and a lockstep twin console.
- **`hacker-news-simulator.html`** — a repaired Hacker News simulator that now runs as a frame machine over `data/content/hacker-news-posts.json`, with fork-aware liquid dimensions and bundle backup and reimport flows.

These pages are not just demos. They treat the raw files as the canonical medium, which means the state stays publicly available in the repo, forks can export a bundle, change it locally, and import it back without losing the business logic flow carried by the frames. That backup and reimport loop is part of the frame contract, not an afterthought.
## 🎯 Auto-Categorization

The gallery automatically categorizes applications based on code analysis:

- **Keywords Detection**: Scans for technology-specific keywords (3D, canvas, audio, game, etc.)
- **Metadata Extraction**: Pulls title, description from HTML tags
- **Complexity Analysis**: Determines simple/intermediate/advanced based on file size and features
- **Interaction Type**: Identifies as game, drawing, visual, interactive, audio, or interface

### Influencing Auto-Categorization

Include relevant keywords in your HTML:

```html
<!-- Keywords: 3d, canvas, animation, physics -->
```

Or use specific technologies in your code:
- **3D/WebGL**: `three.js`, `webgl`, `perspective`
- **Canvas**: `canvas`, `getContext`
- **Audio**: `webaudio`, `audiocontext`
- **Game**: `game`, `score`, `player`, `level`
- **Interactive**: `click`, `drag`, `touch`
- **Generative**: `random`, `generate`, `procedural`

## 🏗️ Architecture

### Local-First Philosophy

Every application in this collection follows these principles:

1. **Privacy by Design**: User data lives in your browser, not on a server
2. **Offline Functionality**: Apps keep working when you're offline (after the first load)
3. **CDN-Powered When It Helps**: External libraries (Three.js, PeerJS, sql.js, WebLLM, etc.) are loaded from CDNs when they make the app dramatically better
4. **Data Ownership**: You control your data through JSON import/export
5. **No Build Process**: Open in any browser, no compilation needed

### Gallery System

The gallery uses a dual-config system:

- **`vibe_gallery_config.json`**: Rich metadata with categories, tags, complexity
- **`tools-manifest.json`**: Simple file listing with timestamps

Both are auto-generated by scanning HTML files in the repository.

## 📱 Browser Compatibility

- ✅ Chrome/Edge (latest 2 versions)
- ✅ Firefox (latest 2 versions)
- ✅ Safari (latest 2 versions)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Add New Tools**: Create self-contained HTML applications
2. **Improve Existing Tools**: Enhance features, fix bugs, improve UX
3. **Documentation**: Improve guides, add examples, create tutorials
4. **Testing**: Report bugs, test on different browsers/devices

### Contribution Guidelines

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-tool`)
3. Follow the development principles (self-contained, offline-first, no dependencies)
4. Test in multiple browsers
5. Update the gallery (`python3 vibe_gallery_updater.py`)
6. Commit your changes (`git commit -m 'Add amazing tool'`)
7. Push to the branch (`git push origin feature/amazing-tool`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Built with vanilla HTML, CSS, and JavaScript
- 3D gallery powered by [Three.js](https://threejs.org/) (only external dependency in gallery)
- Inspired by the local-first software movement

## 🔗 Links

- **Gallery**: [kody-w.github.io/localFirstTools](https://kody-w.github.io/localFirstTools)
- **Repository**: [github.com/kody-w/localFirstTools](https://github.com/kody-w/localFirstTools)
- **Issues**: [github.com/kody-w/localFirstTools/issues](https://github.com/kody-w/localFirstTools/issues)

## 📊 Stats

![Tools Count](https://img.shields.io/badge/Tools-100+-06ffa5?style=flat-square)
![Categories](https://img.shields.io/badge/Categories-9-8338ec?style=flat-square)
![No Dependencies](https://img.shields.io/badge/Dependencies-0-ff006e?style=flat-square)
![Offline First](https://img.shields.io/badge/Offline-100%25-06ffa5?style=flat-square)

---

**Made with ❤️ for the local-first community**
