#!/usr/bin/env python3

"""
Quick Gallery Update - Refresh vibe_gallery_config.json with a single command

Usage:
    python3 update_gallery.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Import the updater function
from vibe_gallery_updater import update_vibe_gallery_config

def main():
    print("🎨 Vibe Gallery Quick Update")
    print("=" * 50)

    # Get the base directory
    base_dir = Path.cwd()

    # Show what we're updating
    config_path = base_dir / "vibe_gallery_config.json"
    print(f"📂 Scanning directory: {base_dir}")
    print(f"📄 Updating file: {config_path}")
    print("=" * 50)

    # Run the update
    try:
        start_time = datetime.now()
        update_vibe_gallery_config(base_dir)

        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        print(f"\n⏱️  Update completed in {duration:.2f} seconds")
        print(f"🎉 Gallery config is now up to date!")

    except Exception as e:
        print(f"\n❌ Error during update: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()