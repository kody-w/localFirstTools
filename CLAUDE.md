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

# Watch mode - automatically updates when HTML files change
python3 vibe_gallery_watcher.py

# Run watcher once and exit (quick update)
python3 vibe_gallery_watcher.py --once

# Quick shell wrapper (runs updater)
./update-gallery.sh

# Legacy updater (still works with data/config/utility_apps_config.json)
python3 archive/app-store-updater.py
```

### Organize Files into Category Folders
```bash
# Move HTML files from root to category folders
python3 vibe_gallery_organizer.py

# Preview what would be moved (dry run)
python3 vibe_gallery_organizer.py --dry-run
```

### Update Tools Manifest
```bash
python3 update-tools-manifest.py
```

### Accessibility Tools
```bash
# Check color contrast in HTML files
python3 color_contrast_check.py

# Apply accessibility patches to HTML files
python3 accessibility_patch.py
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

## Development Workflow

### Adding a New Application
1. Create self-contained HTML file in root directory
2. Include proper `<title>` and `<meta name="description">` tags
3. Test the application in multiple browsers
4. Run `python3 vibe_gallery_updater.py` to regenerate configs
5. Verify the app appears correctly in index.html gallery

### Development Mode
For active development, use the watcher to automatically update configs:
```bash
python3 vibe_gallery_watcher.py
```
This watches for file changes and automatically regenerates the gallery config.

### Modifying Existing Applications
1. Edit the HTML file directly
2. Test changes in browser
3. Run updater or watcher to update gallery configs
4. Commit changes to git

## Development Guidelines

1. **HTML Structure**: Each application should be a complete, valid HTML document with proper DOCTYPE and meta tags
2. **Responsive Design**: Applications should work on desktop and mobile devices
3. **Local Storage**: Use browser localStorage for persistence, never external databases
4. **Data Import/Export**: Every application should include JSON import/export functionality for data portability
5. **Error Handling**: Applications should gracefully handle offline scenarios and missing data
6. **Performance**: Keep file sizes reasonable since all code is inline
7. **Metadata Tags**: Include descriptive comments in HTML for auto-categorization (e.g., <!-- 3d, canvas, animation -->)
8. **Accessibility**: Ensure proper ARIA labels, keyboard navigation, and color contrast ratios (use accessibility_patch.py)

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
- **index.html**: Main gallery launcher with 3D gallery mode and Xbox controller support (must remain in root)
- **vibe_gallery_config.json**: Primary application registry with metadata (auto-generated)
- **vibe_gallery_updater.py**: Main script for updating gallery configuration
- **vibe_gallery_watcher.py**: Auto-updates config when HTML files change
- **vibe_gallery_organizer.py**: Moves HTML files into category folders
- **tools-manifest.json**: Simple manifest of all HTML tools
- **data/config/utility_apps_config.json**: Legacy registry (still functional)

## File Naming Conventions

- Application files: `descriptive-name.html` (lowercase with hyphens)
- Configuration files: `*_config.json`
- Shell scripts: `purpose-description.sh`
- Python scripts: `purpose_description.py`

## Metadata Extraction System

The vibe_gallery_updater.py script automatically extracts metadata from HTML files:

### Extracted Metadata
- **Title**: From `<title>` tags or filename
- **Description**: From meta description tag or auto-generated
- **Tags**: Technical features detected (3D, canvas, SVG, animation, etc.)
- **Complexity**: simple/intermediate/advanced (based on file size and features)
- **Interaction Type**: game/drawing/visual/interactive/audio/interface
- **Category**: Auto-assigned based on content analysis

### Auto-Categorization Logic
Applications are automatically categorized into one of 9 categories based on:
1. **Keywords in file path** (e.g., "games", "ai", "media")
2. **Technical features detected** (e.g., WebGL → 3d_immersive)
3. **Content analysis** (e.g., "particle" keyword → particle_physics)
4. **Interaction patterns** (e.g., click/drag/touch → interactive)

### Configuration Files
- **vibe_gallery_config.json** (root): Primary config with full metadata and categorization
- **tools-manifest.json** (root): Simple listing of all HTML files with basic metadata
- **data/config/utility_apps_config.json**: Legacy config (still functional)

When you modify HTML files, run the updater to regenerate these configs automatically.

## Gallery Features

### 3D Gallery Mode
The index.html includes an immersive 3D gallery experience powered by Three.js:
- **Keyboard Controls**: WASD for movement, mouse for looking around
- **Xbox Controller Support**: Left stick for movement, right stick for camera, A button to open tools
- **Mobile Support**: Touch gestures and virtual joystick for movement
- **Interactive Artwork Display**: Tools displayed as 3D "paintings" in a virtual gallery

### Gallery Modes
- **Main Gallery**: Default view showing all active applications
- **Archive**: View for older/deprecated applications
- **3D Experience**: Immersive walkthrough gallery with controller support

### User Features
- **Search**: Filter tools by title, description, or filename
- **Pin Tools**: Pin favorite tools to the top of the gallery
- **Vote System**: Users can vote for feature requests (stored in localStorage)
- **Download**: Save individual HTML files locally