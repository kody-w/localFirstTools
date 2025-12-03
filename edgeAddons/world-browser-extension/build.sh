#!/bin/bash
# LEVIATHAN World Browser - Build Script
# Creates a distributable ZIP file for the Chrome/Edge extension

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"
ZIP_NAME="leviathan-world-browser.zip"

echo "🌌 Building LEVIATHAN World Browser Extension..."

# Clean previous build
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Copy extension files
cp "$SCRIPT_DIR/manifest.json" "$BUILD_DIR/"
cp "$SCRIPT_DIR/popup.html" "$BUILD_DIR/"
cp "$SCRIPT_DIR/popup.js" "$BUILD_DIR/"
cp "$SCRIPT_DIR/content.js" "$BUILD_DIR/"
cp "$SCRIPT_DIR/background.js" "$BUILD_DIR/"

# Check for icons
if [ -f "$SCRIPT_DIR/icon16.png" ]; then
    cp "$SCRIPT_DIR/icon16.png" "$BUILD_DIR/"
    cp "$SCRIPT_DIR/icon48.png" "$BUILD_DIR/"
    cp "$SCRIPT_DIR/icon128.png" "$BUILD_DIR/"
else
    echo "⚠️  Icons not found. Open generate-icons.html in a browser to create them."
    echo "   Then save them to this directory as icon16.png, icon48.png, icon128.png"
fi

# Create ZIP
cd "$BUILD_DIR"
rm -f "$SCRIPT_DIR/$ZIP_NAME"
zip -r "$SCRIPT_DIR/$ZIP_NAME" ./*

echo ""
echo "✅ Build complete!"
echo "   ZIP file: $SCRIPT_DIR/$ZIP_NAME"
echo ""
echo "📦 To install:"
echo "   1. Open Chrome/Edge and go to chrome://extensions"
echo "   2. Enable 'Developer mode' (toggle in top right)"
echo "   3. Click 'Load unpacked' and select: $BUILD_DIR"
echo "   OR"
echo "   3. Drag and drop $ZIP_NAME onto the extensions page"
echo ""
