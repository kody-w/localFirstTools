# localFirstTools - GitHub Copilot Coding Instructions

**ALWAYS follow these instructions first.** Only search for additional context or run bash commands if the information here is incomplete or found to be incorrect.

## Project Overview

localFirstTools is a collection of 96 self-contained HTML applications following a "local-first" philosophy. Each HTML file is a complete application with inline CSS and JavaScript, requiring no build process or external dependencies.

## Working Effectively

### Start Development Server
Start the local development server to test applications:
```bash
cd /home/runner/work/localFirstTools/localFirstTools
python3 -m http.server 8080
```
- **Expected time**: Instant (<1 second)
- **Access**: http://localhost:8080
- **Note**: No build process needed - serves static HTML files directly

### Build Xbox Extension (if needed)
Build the Xbox Mouse & Keyboard browser extension:
```bash
cd edgeAddons
./create-xbox-mkb-extension.sh
```
- **Expected time**: Instant (~0.01 seconds)
- **Output**: Creates complete extension in `xbox-mkb-extension/` directory
- **Installation**: Load unpacked extension in Edge at `edge://extensions/`

### Organize Files (if needed)
Run the file organization utility:
```bash
python3 scripts/organize_files.py --help    # See options
python3 scripts/organize_files.py           # Dry run mode
python3 scripts/organize_files.py --execute # Execute changes
```
- **Expected time**: Instant (~0.03 seconds)
- **Note**: Always run dry-run first to preview changes

## Application Development

### Adding New Applications
1. **Create self-contained HTML file** in appropriate category directory:
   - `apps/games/` - Gaming applications
   - `apps/productivity/` - Task management, organization tools
   - `apps/business/` - CRM, dashboards, business tools
   - `apps/development/` - Development and coding tools
   - `apps/media/` - Screen recording, video tools
   - `apps/education/` - Learning and teaching tools
   - `apps/ai-tools/` - AI-powered applications
   - `apps/health/` - Health and wellness apps
   - `apps/utilities/` - General purpose tools

2. **File naming**: Use `descriptive-name.html` (lowercase with hyphens)

3. **HTML Structure**: Each application must be a complete, valid HTML document:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>App Name</title>
       <style>
           /* All CSS inline here */
       </style>
   </head>
   <body>
       <!-- Application HTML -->
       <script>
           // All JavaScript inline here
       </script>
   </body>
   </html>
   ```

### Development Rules
- **NEVER split files**: All CSS and JavaScript must be inline
- **NO external dependencies**: No CDN links, no npm packages
- **Offline first**: Applications must work without internet
- **Local storage only**: Use `localStorage` for persistence, never external databases
- **Mobile responsive**: Test on desktop and mobile devices

## Validation and Testing

### Manual Browser Testing Requirements
After making any changes to HTML applications, ALWAYS test:

1. **Load application via HTTP server**:
   ```bash
   # Start server
   python3 -m http.server 8080
   # Test: http://localhost:8080/apps/[category]/[app-name].html
   ```

2. **Test core functionality**:
   - Application loads without errors
   - All interactive elements work
   - Data persists using localStorage
   - Responsive design on different screen sizes

3. **Test offline capability**:
   - Disconnect from internet
   - Refresh page - should still work
   - All features should remain functional

4. **Test in main gallery**:
   - Load http://localhost:8080 (main index.html)
   - Verify application appears in gallery
   - Test launching from gallery interface

### Browser Testing Checklist
- [ ] Chrome/Chromium
- [ ] Firefox  
- [ ] Edge (if extension-related)
- [ ] Mobile browsers (Safari iOS, Chrome Android)
- [ ] Offline functionality
- [ ] localStorage persistence

## Key Repository Structure

```
localFirstTools/
├── index.html                    # Main gallery/launcher (DO NOT MOVE)
├── apps/                        # All HTML applications by category
│   ├── games/                   # 96 total applications across
│   ├── productivity/            # 10+ categories
│   ├── business/
│   ├── development/
│   ├── media/
│   ├── education/
│   ├── ai-tools/
│   ├── health/
│   ├── utilities/
│   └── index-variants/
├── data/                        # Data and configuration files
│   ├── config/
│   │   └── utility_apps_config.json  # Auto-generated app registry
│   └── games/                   # Game JSON configuration files
├── scripts/                     # Python utility scripts
│   ├── organize_files.py        # File organization utility
│   └── setup-flask-app.sh       # Flask app setup script
├── edgeAddons/                  # Browser extensions
│   ├── create-xbox-mkb-extension.sh
│   └── xbox-mkb-extension/
├── archive/                     # Archived/older versions
└── artifacts/                   # Setup scripts and templates
```

## Common Commands Reference

### Repository Navigation
```bash
# Count total applications
find apps -name "*.html" | wc -l    # Should return 96

# List applications by category
ls apps/games/
ls apps/productivity/
ls apps/development/

# Check main gallery
curl -I http://localhost:8080/       # Should return 200 OK
```

### File Operations
```bash
# Check file structure
ls -la                              # See all top-level items

# Verify JSON configuration
cat data/config/utility_apps_config.json | head -20

# Check specific application
curl -I http://localhost:8080/apps/games/3d-world-navigation.html
```

## Troubleshooting

### Server Issues
If HTTP server fails to start:
```bash
# Check if port is in use
lsof -i :8080
# Use different port
python3 -m http.server 8081
```

### Application Not Loading
1. Check file exists: `ls apps/[category]/[filename].html`
2. Verify HTML syntax is valid
3. Check browser console for JavaScript errors
4. Ensure all CSS/JS is inline

### Extension Build Issues
If Xbox extension script fails:
```bash
cd edgeAddons
chmod +x create-xbox-mkb-extension.sh
./create-xbox-mkb-extension.sh
```

## Important Notes

- **No Build Times**: Everything is instant (<1 second) - no "NEVER CANCEL" warnings needed
- **Manual Testing Required**: Always test applications in actual browsers
- **Gallery Integration**: New apps are discovered automatically when placed in correct directories
- **Offline First**: All applications must work without internet connection
- **Self-Contained**: Each HTML file must include all dependencies inline

## Quick Validation Commands

Run these to verify repository health:
```bash
# Verify server works
python3 -m http.server 8080 &
sleep 1
curl -I http://localhost:8080/
killall python3

# Count applications
find apps -name "*.html" | wc -l

# Test key scripts
python3 scripts/organize_files.py
cd edgeAddons && ./create-xbox-mkb-extension.sh && cd ..

# Verify main files exist
ls index.html CLAUDE.md README.md
```

Expected results: Server starts instantly, 96 HTML files found, scripts execute without errors, main files present.