# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

localFirstTools is a collection of **200+ self-contained HTML applications** that follow a "local-first" philosophy. Each HTML file is a complete application with inline CSS and JavaScript, requiring no build process or external dependencies. The project includes games, productivity tools, AI interfaces, educational apps, and experimental P2P multiplayer worlds.

**Live Site:** Hosted via GitHub Pages - applications are accessible directly in the browser.

## Key Architecture Principles

1. **Self-Contained HTML Files**: Every application is a single HTML file with all CSS and JavaScript inline. **Never split these into separate files.**
2. **No External Dependencies**: Applications must work offline. **Do not add CDN links or npm packages.**
3. **Gallery System**: The `index.html` serves as a launcher. New applications are automatically discovered by the Python updater scripts.
4. **JSON Configuration**: Applications are registered in `data/config/utility_apps_config.json` with metadata including title, category, description, and filename.
5. **Local Storage**: All data persistence uses browser localStorage. Never use external databases.
6. **Data Portability**: Every application should include JSON import/export functionality.

## Commands

### Update Gallery Configuration
```bash
python3 archive/app-store-updater.py
```
Updates the `data/config/utility_apps_config.json` file by scanning for HTML applications.

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

### Run Tests (Validation)
Tests are run via GitHub Actions scheduled builds:
- Config file validation (valid JSON)
- No duplicate app IDs
- Critical files exist
- Extension builds successfully

## Application Categories

When creating new applications, place them in the appropriate category directory:

| Directory | Category | Icon | Description |
|-----------|----------|------|-------------|
| `apps/games/` | Games | 🎮 | Gaming and entertainment |
| `apps/productivity/` | Productivity | 📋 | Task management, organization tools |
| `apps/business/` | Business | 💼 | CRM, dashboards, business tools |
| `apps/development/` | Development | 💻 | Development and coding tools |
| `apps/media/` | Media | 📹 | Media creation, recording, music tools |
| `apps/education/` | Education | 🎓 | Learning and teaching tools |
| `apps/ai-tools/` | AI Tools | 🤖 | AI-powered applications |
| `apps/health/` | Health | 💪 | Health and wellness tracking |
| `apps/utilities/` | Utilities | 🔧 | General purpose tools |
| `apps/quantum-worlds/` | Quantum Worlds | 🌌 | P2P multiplayer 3D universes |
| `apps/index-variants/` | Index Variants | 📄 | Alternative gallery layouts |

## Development Guidelines

### HTML Structure
Each application should be a complete, valid HTML document:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Descriptive App Name]</title>
    <style>
        /* ALL CSS inline here - include responsive design */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        /* Include styles for import/export buttons */
        .data-controls { position: fixed; top: 10px; right: 10px; z-index: 1000; }
        .data-controls button { margin-left: 10px; padding: 8px 16px; cursor: pointer; }
    </style>
