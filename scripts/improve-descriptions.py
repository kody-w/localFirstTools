#!/usr/bin/env python3
"""
Improve generic descriptions in utility_apps_config.json by extracting
meaningful information from HTML files.
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


def create_description(title, meta_description, category):
    """Create a meaningful description from title and meta description"""
    if meta_description:
        return meta_description

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
        "index-variants": f"{title_clean} - Alternative gallery index layout",
        "archive": f"{title_clean} - Archived application"
    }

    # Map category to description template
    for key in descriptions:
        if key in category.lower():
            return descriptions[key]

    return f"{title_clean}"


def main():
    """Main function to improve descriptions"""
    config_path = Path(__file__).parent.parent / "data" / "config" / "utility_apps_config.json"

    print("📝 Improving App Descriptions")
    print("=" * 60)

    # Read config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Create backup
    backup_path = config_path.with_suffix(f'.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ Created backup: {backup_path.name}\n")

    # Track improvements
    improved = 0
    failed = 0

    # Process each app
    for app in config['apps']:
        app_id = app['id']
        current_desc = app['description']
        path = app['path']

        # Check if description is generic
        if current_desc.startswith("A ") and current_desc.endswith(" application"):
            # Extract category from current description
            category = current_desc.replace("A ", "").replace(" application", "")

            # Construct full path
            full_path = Path(__file__).parent.parent / path.lstrip('./')

            if not full_path.exists():
                print(f"❌ {app_id}: File not found at {path}")
                failed += 1
                continue

            # Extract metadata
            title, meta_desc = extract_metadata(full_path)

            if title:
                new_desc = create_description(title, meta_desc, category)

                # Update config
                app['description'] = new_desc

                print(f"✅ {app_id}")
                print(f"   Old: {current_desc}")
                print(f"   New: {new_desc}")
                print()

                improved += 1
            else:
                print(f"⚠️  {app_id}: Could not extract title from {path}")
                failed += 1

    # Update timestamp
    config['lastUpdated'] = datetime.now().isoformat()

    # Save updated config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print(f"\n✨ Done!")
    print(f"   Improved: {improved} descriptions")
    print(f"   Failed: {failed} apps")
    print(f"   Backup: {backup_path.name}")


if __name__ == "__main__":
    main()
