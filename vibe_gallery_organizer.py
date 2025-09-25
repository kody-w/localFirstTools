#!/usr/bin/env python3

"""
Vibe Gallery Organizer - Automatically organize HTML files and update config

This script:
1. Scans for HTML files in the root directory
2. Categorizes them based on content analysis
3. Moves them to appropriate category folders
4. Updates vibe_gallery_config.json with new locations
"""

import json
import os
import shutil
import re
from pathlib import Path
from datetime import datetime
import hashlib

# Import existing functions
try:
    from vibe_gallery_updater import (
        extract_metadata_from_html,
        categorize_app
    )
except ImportError:
    print("Warning: vibe_gallery_updater not found, using fallback functions")

def analyze_html_content(filepath):
    """Analyze HTML content to determine appropriate category"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()

        # Category detection patterns
        category_patterns = {
            'games': [
                r'game', r'player', r'score', r'level', r'enemy', r'sprite',
                r'gamepad', r'controller', r'joystick', r'arcade', r'puzzle'
            ],
            'ai-tools': [
                r'ai\s', r'artificial intelligence', r'machine learning', r'copilot',
                r'assistant', r'chatbot', r'gpt', r'claude', r'gemini', r'llm'
            ],
            'media': [
                r'video', r'audio', r'camera', r'recorder', r'player', r'music',
                r'drum', r'sound', r'webcam', r'microphone', r'media'
            ],
            'productivity': [
                r'todo', r'task', r'note', r'document', r'editor', r'writer',
                r'calendar', r'schedule', r'planner', r'organizer', r'workflow'
            ],
            'development': [
                r'code', r'developer', r'github', r'git\s', r'debug', r'terminal',
                r'console', r'compiler', r'ide', r'editor', r'programming'
            ],
            'business': [
                r'crm', r'dashboard', r'analytics', r'report', r'invoice',
                r'customer', r'sales', r'marketing', r'finance', r'accounting'
            ],
            'education': [
                r'learn', r'tutorial', r'teach', r'student', r'course',
                r'training', r'quiz', r'exam', r'study', r'educational'
            ],
            'health': [
                r'health', r'medical', r'fitness', r'exercise', r'wellness',
                r'meditation', r'breathing', r'therapy', r'mental', r'physical'
            ],
            'utilities': [
                r'tool', r'utility', r'converter', r'calculator', r'generator',
                r'analyzer', r'scanner', r'monitor', r'manager', r'helper'
            ]
        }

        # Count pattern matches for each category
        category_scores = {}
        for category, patterns in category_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, content))
                score += matches
            if score > 0:
                category_scores[category] = score

        # Return category with highest score
        if category_scores:
            return f"apps/{max(category_scores, key=category_scores.get)}"

        # Default to utilities if no clear category
        return "apps/utilities"

    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")
        return "apps/utilities"

def should_organize_file(filepath):
    """Check if file should be organized (moved from root)"""
    filename = filepath.name.lower()

    # Skip these files
    skip_files = [
        'index.html',
        'vibe_gallery_config.json',
        'readme.md',
        'license'
    ]

    # Skip if in skip list
    for skip in skip_files:
        if skip in filename:
            return False

    # Skip hidden files
    if filename.startswith('.'):
        return False

    # Only process HTML files
    if not filename.endswith('.html'):
        return False

    return True

def move_file_to_category(filepath, base_path, dry_run=False):
    """Move HTML file to appropriate category folder"""
    # Determine category
    category_path = analyze_html_content(filepath)

    # Create full destination path
    dest_dir = base_path / category_path
    dest_path = dest_dir / filepath.name

    # Check if file already exists in destination
    if dest_path.exists():
        # Add hash suffix to make unique
        hash_suffix = hashlib.md5(str(filepath).encode()).hexdigest()[:8]
        name_parts = filepath.stem, hash_suffix, filepath.suffix
        new_name = f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
        dest_path = dest_dir / new_name

    if dry_run:
        print(f"  Would move: {filepath.name} → {dest_path.relative_to(base_path)}")
        return str(dest_path.relative_to(base_path))
    else:
        # Create directory if it doesn't exist
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Move the file
        shutil.move(str(filepath), str(dest_path))
        print(f"  Moved: {filepath.name} → {dest_path.relative_to(base_path)}")
        return str(dest_path.relative_to(base_path))

def update_gallery_config(base_path, moved_files):
    """Update vibe_gallery_config.json with new file locations"""
    config_path = base_path / "vibe_gallery_config.json"

    # Load existing config
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {"vibeGallery": {"categories": {}}}

    gallery = config.get("vibeGallery", {})
    categories = gallery.get("categories", {})

    # Update file paths for moved files
    for old_path, new_path in moved_files.items():
        # Find and update the file in all categories
        for category_key, category_data in categories.items():
            apps = category_data.get("apps", [])
            for app in apps:
                if app.get("filename") == Path(old_path).name:
                    app["path"] = new_path
                    print(f"  Updated path in config: {old_path} → {new_path}")

    # Update metadata
    gallery["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")

    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n✅ Updated {config_path.name}")

def organize_gallery(base_path, dry_run=False):
    """Main function to organize gallery files"""
    base_path = Path(base_path)
    moved_files = {}

    print("🔍 Scanning for HTML files in root directory...")

    # Find HTML files in root that should be organized
    root_html_files = []
    for filepath in base_path.glob("*.html"):
        if should_organize_file(filepath):
            root_html_files.append(filepath)

    if not root_html_files:
        print("No HTML files found in root that need organizing.")
        return

    print(f"\nFound {len(root_html_files)} files to organize:")
    for filepath in root_html_files:
        print(f"  • {filepath.name}")

    print(f"\n{'🔄 Organizing' if not dry_run else '🔍 Analyzing'} files...")

    # Process each file
    for filepath in root_html_files:
        old_path = filepath.name
        new_path = move_file_to_category(filepath, base_path, dry_run)
        if new_path:
            moved_files[old_path] = new_path

    # Update config if not dry run
    if not dry_run and moved_files:
        print("\n📝 Updating gallery configuration...")
        update_gallery_config(base_path, moved_files)

        # Run the regular updater to ensure everything is in sync
        print("\n🔄 Running full gallery update...")
        os.system("python3 vibe_gallery_watcher.py --once")

    print(f"\n{'✅ Organization complete!' if not dry_run else '✅ Analysis complete (dry run)'}")
    print(f"Files {'moved' if not dry_run else 'would be moved'}: {len(moved_files)}")

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Organize HTML files into category folders and update gallery config',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 vibe_gallery_organizer.py           # Organize files (actually move them)
  python3 vibe_gallery_organizer.py --dry-run # Preview what would be moved
  python3 vibe_gallery_organizer.py --help    # Show this help
        """
    )

    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help="Don't actually move files, just show what would be done"
    )

    parser.add_argument(
        '--path', '-p',
        type=str,
        default='.',
        help='Base path to scan (default: current directory)'
    )

    args = parser.parse_args()

    # Get the base directory
    base_dir = Path(args.path).resolve()

    print("🎨 Vibe Gallery Organizer")
    print("=" * 50)
    print(f"📂 Base directory: {base_dir}")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be moved")
    print()

    organize_gallery(base_dir, dry_run=args.dry_run)

if __name__ == "__main__":
    main()