#!/bin/bash

# Vibe Gallery Update Script
# Quick way to refresh the gallery configuration

echo "🎨 Updating Vibe Gallery..."
python3 scripts/gallery/update_gallery.py

# Optional: Show summary of changes
echo ""
echo "📊 Gallery Statistics:"
python3 -c "
import json
with open('vibe_gallery_config.json', 'r') as f:
    data = json.load(f)
    gallery = data.get('vibeGallery', {})
    categories = gallery.get('categories', {})
    total = sum(len(cat.get('apps', [])) for cat in categories.values())
    print(f'  Total Apps: {total}')
    print(f'  Categories: {len(categories)}')
    print(f'  Last Updated: {gallery.get(\"lastUpdated\", \"Unknown\")}')
"