</head>
<body>
    <!-- HTML content including import/export UI -->
    <div class="data-controls">
        <button onclick="exportData()">Export Data</button>
        <button onclick="document.getElementById('importFile').click()">Import Data</button>
        <input type="file" id="importFile" accept=".json" style="display: none;" onchange="importData(event)">
    </div>

    <script>
        // ALL JavaScript inline here
        const APP_NAME = '[app-name-key]';

        // Data management
        let appData = JSON.parse(localStorage.getItem(APP_NAME) || '{}');

        function saveData() {
            localStorage.setItem(APP_NAME, JSON.stringify(appData));
        }

        function exportData() {
            const dataStr = JSON.stringify(appData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `${APP_NAME}-data-${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            URL.revokeObjectURL(url);
        }

        function importData(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    appData = JSON.parse(e.target.result);
                    saveData();
                    location.reload();
                } catch (error) {
                    alert('Invalid JSON file');
                }
            };
            reader.readAsText(file);
        }

        // Application logic here
    </script>
</body>
</html>
```

### Core Requirements

1. **Responsive Design**: Applications should work on desktop (1920px+), tablet (768px-1024px), and mobile (320px-767px)
2. **Local Storage**: Use browser localStorage for persistence, never external databases
3. **Data Import/Export**: Every application should include JSON import/export functionality for data portability
4. **Error Handling**: Applications should gracefully handle offline scenarios and missing data
5. **Performance**: Keep file sizes reasonable since all code is inline
6. **Accessibility**: Include proper ARIA labels and keyboard navigation
7. **No External Assets**: All assets must be inline (use base64 for images if absolutely necessary)

## Testing

Testing is done manually in the browser. When modifying applications:

1. Test in multiple browsers (Chrome, Firefox, Edge)
2. Test offline functionality
3. Test on mobile devices
4. Verify local storage persistence
5. Test JSON import/export functionality
6. Check responsive design at different breakpoints
7. Verify keyboard navigation and accessibility

## File Organization

### Core Structure
```
localFirstTools/
├── index.html                       # Main gallery/launcher (DO NOT MOVE)
├── CLAUDE.md                        # This file - project guidelines
├── README.md                        # Public readme
│
├── apps/                           # All HTML applications by category
│   ├── games/                      # Games and entertainment (50+ apps)
│   ├── productivity/               # Productivity tools
│   ├── business/                   # Business applications
│   ├── development/                # Developer tools
│   ├── media/                      # Media and music tools
│   ├── education/                  # Educational tools
│   ├── ai-tools/                   # AI-powered tools
│   ├── health/                     # Health and wellness
│   ├── utilities/                  # General utilities
│   ├── quantum-worlds/             # P2P multiplayer universes (10 worlds)
│   └── index-variants/             # Alternative index pages
│
├── data/
│   ├── config/
│   │   └── utility_apps_config.json  # Auto-generated app registry (200+ apps)
│   └── games/                        # Game configuration files
│
├── .claude/
│   └── agents/                       # Custom Claude Code subagent definitions
│       ├── local-first-app-builder.md
│       ├── quantum-world-generator.md
│       ├── local-first-steward.md
│       ├── app-buzzsaw-enhancer.md
│       ├── strategy-analyzer.md
│       └── ... (12 agents total)
│
├── .github/
│   └── workflows/                    # GitHub Actions automation
│       ├── build-extension.yml       # Automatic extension builds
│       ├── release-extension.yml     # Version releases
│       └── scheduled-build.yml       # Weekly health checks
│
├── scripts/                          # Utility shell scripts
├── archive/                          # Archived versions and updater script
│   └── app-store-updater.py          # Python script for updating config
│
├── vibe_templates/                   # Project templates for bootstrapping
│
└── edgeAddons/
    └── xbox-mkb-extension/           # Xbox controller support extension
```

### Important Files
- **index.html**: Main gallery launcher (must remain in root)
- **data/config/utility_apps_config.json**: Application registry used by gallery
- **archive/app-store-updater.py**: Python script for updating app configuration
- **CLAUDE.md**: This file - project guidelines and AI assistant instructions

## Claude Code Custom Agents

The project includes 12 custom Claude Code subagents in `.claude/agents/`:

| Agent | Purpose |
|-------|---------|
| `local-first-app-builder` | Creates new self-contained HTML applications with import/export |
| `quantum-world-generator` | Creates P2P networked 3D universe applications |
| `local-first-steward` | Maintains and validates the localFirstTools directory |
| `app-buzzsaw-enhancer` | Analyzes and enhances apps using 8 strategy analyzers |
| `strategy-analyzer` | Analyzes solutions without making code changes |
| `file-reorganizer-indexer` | Reorganizes files and updates index.html |
| `app-organizer-dynamic` | Dynamically categorizes and sorts applications |
| `pii-scrubber` | Scans and removes PII from codebase files |
| `meta-agent` | Generates new Claude Code subagent configurations |
| `agent-orchestrator` | Coordinates multiple specialized agents |
| `scenario-brainstorm-generator` | Generates creative AI application ideas |
| `git-history-cleaner` | Cleans git history |

### Using Custom Agents

When creating new applications, use the `local-first-app-builder` agent:
```
Create a new [category] app that [description]
```

For Quantum Worlds, use the `quantum-world-generator` agent:
```
Create a new Quantum World about [concept]
```

## GitHub Actions Workflows

### 1. Build Extension (`build-extension.yml`)
- **Triggers**: Push to main (when apps/data/extension files change), manual dispatch
- **Actions**: Runs meta-analysis, builds Chrome extension, creates ZIP, commits built files

### 2. Release Extension (`release-extension.yml`)
- **Triggers**: Push tag `v*.*.*`, manual dispatch with version input
- **Actions**: Updates manifest version, builds extension, creates GitHub Release

### 3. Scheduled Build (`scheduled-build.yml`)
- **Triggers**: Every Monday at 9 AM UTC, manual dispatch
- **Actions**: Weekly meta-analysis, validation tests, health report generation

### Creating a Release
```bash
# Using git tags (recommended)
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# Manual workflow
gh workflow run release-extension.yml -f version=1.2.0
```

## Quantum Worlds System

The project includes a unique P2P multiplayer 3D universe system with 10 experimental worlds in `apps/quantum-worlds/`:

| World | Theme | Description |
|-------|-------|-------------|
| Quantum Garden | Fantastical | Floating islands with bioluminescent plants |
| Neon Synthwave City | Artistic | Cyberpunk metropolis in eternal sunset |
| Collaborative Music Garden | Artistic | Objects generate tones and melodies |
| Impossible Architecture | Scientific | M.C. Escher-inspired geometry |
| Bioluminescent Ocean | Scientific | Underwater abyss with zero-gravity |
| Particle Physics | Educational | Players ARE subatomic particles |
| Zero-G Space Station | Social | Modular space station building |
| Fractal Forest | Scientific | Infinite recursion at every scale |
| Living Paint Dimension | Artistic | Movements create living paint |
| Ancient Ruins | Action | Temples on a dying star |

### Quantum Worlds Technical Stack
- **3D Rendering**: Three.js (inline)
- **Networking**: WebRTC P2P
- **Storage**: localStorage/IndexedDB
- **Architecture**: Config-driven modular monolith

## Featured Applications

Applications with the `featured` tag are highlighted in the gallery:

- **FocusFlow Timer** - Productivity timer with circular visualization
- **SecureVault** - Privacy-first password manager
- **JARVIS Protocol** - Complete AI assistant OS
- **NeRF Studio** - Neural 3D scene capture
- **Quantum Particle Lab** - Interactive physics playground
- **Holographic Display Creator** - Real 3D holograms with Pepper's Ghost
- **Quantum Worlds Social VR** - P2P multiverse explorer

## File Naming Conventions

- Application files: `descriptive-name.html` (lowercase with hyphens)
- Game configuration: `game-name-game.json`
- Shell scripts: `purpose-description.sh`
- Python scripts: `purpose_description.py`
- Agent definitions: `agent-name.md`

## Best Practices

### DO
- Keep all code in a single HTML file
- Use localStorage for all data persistence
- Include import/export JSON functionality
- Make apps work offline
- Use semantic HTML and ARIA labels
- Test on mobile devices
- Follow the established HTML template structure

### DON'T
- Split code into separate CSS/JS files
- Add CDN links or external dependencies
- Use external APIs that require internet
- Create files without proper categorization
- Skip the import/export functionality
- Ignore responsive design
- Use generic or unclear app names

## Adding a New Application

1. **Create the file** in the appropriate `apps/[category]/` directory
2. **Follow the HTML template** with inline CSS/JS and import/export
3. **Test locally** with `python3 -m http.server 8000`
4. **Update the config** by running `python3 archive/app-store-updater.py`
5. **Commit and push** - GitHub Actions will handle the rest

## Troubleshooting

### Application not appearing in gallery
- Run `python3 archive/app-store-updater.py` to update config
- Check that the file is in the correct `apps/` subdirectory
- Verify the HTML has a proper `<title>` tag

### GitHub Actions failing
- Check workflow permissions in Repository Settings
- Ensure trigger paths match file locations
- Review the Actions tab for specific error messages

### Extension not building
- Verify all required files exist
- Check that `utility_apps_config.json` is valid JSON
- Review build logs in GitHub Actions
