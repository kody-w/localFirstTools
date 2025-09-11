# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

localFirstTools is a collection of self-contained HTML applications that follow a "local-first" philosophy. Each HTML file is a complete application with inline CSS and JavaScript, requiring no build process or external dependencies.

## Key Architecture Principles

1. **Self-Contained HTML Files**: Every application is a single HTML file with all CSS and JavaScript inline. Never split these into separate files.
2. **No External Dependencies**: Applications must work offline. Do not add CDN links or npm packages.
3. **Gallery System**: The index.html serves as a launcher. New applications are automatically discovered by the Python updater scripts.
4. **JSON Configuration**: Applications are registered in `utility_apps_config.json` with metadata including title, category, description, and filename.

## Common Development Tasks

### Adding a New Application
1. Create a single HTML file with all code inline in the appropriate category directory:
   - `apps/games/` for games
   - `apps/productivity/` for productivity tools
   - `apps/business/` for business applications
   - etc.
2. The application will be available at its path when served via GitHub Pages or a local server

### Building the Xbox Extension
```bash
cd edgeAddons/xbox-mkb-extension
./create-xbox-mkb-extension.sh
```

## Application Categories

When creating new applications, use these existing categories:
- Games
- Productivity
- Media & Entertainment
- Business & Finance
- Development Tools
- Education & Reference
- AI Tools
- Utilities

## Development Guidelines

1. **HTML Structure**: Each application should be a complete, valid HTML document with proper DOCTYPE and meta tags
2. **Responsive Design**: Applications should work on desktop and mobile devices
3. **Local Storage**: Use browser localStorage for persistence, never external databases
4. **Error Handling**: Applications should gracefully handle offline scenarios and missing data
5. **Performance**: Keep file sizes reasonable since all code is inline

## Testing

Testing is done manually in the browser. There is no automated test framework. When modifying applications:
1. Test in multiple browsers (Chrome, Firefox, Edge)
2. Test offline functionality
3. Test on mobile devices
4. Verify local storage persistence

## File Naming Conventions

- Application files: descriptive-name.html (lowercase with hyphens)
- Game configuration: game-name-game.json
- Utility scripts: purpose-description.py

## File Organization

### Directory Structure
```
localFirstTools/
├── index.html          # Main gallery/launcher (DO NOT MOVE)
├── apps/              # All HTML applications organized by category
│   ├── games/         # Gaming applications
│   ├── productivity/  # Task management, organization tools
│   ├── business/      # CRM, dashboards, business tools
│   ├── development/   # Development and coding tools
│   ├── media/         # Screen recording, video tools
│   ├── education/     # Learning and teaching tools
│   ├── ai-tools/      # AI-powered applications
│   ├── health/        # Health and wellness apps
│   ├── utilities/     # General purpose tools
│   └── index-variants/# Alternative index page versions
├── data/              # Data files
│   ├── games/         # Game JSON configuration files
│   └── config/        # Application configuration
│       ├── utility_apps_config.json  # Auto-generated app registry
│       └── tasks.json               # Task tracking (gitignored)
├── archive/           # Archived/older versions
└── edgeAddons/        # Browser extensions
```

### Important Files
- **index.html**: Main gallery/launcher page (must remain in root)
- **data/config/utility_apps_config.json**: Application registry (if using dynamic gallery)