#!/bin/bash

# Vibe Gallery Complete Update & Organization Script
# This script organizes root HTML files and updates the gallery configuration

echo "🎨 Vibe Gallery Update & Organization"
echo "======================================"
echo ""

# Step 1: Organize files from root into categories
echo "📁 Step 1: Organizing root HTML files..."
python3 vibe_gallery_organizer.py

echo ""
echo "📊 Step 2: Updating gallery configuration..."
# Step 2: Run the full gallery update to scan all files
python3 vibe_gallery_watcher.py --once

# Step 3: Show statistics
echo ""
echo "📊 Gallery Statistics:"
python3 -c "
import json
with open('vibe_gallery_config.json', 'r') as f:
    data = json.load(f)
    gallery = data.get('vibeGallery', {})
    categories = gallery.get('categories', {})
    total = sum(len(cat.get('apps', [])) for cat in categories.values())
    print(f'  ✅ Total Apps: {total}')
    print(f'  📁 Categories: {len(categories)}')
    print(f'  📅 Last Updated: {gallery.get(\"lastUpdated\", \"Unknown\")}')
    print()
    print('  Category Breakdown:')
    for cat_name, cat_data in categories.items():
        app_count = len(cat_data.get('apps', []))
        if app_count > 0:
            print(f'    • {cat_data.get(\"title\", cat_name)}: {app_count} apps')
"

echo ""
echo "✨ Gallery update and organization complete!"