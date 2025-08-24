# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

localFirstTools is a collection of self-contained HTML applications that follow a "local-first" philosophy. Each HTML file is a complete application with inline CSS and JavaScript, requiring no build process or external dependencies.

## Key Architecture Principles

1. **Self-Contained HTML Files**: Every application is a single HTML file with all CSS and JavaScript inline. Never split these into separate files.
2. **No External Dependencies**: Applications must work offline. Do not add CDN links or npm packages.
3. **Gallery System**: The index.html serves as a launcher. New applications are automatically discovered by the Python updater scripts.
4. **JSON Configuration**: Applications are registered in `data/config/utility_apps_config.json` with metadata including id, title, description, tags, path, and icon.

## Common Development Tasks

### Adding a New Application
1. Create a single HTML file with all code inline in the appropriate category directory:
   - `apps/games/` for games
   - `apps/productivity/` for productivity tools
   - `apps/business/` for business applications
   - `apps/ai-tools/` for AI-powered tools
   - `apps/development/` for development tools
   - `apps/media/` for media/recording apps
   - `apps/education/` for learning tools
   - `apps/health/` for health apps
   - `apps/utilities/` for general utilities
2. The application will be available at its path when served via GitHub Pages or a local server

### Organizing Files
```bash
python scripts/organize_files.py --execute
```
This script automatically categorizes and moves HTML files to appropriate directories based on filename patterns.

### Local Development Server
For Flask-based development (if needed):
```bash
cd scripts
./setup-flask-app.sh
```

### Building the Xbox Extension
```bash
cd edgeAddons
./create-xbox-mkb-extension.sh
```

## Application Pattern

Each HTML application follows this structure:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Name</title>
    <style>
        /* All CSS inline - no external stylesheets */
    </style>
</head>
<body>
    <!-- HTML content -->
    <script>
        // All JavaScript inline - no external scripts
        // Use localStorage for persistence
    </script>
</body>
</html>
```

## Development Guidelines

1. **HTML Structure**: Each application should be a complete, valid HTML document with proper DOCTYPE and meta tags
2. **Responsive Design**: Applications should work on desktop and mobile devices
3. **Local Storage**: Use browser localStorage for persistence, never external databases
4. **Error Handling**: Applications should gracefully handle offline scenarios and missing data
5. **Performance**: Keep file sizes reasonable since all code is inline

## Game Data Files

Games can load configuration from JSON files in `data/games/`:
- Game configuration files follow the pattern: `game-name-game.json`
- These contain game levels, sprites, rules, etc.
- Games should gracefully handle missing JSON files

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
- **index.html**: Main gallery/launcher page (must remain in root) - Features animated "Vibe Coding" gallery interface
- **data/config/utility_apps_config.json**: Auto-generated application registry with metadata
- **data/config/tasks.json**: Task tracking data (gitignored)
- **scripts/organize_files.py**: Utility to auto-categorize and organize HTML files into proper directories