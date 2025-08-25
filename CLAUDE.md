# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

localFirstTools is a collection of 70+ self-contained HTML applications that follow a "local-first" philosophy. Each HTML file is a complete application with inline CSS and JavaScript, requiring no build process, npm packages, or external dependencies. Applications work completely offline and store data locally in the browser.

## Critical Architecture Rules

1. **NEVER Split Files**: Every application MUST be a single HTML file with ALL code inline. Never create separate CSS, JS, or asset files.
2. **Zero External Dependencies**: No CDN links, npm packages, or external resources. Applications must work 100% offline.
3. **localStorage Only**: Use browser localStorage for persistence. Never use external databases or APIs.
4. **Gallery Auto-Discovery**: New apps are automatically indexed when placed in the correct directory structure.

## Directory Structure

```
localFirstTools/
├── index.html          # Main gallery launcher (DO NOT MOVE - must stay in root)
├── apps/              # All applications by category
│   ├── games/         # Gaming applications  
│   ├── productivity/  # Task management, writing tools
│   ├── business/      # CRM, presentations, sales tools
│   ├── ai-tools/      # AI agents and interfaces
│   ├── development/   # Developer utilities
│   ├── media/         # Recording, audio/video tools
│   ├── education/     # Learning and training apps
│   ├── health/        # Wellness applications
│   ├── utilities/     # General purpose tools
│   └── index-variants/# Alternative gallery versions
├── data/              
│   ├── games/         # Game configuration JSONs (optional)
│   └── config/        
│       └── utility_apps_config.json  # Auto-generated app registry
├── scripts/           # Utility scripts
└── edgeAddons/        # Browser extensions
```

## Common Commands

### Organize Files Into Categories
```bash
python scripts/organize_files.py --execute
```
This automatically categorizes HTML files based on filename patterns and moves them to appropriate directories.

### Local Development Server (Optional)
```bash
# Python
python -m http.server 8000

# Flask-based (if needed)
cd scripts && ./setup-flask-app.sh
```

### Build Xbox Controller Extension
```bash
cd edgeAddons && ./create-xbox-mkb-extension.sh
```

## Application Template

Every HTML application MUST follow this exact structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Name</title>
    <style>
        /* ALL CSS must be inline here */
    </style>
</head>
<body>
    <!-- HTML content -->
    <script>
        // ALL JavaScript must be inline here
        // Use localStorage for data persistence
        // Handle offline scenarios gracefully
    </script>
</body>
</html>
```

## Adding New Applications

1. Create a single HTML file in the appropriate `apps/` subdirectory
2. Include ALL code inline (HTML, CSS, JavaScript)
3. Test offline functionality thoroughly
4. Ensure mobile responsiveness
5. Use localStorage for any data persistence needs

## Important Implementation Notes

- **index.html Location**: The main gallery index.html MUST remain in the root directory for GitHub Pages compatibility
- **App Registry**: `data/config/utility_apps_config.json` is auto-generated and contains app metadata (id, title, description, tags, path, icon)
- **Game Data**: Games can optionally load JSON configs from `data/games/` following the pattern `game-name-game.json`
- **File Naming**: Use lowercase with hyphens (e.g., `my-app-name.html`)
- **Responsive Design**: All apps must work on desktop, tablet, and mobile devices
- **Error Handling**: Apps must gracefully handle offline scenarios and missing data files

## Development Philosophy

This project adheres to local-first principles:
- User data never leaves the device
- No tracking, analytics, or telemetry
- No build process or compilation required
- Standard HTML/CSS/JS ensures decades of compatibility
- Copy files anywhere and they continue to work