#!/bin/bash

echo "🏗️  Building Chrome Extension..."

# Create build directory
BUILD_DIR="chrome-extension-build"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "📦 Copying files..."

# Copy extension files
cp -r chrome-extension/* "$BUILD_DIR/"

# Copy essential app files
mkdir -p "$BUILD_DIR/apps"
mkdir -p "$BUILD_DIR/data"

# Copy index.html
cp index.html "$BUILD_DIR/"

# Copy config data
cp -r data/config "$BUILD_DIR/data/"
cp data/meta-analysis.json "$BUILD_DIR/data/" 2>/dev/null || true

# Copy all apps
cp -r apps/* "$BUILD_DIR/apps/"

# Create placeholder icons if they don't exist
mkdir -p "$BUILD_DIR/icons"

# Create simple icon using ImageMagick or base64 placeholder
cat > "$BUILD_DIR/icons/icon-16.png" << 'EOF'
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAFFSURBVDiNpdIxS8NAGMbx3yVpY1GxOLiIk4ODo5ODgpNDZ8HJQfwGfgAHR0cHZ0cHBwe/gIODk4ODk4ODk4ODk4ODk4iKWkubXgeRNNfLJf7hfbj3uXsfRATLsiAiWJYFEcGyLIgIlmVBRLAsC8CfAJZlQUSwLAsiQq1Ww/d9PM+j3W7jui6u6+K6Lq7r4rouruvS6XSwbRvbtrFtG9u2sW0b27axbRvbtrFtm263S7/fp9/v0+/36ff79Pt9+v0+g8GAwWDAYDBgMBgwGAwYDAYMh0OGwyHD4ZDhcMhwOGQ4HDIajRiNRoxGI0ajEaPRiNFoxHg8ZjweA2BZFrZtY9s2tm1j2za2bWPbNp7n4XkenueyXq/xfR/P8/A8D8/z8DwPz/PwPA/f9/F9H9/38X0f3/fxfR/f9/F9H9/3EZEPP77v4/s+IvILxKVwnzc+4FcAAAAASUVORK5CYII=
EOF

# Copy for other sizes
cp "$BUILD_DIR/icons/icon-16.png" "$BUILD_DIR/icons/icon-32.png"
cp "$BUILD_DIR/icons/icon-16.png" "$BUILD_DIR/icons/icon-48.png"
cp "$BUILD_DIR/icons/icon-16.png" "$BUILD_DIR/icons/icon-128.png"

echo "📊 Package statistics:"
echo "  - Total size: $(du -sh "$BUILD_DIR" | cut -f1)"
echo "  - Apps: $(find "$BUILD_DIR/apps" -name "*.html" | wc -l)"

echo ""
echo "✅ Chrome Extension built successfully!"
echo ""
echo "📦 Package location: ./$BUILD_DIR"
echo ""
echo "To install:"
echo "1. Open Chrome and go to: chrome://extensions/"
echo "2. Enable 'Developer mode' (top right)"
echo "3. Click 'Load unpacked'"
echo "4. Select the '$BUILD_DIR' directory"
echo ""
echo "🚀 Enjoy your Local First Tools extension!"
