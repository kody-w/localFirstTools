import json
import os
import sys

def check_gallery_config(config_path):
    """
    Scans the gallery config and verifies that all referenced files exist.
    """
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return

    print(f"🔍 Scanning {config_path}...")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config file: {e}")
        return

    root_dir = os.path.dirname(os.path.abspath(config_path))
    
    missing_files = []
    total_apps = 0
    checked_paths = 0

    # Navigate the structure: vibeGallery -> categories -> [category] -> apps
    gallery = data.get('vibeGallery', {})
    categories = gallery.get('categories', {})

    for cat_id, cat_data in categories.items():
        apps = cat_data.get('apps', [])
        print(f"  📂 Checking category: {cat_data.get('title', cat_id)} ({len(apps)} apps)")
        
        for app in apps:
            total_apps += 1
            app_title = app.get('title', 'Unknown App')
            
            # Check main path
            main_path = app.get('path')
            if main_path:
                full_path = os.path.join(root_dir, main_path)
                checked_paths += 1
                if not os.path.exists(full_path):
                    missing_files.append({
                        'type': 'Main App',
                        'title': app_title,
                        'path': main_path,
                        'category': cat_id
                    })

            # Check versions if they exist
            versions = app.get('versions', [])
            for v in versions:
                v_path = v.get('path')
                if v_path:
                    full_path = os.path.join(root_dir, v_path)
                    checked_paths += 1
                    if not os.path.exists(full_path):
                        missing_files.append({
                            'type': 'Version',
                            'title': app_title,
                            'path': v_path,
                            'category': cat_id
                        })

    print("\n" + "="*50)
    print(f"📊 SUMMARY")
    print(f"   Total Apps Checked: {total_apps}")
    print(f"   Total Paths Verified: {checked_paths}")
    
    if missing_files:
        print(f"❌ Found {len(missing_files)} broken paths:")
        print("="*50)
        for missing in missing_files:
            print(f"  • [{missing['category']}] {missing['title']}")
            print(f"    Type: {missing['type']}")
            print(f"    Missing Path: {missing['path']}")
            print("-" * 30)
        sys.exit(1)
    else:
        print("✅ All paths are valid! No ghosts found.")
        sys.exit(0)

if __name__ == "__main__":
    # Default to looking in current directory
    config_file = "vibe_gallery_config.json"
    check_gallery_config(config_file)
