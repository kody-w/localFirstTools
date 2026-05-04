# localFirstTools Quick Reference

## Repository Structure (Reorganized 2025-10-13)

### Root Directory
- **152 HTML applications** - All self-contained apps remain in root for gallery compatibility
- **index.html** - Main gallery launcher with 3D mode and Xbox controller support
- **README.md** - Project documentation
- **CLAUDE.md** - AI assistant instructions with full repo details
- **ORGANIZATION_REPORT.md** - Details of recent repository reorganization

### Documentation (`docs/`)
All documentation now organized by category:

```
docs/
├── wowmon/          60 files - WowMon game design (endgame, narrative, casual, etc.)
├── agent/           12 files - Agent strategies and design reports
├── accessibility/    6 files - A11y guides, reports, and code examples
├── tutorials/        8 files - Quick refs, cheatsheets, guides
├── game-design/      7 files - Game redesigns (roguelike, metroidvania, etc.)
├── implementation/   5 files - Implementation and integration guides
├── misc/             5 files - UIRenderer docs, build ideas, misc READMEs
├── reports/          3 files - Performance reports and analysis
└── architecture/     2 files - System architecture documentation
```

### Scripts (`scripts/`)
All automation scripts organized by purpose:

```
scripts/
├── gallery/         5 scripts - Gallery config updater, watcher, organizer
├── maintenance/     4 scripts - Accessibility, contrast checks, compression
└── shell/           2 scripts - Shell wrappers for common tasks
```

## Quick Commands

### Update Gallery
```bash
# These work from root via symlinks:
python3 vibe_gallery_updater.py
./update-gallery.sh

# Or use direct paths:
python3 scripts/gallery/vibe_gallery_updater.py
```

### Watch for Changes
```bash
python3 scripts/gallery/vibe_gallery_watcher.py
```

### Check Accessibility
```bash
python3 scripts/maintenance/color_contrast_check.py
python3 scripts/maintenance/accessibility_patch.py
```

### Update Tools Manifest
```bash
python3 update-tools-manifest.py  # symlinked
```

## Finding Documentation

### WowMon Game Design
```bash
ls docs/wowmon/
# 60+ files covering all aspects of WowMon game
```

### Agent Strategies
```bash
ls docs/agent/
# 12 files with agent design reports and implementations
```

### Accessibility
```bash
ls docs/accessibility/
# Guides, reports, and code examples for a11y
```

### Quick References
```bash
ls docs/tutorials/
# Quickstart guides, cheatsheets, and references
```

## Key Features

### Backward Compatibility
All existing commands work via symlinks:
- `vibe_gallery_updater.py` → `scripts/gallery/vibe_gallery_updater.py`
- `update-tools-manifest.py` → `scripts/gallery/update-tools-manifest.py`
- `update-gallery.sh` → `scripts/shell/update-gallery.sh`

### Gallery System
- **Main Gallery**: Default view with all apps
- **3D Experience**: Immersive walkthrough (WASD + mouse, Xbox controller supported)
- **Search**: Filter by title, description, filename
- **Pin Tools**: Favorite tools stay at top
- **Categories**: 9 auto-categorized app types

### Development Workflow
1. Create/edit HTML in root directory
2. Run `python3 vibe_gallery_updater.py`
3. Test in browser
4. Commit changes

## Quick Stats

- **152 HTML applications** in root
- **112 documentation files** organized in docs/
- **13 scripts** organized in scripts/
- **3 symlinks** for backward compatibility
- **9 documentation categories**
- **3 script categories**

## Need More Info?

- **Full details**: See [CLAUDE.md](/Users/kodyw/Documents/GitHub/localFirstTools3/CLAUDE.md)
- **Organization report**: See [ORGANIZATION_REPORT.md](/Users/kodyw/Documents/GitHub/localFirstTools3/ORGANIZATION_REPORT.md)
- **Project info**: See [README.md](/Users/kodyw/Documents/GitHub/localFirstTools3/README.md)
