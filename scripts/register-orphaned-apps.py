#!/usr/bin/env python3
"""
Register orphaned HTML applications in utility_apps_config.json.
Scans apps/ directory for HTML files not yet in the config and adds them.
"""

import json
import re
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime


class TitleExtractor(HTMLParser):
    """Extract title and meta description from HTML file"""
    def __init__(self):
        super().__init__()
        self.title = None
        self.description = None
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            attrs_dict = dict(attrs)
            if attrs_dict.get("name") == "description":
                self.description = attrs_dict.get("content", "").strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and self.title is None:
            self.title = data.strip()


def extract_metadata(filepath):
    """Extract title and description from HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(10000)  # Read first 10KB for performance

        parser = TitleExtractor()
        parser.feed(content)
        return parser.title, parser.description
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None, None


def get_category_from_path(path):
    """Determine category from file path"""
    path_str = str(path)

    if '/ai-tools/' in path_str:
        return 'ai-tools', '🤖', ['ai', 'tools']
    elif '/business/' in path_str:
        return 'business', '💼', ['business']
    elif '/development/' in path_str:
        return 'development', '💻', ['development', 'tools']
    elif '/education/' in path_str:
        return 'education', '🎓', ['education']
    elif '/games/' in path_str:
        return 'games', '🎮', ['games']
    elif '/media/' in path_str:
        return 'media', '📹', ['media']
    elif '/productivity/' in path_str:
        return 'productivity', '📋', ['productivity']
    elif '/utilities/' in path_str:
        return 'utilities', '🔧', ['utility']
    elif '/health/' in path_str:
        return 'health', '💪', ['health', 'wellness']
    elif '/quantum-worlds/' in path_str:
        return 'quantum-worlds', '🌌', ['quantum-worlds', 'games', 'p2p', 'multiplayer']
    elif '/index-variants/' in path_str:
        return 'index-variants', '📄', ['utility']
    else:
        return 'utilities', '🔧', ['utility']


def create_description(title, meta_description, category):
    """Create a meaningful description from title and meta description"""
    if meta_description:
        # Clean up meta description
        desc = meta_description.strip()
        # Limit length
        if len(desc) > 200:
            desc = desc[:197] + "..."
        return desc

    if not title:
        return f"A {category} application"

    # Clean up the title
    title_clean = title.strip()

    # Create description based on category and title
    descriptions = {
        "ai-tools": f"{title_clean} - AI-powered tool for enhanced productivity and automation",
        "business": f"{title_clean} - Business management and productivity tool",
        "development": f"{title_clean} - Development tool for building and debugging applications",
        "education": f"{title_clean} - Educational tool for learning and teaching",
        "games": f"{title_clean} - Interactive game experience",
        "media": f"{title_clean} - Media creation and editing tool",
        "productivity": f"{title_clean} - Productivity tool for task management and organization",
        "utilities": f"{title_clean} - Utility tool for everyday tasks",
        "health": f"{title_clean} - Health and wellness tracking tool",
        "quantum-worlds": f"{title_clean} - Experimental P2P networked universe",
        "index-variants": f"{title_clean} - Alternative gallery index layout",
    }

    return descriptions.get(category, f"{title_clean}")


def scan_for_orphaned_apps(config, project_root):
    """Scan for HTML files not in config"""
    # Get all existing paths from config
    existing_paths = set()
    existing_ids = set()

    for app in config['apps']:
        # Normalize path
        normalized_path = app['path'].lstrip('./')
        existing_paths.add(normalized_path)
        existing_ids.add(app['id'])

    print(f"📊 Current config has {len(existing_paths)} apps registered\n")

    # Scan apps directory
    apps_dir = project_root / "apps"
    orphaned_apps = []

    # Files/directories to exclude
    exclude_files = {'index.html', 'template.html', 'example.html', 'test.html'}

    # Scan all subdirectories
    for html_file in apps_dir.rglob("*.html"):
        if html_file.name.lower() in exclude_files:
            continue

        # Get relative path
        rel_path = html_file.relative_to(project_root)
        rel_path_str = str(rel_path)

        # Check if already in config
        if rel_path_str not in existing_paths and f"./{rel_path_str}" not in existing_paths:
            orphaned_apps.append(html_file)

    # Also check root directory for specific files
    root_files = ['levi.html', 'quantum-worlds-store.html', 'db-viewer-index.html']
    for filename in root_files:
        file_path = project_root / filename
        if file_path.exists():
            rel_path_str = filename
            if rel_path_str not in existing_paths and f"./{rel_path_str}" not in existing_paths:
                orphaned_apps.append(file_path)

    return orphaned_apps


def create_app_entry(filepath, project_root, existing_ids):
    """Create a new app entry from HTML file"""
    # Extract metadata
    title, meta_desc = extract_metadata(filepath)

    if not title:
        title = filepath.stem.replace('-', ' ').replace('_', ' ').title()

    # Get relative path
    rel_path = filepath.relative_to(project_root)

    # Determine category
    category, icon, tags = get_category_from_path(rel_path)

    # Create description
    description = create_description(title, meta_desc, category)

    # Generate unique ID
    base_id = filepath.stem
    app_id = base_id
    counter = 1
    while app_id in existing_ids:
        app_id = f"{base_id}-{counter}"
        counter += 1

    return {
        "id": app_id,
        "title": title,
        "description": description,
        "tags": tags,
        "path": f"./{rel_path}",
        "icon": icon
    }


def main():
    """Main function to register orphaned applications"""
    project_root = Path(__file__).parent.parent
    config_path = project_root / "data" / "config" / "utility_apps_config.json"

    print("🔍 Scanning for Orphaned Applications")
    print("=" * 60)

    # Read config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Create backup
    backup_path = config_path.with_suffix(f'.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ Created backup: {backup_path.name}\n")

    # Find orphaned apps
    orphaned_apps = scan_for_orphaned_apps(config, project_root)

    if not orphaned_apps:
        print("✨ No orphaned applications found! All apps are registered.")
        return

    print(f"📦 Found {len(orphaned_apps)} orphaned applications:\n")

    # Get existing IDs
    existing_ids = {app['id'] for app in config['apps']}

    # Create entries for orphaned apps
    new_apps = []
    for filepath in sorted(orphaned_apps):
        try:
            app_entry = create_app_entry(filepath, project_root, existing_ids)
            new_apps.append(app_entry)
            existing_ids.add(app_entry['id'])

            print(f"✅ {app_entry['icon']} {app_entry['title']}")
            print(f"   ID: {app_entry['id']}")
            print(f"   Path: {app_entry['path']}")
            print(f"   Description: {app_entry['description'][:80]}...")
            print()

        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}\n")

    # Add new apps to config
    config['apps'].extend(new_apps)

    # Sort apps by category then title
    config['apps'].sort(key=lambda x: (x.get('tags', [''])[0], x['title']))

    # Update timestamp
    config['lastUpdated'] = datetime.now().isoformat()

    # Save updated config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print(f"\n✨ Done!")
    print(f"   Added: {len(new_apps)} new applications")
    print(f"   Total apps: {len(config['apps'])}")
    print(f"   Backup: {backup_path.name}")


if __name__ == "__main__":
    main()
