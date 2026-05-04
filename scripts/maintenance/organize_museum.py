#!/usr/bin/env python3

import os
import json
import shutil
import re
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = BASE_DIR / "vibe_gallery_config.json"
EXHIBITION_HALLS = BASE_DIR / "Exhibition_Halls"

# Category Mapping
CATEGORY_MAPPING = {
    "visual_art": "Visual_Arts",
    "generative_art": "Visual_Arts",
    "3d_immersive": "Simulation_Lab",
    "particle_physics": "Simulation_Lab",
    "games_puzzles": "The_Arcade",
    "audio_music": "Sound_Studio",
    "creative_tools": "Productivity_Suite",
    "experimental_ai": "AI_Research",
    "educational_tools": "Educational_Center"
}

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def get_relative_path(from_path, to_path):
    """Calculate relative path from one file to another"""
    return os.path.relpath(to_path, from_path.parent)

def update_links(content, depth_diff):
    """Update relative links in HTML content based on depth change"""
    if depth_diff == 0:
        return content
        
    prefix = "../" * depth_diff
    
    def replace_link(match):
        attr, quote, url = match.groups()
        if url.startswith(('http', 'https', '#', 'mailto:', 'javascript:', 'data:', '/')):
            return match.group(0)
        
        # Don't double prefix if it already looks like we are adjusting
        # But simple logic: just prepend prefix
        return f'{attr}={quote}{prefix}{url}{quote}'
        
    # Regex for href and src attributes
    pattern = r'(href|src)=("|\')([^"\']+)\2'
    return re.sub(pattern, replace_link, content)

def create_ghost_file(old_path, new_path):
    """Create a redirect stub at the old path"""
    rel_new_path = get_relative_path(old_path, new_path)
    
    ghost_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url={rel_new_path}">
    <script>window.location.replace("{rel_new_path}");</script>
    <title>Redirecting...</title>
    <style>
        body {{ font-family: system-ui, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #111; color: #eee; }}
        .card {{ background: #222; padding: 2rem; border-radius: 1rem; text-align: center; border: 1px solid #333; }}
        a {{ color: #4ecdc4; }}
    </style>
</head>
<body>
    <div class="card">
        <p>This artwork has been moved to the <a href="{rel_new_path}">Exhibition Halls</a>.</p>
        <p><small>Redirecting you now...</small></p>
    </div>
</body>
</html>"""
    
    with open(old_path, 'w') as f:
        f.write(ghost_content)
    print(f"👻 Created ghost at {old_path.relative_to(BASE_DIR)}")

def move_file(file_entry, category):
    filename = file_entry['filename']
    current_rel_path = file_entry.get('path', filename)
    
    # Handle case where path might be just filename but file is in root
    if current_rel_path == filename:
        current_path = BASE_DIR / filename
    else:
        current_path = BASE_DIR / current_rel_path
        
    if not current_path.exists():
        print(f"⚠️ File not found: {current_path}")
        return

    # Determine target wing
    wing = CATEGORY_MAPPING.get(category, "The_Workshop")
    target_dir = EXHIBITION_HALLS / wing
    target_path = target_dir / filename
    
    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Calculate depth difference
    # Root is depth 0. Exhibition_Halls/Wing is depth 2.
    # If file was at root, depth diff is 2.
    # If file was at apps/subdir, depth is 2. Diff is 0.
    
    old_depth = len(current_path.relative_to(BASE_DIR).parts) - 1
    new_depth = len(target_path.relative_to(BASE_DIR).parts) - 1
    depth_diff = new_depth - old_depth
    
    # Read content
    try:
        with open(current_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"❌ Error reading {filename}, skipping link updates")
        content = None

    # Move file (copy then delete to be safe, or rename)
    # We need to keep the old path for the ghost file
    
    # 1. Write new file with updated links
    if content:
        new_content = update_links(content, depth_diff)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        shutil.copy2(current_path, target_path)
        
    print(f"🚚 Moved {filename} -> {wing}")
    
    # 2. Create ghost at old path
    create_ghost_file(current_path, target_path)

def main():
    print("🏛️  Starting Museum Reorganization...")
    config = load_config()
    
    categories = config.get('vibeGallery', {}).get('categories', {})
    
    for cat_key, cat_data in categories.items():
        print(f"\nProcessing Category: {cat_data['title']}")
        for app in cat_data.get('apps', []):
            move_file(app, cat_key)
            
            # Handle versions if any
            if 'versions' in app:
                for version in app['versions']:
                    move_file(version, cat_key)

    print("\n✨ Reorganization Complete!")

if __name__ == "__main__":
    main()
