# LEVIATHAN World Browser Extension

A Chrome/Edge extension that allows you to browse and import public world seeds into LEVIATHAN: OMNIVERSE directly from GitHub.

## Features

- Browse public worlds from the LEVIATHAN world registry
- Filter by category: Featured, Exploration, Story, Creative, Challenge
- One-click import into the game
- Works with locally hosted or GitHub Pages hosted game
- Automatic world detection when game is running
- Caches registry for faster loading

## Installation

### Method 1: Quick Install (Recommended)

1. **Get Icons from GitHub Pages**:
   - Go to: https://kody-w.github.io/localFirstTools/assets/icons/
   - Click "Download All Icons (PNG)"
   - Save icons to this `world-browser-extension` folder

2. **Load the Extension**:
   - Open Chrome/Edge
   - Navigate to `chrome://extensions` (or `edge://extensions`)
   - Enable "Developer mode" (toggle in top right)
   - Click "Load unpacked"
   - Select this `world-browser-extension` folder

3. **Pin the Extension**:
   - Click the puzzle piece icon in your toolbar
   - Pin "LEVIATHAN World Browser"

### Method 2: Generate Icons Locally

1. Open `generate-icons.html` in your browser
2. Click "Download All Icons"
3. Follow steps 2-3 above

### Method 3: Build ZIP

```bash
./build.sh
```

This creates `leviathan-world-browser.zip` - drag onto extensions page.

## Hosted Assets

Icons are permanently hosted on GitHub Pages:

| Size | URL |
|------|-----|
| 16x16 | https://kody-w.github.io/localFirstTools/assets/icons/world-browser-16.svg |
| 48x48 | https://kody-w.github.io/localFirstTools/assets/icons/world-browser-48.svg |
| 128x128 | https://kody-w.github.io/localFirstTools/assets/icons/world-browser-128.svg |

Icon generator page: https://kody-w.github.io/localFirstTools/assets/icons/

## Usage

1. Click the extension icon in your toolbar
2. Browse available worlds
3. Click "Import World" on any world you want
4. If LEVIATHAN is open, the world imports immediately
5. If not, worlds are saved and import when you open the game

## How It Works

The extension fetches the world registry from:
- `https://kody-w.github.io/localFirstTools/data/public-worlds/registry.json`

When you import a world, it:
1. Downloads the world seed JSON
2. Stores it in the game's localStorage
3. Notifies the game via a custom event
4. Shows an in-game banner confirming import

## Files

| File | Purpose |
|------|---------|
| `manifest.json` | Extension configuration |
| `popup.html` | World browser UI |
| `popup.js` | Fetching and display logic |
| `content.js` | Game integration |
| `background.js` | Service worker |
| `generate-icons.html` | Icon generator |
| `build.sh` | Build script |

## World Registry Format

```json
{
  "version": "1.0.0",
  "worlds": [
    {
      "id": "volcano-prime",
      "name": "Volcano Prime",
      "author": "kodywildfeuer",
      "description": "...",
      "category": "exploration",
      "tags": ["volcanic", "ruins"],
      "featured": true
    }
  ]
}
```

## Adding New Worlds

To add a world to the public registry:

1. Create a world seed JSON in `data/public-worlds/seeds/`
2. Add an entry to `data/public-worlds/registry.json`
3. Commit and push to GitHub

## Troubleshooting

**Extension not loading?**
- Ensure all icon files exist (use generate-icons.html)
- Check browser console for errors

**Can't import worlds?**
- Verify you're on the LEVIATHAN game page
- Check that the game has finished loading
- Look for import banners/notifications

**Registry not loading?**
- Check internet connection
- Verify GitHub Pages is accessible
- Try the "Refresh" button

## License

Part of the LEVIATHAN: OMNIVERSE project.
