# localFirstTools

## **Start Using Now - No Installation Required!**

**Just want to use the apps? Click below to open the gallery in your browser:**

### **[Open localFirstTools Gallery](https://kody-w.github.io/localFirstTools/)**

All 200+ applications work directly in your browser - no downloads, no accounts, no setup. Your data stays on your device.

**Quick Links to Popular Apps:**
- [Games Collection](https://kody-w.github.io/localFirstTools/apps/games/) - 50+ browser games
- [Productivity Tools](https://kody-w.github.io/localFirstTools/apps/productivity/) - Timers, task managers, and more
- [AI Tools](https://kody-w.github.io/localFirstTools/apps/ai-tools/) - AI-powered utilities
- [Quantum Worlds](https://kody-w.github.io/localFirstTools/apps/quantum-worlds/) - P2P multiplayer 3D universes

**Example:** Play a game directly at:
`https://kody-w.github.io/localFirstTools/apps/games/levi.html`

---

## For Developers

### Project Overview

localFirstTools is a collection of **200+ self-contained HTML applications** following a "local-first" philosophy. Each HTML file is a complete application with inline CSS and JavaScript, requiring no build process or external dependencies.

### Key Features

- **Self-Contained**: Every app is a single HTML file
- **Works Offline**: No internet required after loading
- **Privacy-First**: All data stored locally in your browser
- **Data Portable**: JSON import/export in every app
- **Zero Dependencies**: No npm, no build tools, no CDNs

### Run Locally

```bash
git clone https://github.com/kody-w/localFirstTools.git
cd localFirstTools
python3 -m http.server 8000
# Open http://localhost:8000
```

### Application Categories

| Directory | Category | Description |
|-----------|----------|-------------|
| `apps/games/` | Games | 50+ browser games |
| `apps/productivity/` | Productivity | Task management, timers |
| `apps/business/` | Business | CRM, dashboards |
| `apps/development/` | Development | Developer tools |
| `apps/media/` | Media | Recording, music tools |
| `apps/education/` | Education | Learning tools |
| `apps/ai-tools/` | AI Tools | AI-powered apps |
| `apps/health/` | Health | Wellness tracking |
| `apps/utilities/` | Utilities | General tools |
| `apps/quantum-worlds/` | Quantum Worlds | P2P 3D universes |

### Contributing

1. Create your app in the appropriate `apps/[category]/` directory
2. Follow the self-contained HTML pattern (see `CLAUDE.md` for template)
3. Include JSON import/export functionality
4. Test locally and submit a PR

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines.

## License

MIT License - Use freely, keep it local-first!
