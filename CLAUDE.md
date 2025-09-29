# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

localFirstTools is a collection of self-contained HTML applications following a "local-first" philosophy. Each HTML file is a complete application with inline CSS and JavaScript, requiring no build process or external dependencies. The project includes 100+ interactive tools, games, and creative applications accessible through a gallery launcher.

## Key Architecture Principles

1. **Self-Contained HTML Files**: Every application is a single HTML file with all CSS and JavaScript inline. Never split these into separate files.
2. **No External Dependencies**: Applications must work offline. Do not add CDN links or npm packages.
3. **Gallery System**: The index.html serves as a launcher that reads from vibe_gallery_config.json for application discovery.
4. **Auto-Discovery**: Python scripts automatically scan HTML files and extract metadata for categorization.
5. **Flat File Structure**: Currently, all HTML applications reside in the root directory (not in subdirectories).

## Commands

### Update Gallery Configuration
```bash
# Primary method - extracts metadata and regenerates config
python3 vibe_gallery_updater.py

# Quick shell wrapper
./update-gallery.sh

# Legacy updater (still works with data/config/utility_apps_config.json)
python3 archive/app-store-updater.py
```

### Update Tools Manifest
```bash
python3 update-tools-manifest.py
```

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

The gallery organizes applications into thematic categories:
- **visual_art** - Interactive visual experiences and design tools
- **3d_immersive** - Three-dimensional and WebGL experiences
- **audio_music** - Sound synthesis and music creation tools
- **games_puzzles** - Interactive games and playful experiences
- **experimental_ai** - AI-powered interfaces and cutting-edge demos
- **creative_tools** - Productivity and creative utilities
- **generative_art** - Algorithmic art generation systems
- **particle_physics** - Physics simulations and particle systems
- **educational_tools** - Learning resources and tutorials

## Development Guidelines

1. **HTML Structure**: Each application should be a complete, valid HTML document with proper DOCTYPE and meta tags
2. **Responsive Design**: Applications should work on desktop and mobile devices
3. **Local Storage**: Use browser localStorage for persistence, never external databases
4. **Data Import/Export**: Every application should include JSON import/export functionality for data portability
5. **Error Handling**: Applications should gracefully handle offline scenarios and missing data
6. **Performance**: Keep file sizes reasonable since all code is inline
7. **Metadata Tags**: Include descriptive comments in HTML for auto-categorization (e.g., <!-- 3d, canvas, animation -->)

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
├── index.html                       # Main gallery launcher (DO NOT MODIFY LOCATION)
├── vibe_gallery_config.json        # Primary auto-generated app registry
├── tools-manifest.json             # Simple tool listing with metadata
├── [100+ HTML applications]        # Self-contained apps in root directory
├── archive/                        # Legacy scripts and archived versions
├── scripts/                        # Utility shell scripts
├── edgeAddons/
│   └── xbox-mkb-extension/         # Xbox controller browser support
├── data/
│   ├── config/
│   │   └── utility_apps_config.json  # Legacy app registry
│   └── games/                        # Game-specific data files
└── notes/                            # Development notes and experiments
```

### Important Files
- **index.html**: Main gallery launcher (must remain in root)
- **vibe_gallery_config.json**: Primary application registry with metadata (auto-generated)
- **vibe_gallery_updater.py**: Main script for updating gallery configuration
- **tools-manifest.json**: Simple manifest of all HTML tools
- **data/config/utility_apps_config.json**: Legacy registry (still functional)

## File Naming Conventions

- Application files: `descriptive-name.html` (lowercase with hyphens)
- Configuration files: `*_config.json`
- Shell scripts: `purpose-description.sh`
- Python scripts: `purpose_description.py`

## Metadata Extraction

The vibe_gallery_updater.py script automatically extracts:
- Title from `<title>` tags
- Description from meta description or auto-generated from content
- Technical features (3D, canvas, SVG, animation, etc.) from code analysis
- Complexity level based on code patterns
- Interaction type (game, drawing, visual, interactive)

Applications are automatically categorized based on keywords and technical features detected in the code.