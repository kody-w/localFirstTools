# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

localFirstTools is a collection of self-contained HTML applications that follow a "local-first" philosophy. Each HTML file is a complete application with inline CSS and JavaScript, requiring no build process or external dependencies.

## Key Architecture Principles

1. **Self-Contained HTML Files**: Every application is a single HTML file with all CSS and JavaScript inline. Never split these into separate files.
2. **No External Dependencies for new apps**: New productivity/utility/business apps must work fully offline (no CDN links, no npm packages). A small set of legacy 3D/P2P apps and three showcase apps (`apps/ai-tools/local-llm.html`, `apps/productivity/mesh-board.html`, `apps/development/sql-time-capsule.html`) load Three.js / PeerJS / WebLLM / Yjs / sql.js from CDN — leave those alone, but don't introduce CDNs in new apps.
3. **Gallery System**: Root `index.html` IS the gallery launcher. (Earlier in this repo's history root `index.html` was a P2P world; that has been moved to `apps/p2p-world/networked-world.html` with a `?room=…` redirect shim at root for backwards compatibility.)
4. **JSON Configuration**: Applications are registered in `data/config/utility_apps_config.json` with `{id, title, description, tags, path, icon, category, aliases}`. IDs are path-based (`category__filename-stem`) to guarantee uniqueness.

## Commands

### Update Gallery Configuration
```bash
python3 scripts/regenerate_registry.py
# Optional flags:
python3 scripts/regenerate_registry.py --dry-run   # preview, no write
python3 scripts/regenerate_registry.py --check     # exit 1 on duplicate IDs
```
Regenerates `data/config/utility_apps_config.json` by walking `apps/**/*.html`. Read-only — never moves files. Extracts `<title>`, `<meta name="description">`, `<meta name="keywords">`, `<meta name="icon">` from each HTML; falls back to first `<h1>`/`<p>` then a category-based default.

The two older organizers (`intelligent_organizer.py`, `organize_files.py`) are now in `archive/*.deprecated` — do not run them. Their `--execute` mode reshuffles files based on filename heuristics regardless of current placement.

### Build Xbox Extension
```bash
cd edgeAddons/xbox-mkb-extension
./create-xbox-mkb-extension.sh
```

### Run Local Server
```bash
python3 -m http.server 8000
# Access at http://localhost:8000
```

## Application Categories

When creating new applications, place them in the appropriate category directory:
- `apps/games/` - Gaming and entertainment
- `apps/productivity/` - Task management, organization tools
- `apps/business/` - CRM, dashboards, business tools
- `apps/development/` - Development and coding tools
- `apps/media/` - Media creation, recording, music tools
- `apps/education/` - Learning and teaching tools
- `apps/ai-tools/` - AI-powered applications
- `apps/health/` - Health and wellness tracking
- `apps/utilities/` - General purpose tools

## Development Guidelines

1. **HTML Structure**: Each application should be a complete, valid HTML document with proper DOCTYPE and meta tags
2. **Responsive Design**: Applications should work on desktop and mobile devices
3. **Local Storage**: Use browser localStorage for persistence, never external databases
4. **Data Import/Export**: Every application should include JSON import/export functionality for data portability
5. **Error Handling**: Applications should gracefully handle offline scenarios and missing data
6. **Performance**: Keep file sizes reasonable since all code is inline

## Testing

Testing is done manually in the browser. When modifying applications:
1. Test in multiple browsers (Chrome, Firefox, Edge)
2. Test offline functionality
3. Test on mobile devices
4. Verify local storage persistence
5. Test JSON import/export functionality

## File Organization

### Core Structure
```
localFirstTools/
├── index.html                       # The gallery launcher (DO NOT MOVE)
├── apps/                            # All HTML applications by category
│   ├── games/                       # Games and entertainment
│   ├── productivity/                # Productivity tools
│   ├── business/                    # Business applications
│   ├── development/                 # Developer tools
│   ├── media/                       # Media and music tools
│   ├── education/                   # Educational tools
│   ├── ai-tools/                    # AI-powered tools
│   ├── health/                     # Health and wellness
│   ├── utilities/                   # General utilities (incl. recommender, telepathy bus, NL patcher)
│   ├── p2p-world/                   # Three.js + PeerJS networked worlds (incl. networked-world.html)
│   ├── quantum-worlds/              # 3D collaborative experiences (incl. portal-hub.html)
│   └── index-variants/              # Alternative gallery snapshots
├── data/
│   ├── config/
│   │   └── utility_apps_config.json  # Auto-generated app registry
│   └── games/                        # Game configuration files
├── scripts/
│   ├── regenerate_registry.py        # The ONE registry generator (read-only)
│   ├── forge-bridge.py               # Local NL→app forge HTTP server (port 7711)
│   └── *.sh                          # Various one-off setup scripts
├── archive/                          # Deprecated experiments + provenance
└── edgeAddons/
    └── xbox-mkb-extension/           # Xbox controller support
```

### Important Files
- **index.html**: The gallery launcher (root). Old `apps/utilities/index_sorting.html` is now a redirect stub that forwards to root.
- **data/config/utility_apps_config.json**: Application registry consumed by the gallery
- **scripts/regenerate_registry.py**: The canonical registry generator (replaces the deprecated `intelligent_organizer.py` and `organize_files.py`)

## File Naming Conventions

- Application files: `descriptive-name.html` (lowercase with hyphens)
- Game configuration: `game-name-game.json`
- Shell scripts: `purpose-description.sh`
- Python scripts: `purpose_description.py`