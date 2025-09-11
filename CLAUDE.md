# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

localFirstTools is a collection of self-contained HTML applications that follow a "local-first" philosophy. Each HTML file is a complete application with inline CSS and JavaScript, requiring no build process or external dependencies.

## Key Architecture Principles

1. **Self-Contained HTML Files**: Every application is a single HTML file with all CSS and JavaScript inline. Never split these into separate files.
2. **No External Dependencies**: Applications must work offline. Do not add CDN links or npm packages.
3. **Gallery System**: The index.html serves as a launcher. New applications are automatically discovered by the Python updater scripts.
4. **JSON Configuration**: Applications are registered in `data/config/utility_apps_config.json` with metadata including title, category, description, and filename.

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
├── index.html                       # Main gallery/launcher (DO NOT MOVE)
├── apps/                           # All HTML applications by category
│   ├── games/                      # Games and entertainment
│   ├── productivity/               # Productivity tools
│   ├── business/                   # Business applications
│   ├── development/                # Developer tools
│   ├── media/                      # Media and music tools
│   ├── education/                  # Educational tools
│   ├── ai-tools/                   # AI-powered tools
│   ├── health/                     # Health and wellness
│   ├── utilities/                  # General utilities
│   └── index-variants/             # Alternative index pages
├── data/                           
│   ├── config/
│   │   └── utility_apps_config.json  # Auto-generated app registry
│   └── games/                        # Game configuration files
├── scripts/                          # Utility shell scripts
├── archive/                          # Archived versions and updater script
└── edgeAddons/                       
    └── xbox-mkb-extension/           # Xbox controller support
```

### Important Files
- **index.html**: Main gallery launcher (must remain in root)
- **data/config/utility_apps_config.json**: Application registry used by gallery
- **archive/app-store-updater.py**: Python script for updating app configuration

## File Naming Conventions

- Application files: `descriptive-name.html` (lowercase with hyphens)
- Game configuration: `game-name-game.json`
- Shell scripts: `purpose-description.sh`
- Python scripts: `purpose_description.py`