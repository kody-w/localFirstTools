#!/bin/bash

# Generate PWA icons from SVG
# Requires: rsvg-convert (librsvg) or ImageMagick

echo "Generating PWA icons..."

# Check if rsvg-convert is available (preferred)
if command -v rsvg-convert &> /dev/null; then
    echo "Using rsvg-convert..."
    rsvg-convert -w 192 -h 192 icon.svg -o icon-192.png
    rsvg-convert -w 512 -h 512 icon.svg -o icon-512.png
    rsvg-convert -w 192 -h 192 icon.svg -o icon-maskable-192.png
    rsvg-convert -w 512 -h 512 icon.svg -o icon-maskable-512.png
    rsvg-convert -w 180 -h 180 icon.svg -o apple-touch-icon.png
    echo "Icons generated successfully with rsvg-convert!"

# Check if ImageMagick is available
elif command -v convert &> /dev/null; then
    echo "Using ImageMagick..."
    convert -background none -resize 192x192 icon.svg icon-192.png
    convert -background none -resize 512x512 icon.svg icon-512.png
    convert -background none -resize 192x192 icon.svg icon-maskable-192.png
    convert -background none -resize 512x512 icon.svg icon-maskable-512.png
    convert -background none -resize 180x180 icon.svg apple-touch-icon.png
    echo "Icons generated successfully with ImageMagick!"

# Check if sips is available (macOS built-in)
elif command -v sips &> /dev/null; then
    echo "Using sips (macOS)..."
    echo "Note: sips doesn't handle SVG well. Installing rsvg-convert is recommended:"
    echo "  brew install librsvg"
    exit 1

else
    echo "Error: No SVG conversion tool found."
    echo ""
    echo "Please install one of the following:"
    echo "  macOS:   brew install librsvg"
    echo "  Ubuntu:  sudo apt-get install librsvg2-bin"
    echo "  Fedora:  sudo dnf install librsvg2-tools"
    echo ""
    echo "Or use ImageMagick:"
    echo "  macOS:   brew install imagemagick"
    echo "  Ubuntu:  sudo apt-get install imagemagick"
    exit 1
fi

echo ""
echo "Generated files:"
echo "  - icon-192.png"
echo "  - icon-512.png"
echo "  - icon-maskable-192.png"
echo "  - icon-maskable-512.png"
echo "  - apple-touch-icon.png"
