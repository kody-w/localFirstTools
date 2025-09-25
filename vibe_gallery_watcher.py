#!/usr/bin/env python3

"""
Vibe Gallery Watcher - Auto-update vibe_gallery_config.json when HTML files change

Usage:
    python3 vibe_gallery_watcher.py          # Watch mode - auto-updates on changes
    python3 vibe_gallery_watcher.py --once   # Run once and exit
"""

import json
import os
import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime
import argparse
import subprocess

# Import the updater functions
from vibe_gallery_updater import (
    extract_metadata_from_html,
    categorize_app,
    scan_directories_for_apps,
    update_vibe_gallery_config
)

class VibeGalleryWatcher:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.config_path = self.base_path / "vibe_gallery_config.json"
        self.file_hashes = {}
        self.last_update = None

    def get_all_html_files(self):
        """Get all HTML files in the project"""
        html_files = set()

        # Scan apps directory
        apps_path = self.base_path / "apps"
        if apps_path.exists():
            for html_file in apps_path.rglob("*.html"):
                if not html_file.name.startswith('.'):
                    html_files.add(html_file)

        # Scan root directory
        for html_file in self.base_path.glob("*.html"):
            if not html_file.name.startswith('.') and html_file.name != 'index.html':
                html_files.add(html_file)

        # Scan other directories
        other_dirs = ["artifacts", "archive", "notes", "edgeAddons"]
        for dir_name in other_dirs:
            dir_path = self.base_path / dir_name
            if dir_path.exists():
                for html_file in dir_path.rglob("*.html"):
                    if not html_file.name.startswith('.'):
                        html_files.add(html_file)

        return html_files

    def get_file_hash(self, filepath):
        """Get MD5 hash of file content"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def check_for_changes(self):
        """Check if any HTML files have been added, removed, or modified"""
        current_files = self.get_all_html_files()
        current_hashes = {}
        changes_detected = False

        # Check for new or modified files
        for html_file in current_files:
            current_hash = self.get_file_hash(html_file)
            current_hashes[str(html_file)] = current_hash

            if str(html_file) not in self.file_hashes:
                print(f"✨ New file detected: {html_file.relative_to(self.base_path)}")
                changes_detected = True
            elif self.file_hashes[str(html_file)] != current_hash:
                print(f"📝 File modified: {html_file.relative_to(self.base_path)}")
                changes_detected = True

        # Check for removed files
        for old_file in self.file_hashes:
            if old_file not in current_hashes:
                print(f"🗑️  File removed: {Path(old_file).relative_to(self.base_path)}")
                changes_detected = True

        self.file_hashes = current_hashes
        return changes_detected

    def update_config(self):
        """Update the vibe_gallery_config.json file"""
        print("🔄 Updating vibe_gallery_config.json...")
        update_vibe_gallery_config(self.base_path)
        self.last_update = datetime.now()
        print(f"✅ Config updated at {self.last_update.strftime('%H:%M:%S')}")

    def run_once(self):
        """Run the updater once and exit"""
        print("🚀 Running Vibe Gallery Updater...")
        print("=" * 50)
        self.update_config()

    def watch(self, interval=2):
        """Watch for changes and auto-update"""
        print("👁️  Vibe Gallery Watcher Started")
        print(f"📂 Watching: {self.base_path}")
        print(f"📄 Config file: {self.config_path}")
        print("=" * 50)
        print("Press Ctrl+C to stop watching\n")

        # Initial scan
        self.check_for_changes()
        self.update_config()

        try:
            while True:
                time.sleep(interval)
                if self.check_for_changes():
                    self.update_config()
        except KeyboardInterrupt:
            print("\n\n👋 Watcher stopped")
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description='Vibe Gallery Watcher - Auto-update gallery config when files change',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 vibe_gallery_watcher.py          # Watch mode (auto-updates on changes)
  python3 vibe_gallery_watcher.py --once   # Run once and exit
  python3 vibe_gallery_watcher.py --quick  # Quick update (alias for --once)
        """
    )

    parser.add_argument(
        '--once', '--quick', '-q',
        action='store_true',
        help='Run once and exit (don\'t watch for changes)'
    )

    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=2,
        help='Check interval in seconds (default: 2)'
    )

    args = parser.parse_args()

    # Get the base directory
    base_dir = Path.cwd()

    # Create watcher
    watcher = VibeGalleryWatcher(base_dir)

    if args.once:
        watcher.run_once()
    else:
        watcher.watch(interval=args.interval)

if __name__ == "__main__":
    main()