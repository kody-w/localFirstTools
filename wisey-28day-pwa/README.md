# Wisey 28-Day Brain Plan PWA


A Progressive Web App for the Wisey 28-day brain training program.

## Features

- 📱 **Installable PWA** - Add to home screen on iOS/Android
- 🔌 **Works Offline** - Full functionality without internet
- 💾 **Progress Tracking** - LocalStorage saves your progress
- 📤 **Import/Export** - Backup and sync progress via JSON
- ⏱️ **Built-in Timer** - 15-minute session timer for each day

## Installation to localFirstTools

### Quick Setup

1. **Copy the `wisey-28day-pwa` folder** to your `localFirstTools` repository:

```bash
# Clone your repo (if not already)
git clone https://github.com/kody-w/localFirstTools.git
cd localFirstTools

# Copy the wisey-28day-pwa folder into it
# (assuming you downloaded/extracted it somewhere)
cp -r /path/to/wisey-28day-pwa ./wisey-28day-pwa

# Commit and push
git add .
git commit -m "Add Wisey 28-Day Brain Plan PWA"
git push
```

2. **Access via GitHub Pages**:
   - URL will be: `https://kody-w.github.io/localFirstTools/wisey-28day-pwa/`

### File Structure

```
wisey-28day-pwa/
├── index.html      # Main app (all-in-one HTML)
├── manifest.json   # PWA manifest
├── sw.js          # Service worker for offline
├── icon-192.png   # App icon (192x192)
├── icon-512.png   # App icon (512x512)
└── README.md      # This file
```

## Usage on iPhone

1. Open the URL in Safari
2. Tap the **Share** button (square with arrow)
3. Scroll down and tap **"Add to Home Screen"**
4. Tap **"Add"** to confirm

The app will appear on your home screen and work offline!

## Sharing via iMessage

Simply share the GitHub Pages URL:
```
https://kody-w.github.io/localFirstTools/wisey-28day-pwa/
```

Recipients can add it to their home screen too.

## Progress Sync Between Devices

Since each device has its own localStorage:

1. **Export** progress on Device A (downloads JSON file)
2. Transfer JSON file to Device B (AirDrop, iMessage, email)
3. **Import** the JSON file on Device B

## Customizing Icons

To create custom icons with the brain emoji:

1. Use an online tool like [Favicon.io](https://favicon.io/emoji-favicons/)
2. Search for "brain" emoji
3. Download and replace `icon-192.png` and `icon-512.png`

## Tech Stack

- Pure HTML/CSS/JavaScript (no frameworks)
- Service Worker for offline caching
- Web App Manifest for PWA features
- LocalStorage for progress persistence
