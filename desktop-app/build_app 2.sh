#!/bin/bash

# Ensure we are in the desktop-app directory
cd "$(dirname "$0")"

echo "🧹 Cleaning previous build..."
rm -rf dist
mkdir -p dist

echo "📦 Copying files to dist..."
# Copy everything from root to dist, excluding desktop-app, .git, and other non-app files
# We use rsync for this
rsync -av --progress ../* dist/ \
    --exclude "desktop-app" \
    --exclude ".git" \
    --exclude ".github" \
    --exclude "node_modules" \
    --exclude "target" \
    --exclude "*.zip" \
    --exclude "venv" \
    --exclude "__pycache__"

echo "✅ Files prepared in desktop-app/dist"
echo "🚀 Building Tauri app..."

# Check if cargo is installed
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust/Cargo is not installed. Please install Rust: https://rustup.rs/"
    exit 1
fi

# Check if tauri-cli is installed
if ! cargo tauri --version &> /dev/null; then
    echo "⚠️  Tauri CLI not found. Installing..."
    cargo install tauri-cli
fi

# Build
cargo tauri build

echo "🎉 Build complete! Check desktop-app/src-tauri/target/release/bundle/"
