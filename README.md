# Local First Tools 🛠️

A curated collection of **100+ self-contained HTML applications** following the "local-first" philosophy. Every tool works completely offline, with no external dependencies, no build process, and no tracking.

https://kody-w.github.io/localFirstTools/index.html


[![License](https://img.shields.io/badge/License-MIT-8338ec?style=for-the-badge)](LICENSE)

![Local First Tools Gallery](https://via.placeholder.com/1200x400/0a0a0a/06ffa5?text=Local+First+Tools+Gallery)

## ✨ Features

- **🔒 Offline-First**: Every application works completely offline
- **🎯 Zero Dependencies**: No CDN links, no npm packages, no build process
- **📦 Self-Contained**: Each HTML file is a complete application
- **🎨 Beautiful Gallery**: Browse tools in a modern, animated gallery interface
- **🌐 3D Experience**: Explore tools in an immersive 3D virtual gallery
- **💾 Data Privacy**: All data stays local in your browser
- **📥 Import/Export**: Full JSON import/export for data portability
- **🎮 100+ Tools**: Games, creative tools, productivity apps, and more

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

- ✅ **Self-Contained**: All CSS and JavaScript must be inline
- ✅ **No External Dependencies**: No CDN links, no npm packages
- ✅ **Offline-First**: Must work without internet connection
- ✅ **Data Import/Export**: Include JSON import/export functionality
- ✅ **Responsive Design**: Works on desktop and mobile devices
- ✅ **Local Storage**: Use browser localStorage for persistence

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

Every application in this collection adheres to these principles:

1. **Privacy by Design**: No data leaves your browser
2. **Offline Functionality**: Works without internet connection
3. **No External Dependencies**: Self-contained and portable
4. **Data Ownership**: You control your data through import/export
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
