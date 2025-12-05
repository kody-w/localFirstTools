#!/usr/bin/env python3
"""
Moves all HTML files from subdirectories to the root directory.
Handles naming conflicts by appending numbers to duplicates.
"""

import os
import shutil
from pathlib import Path

def get_unique_filename(root_dir, original_name):
    """Generate a unique filename if there's a conflict"""
    target_path = root_dir / original_name

    if not target_path.exists():
        return original_name

    # Split name and extension
    name_parts = original_name.rsplit('.', 1)
    base_name = name_parts[0]
    extension = name_parts[1] if len(name_parts) > 1 else ''

    # Try appending numbers until we find a unique name
    counter = 1
    while True:
        new_name = f"{base_name}-{counter}.{extension}" if extension else f"{base_name}-{counter}"
        if not (root_dir / new_name).exists():
            return new_name
        counter += 1

def flatten_html_files():
    """Move all HTML files from subdirectories to root"""
    root_dir = Path('.')
    moved_files = []
    skipped_files = []
    errors = []

    # Directories to search (excluding some that shouldn't be touched)
    exclude_dirs = {'.git', 'node_modules', '.next', 'build', 'dist', '__pycache__'}

    print("🔍 Searching for HTML files in subdirectories...")

    # Find all HTML files in subdirectories
    for subdir in root_dir.iterdir():
        if subdir.is_dir() and subdir.name not in exclude_dirs:
            # Search recursively in this subdirectory
            for html_file in subdir.rglob('*.html'):
                # Skip if it's already in root
                if html_file.parent == root_dir:
                    continue

                original_name = html_file.name
                relative_path = html_file.relative_to(root_dir)

                # Skip index.html files from subdirectories (they're usually specific to that dir)
                if original_name == 'index.html':
                    skipped_files.append(str(relative_path))
                    continue

                # Get unique filename for root directory
                new_name = get_unique_filename(root_dir, original_name)
                new_path = root_dir / new_name

                try:
                    # Move the file
                    shutil.move(str(html_file), str(new_path))
                    moved_files.append({
                        'from': str(relative_path),
                        'to': new_name,
                        'renamed': new_name != original_name
                    })
                    print(f"✓ Moved: {relative_path} → {new_name}")

                except Exception as e:
                    errors.append({
                        'file': str(relative_path),
                        'error': str(e)
                    })
                    print(f"✗ Error moving {relative_path}: {e}")

    # Print summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)

    print(f"\n✓ Moved {len(moved_files)} files to root directory")
    if moved_files:
        for item in moved_files[:10]:  # Show first 10
            if item['renamed']:
                print(f"  • {item['from']} → {item['to']} (renamed)")
            else:
                print(f"  • {item['from']} → {item['to']}")
        if len(moved_files) > 10:
            print(f"  ... and {len(moved_files) - 10} more")

    if skipped_files:
        print(f"\n⊘ Skipped {len(skipped_files)} index.html files from subdirectories")
        for file in skipped_files[:5]:  # Show first 5
            print(f"  • {file}")
        if len(skipped_files) > 5:
            print(f"  ... and {len(skipped_files) - 5} more")

    if errors:
        print(f"\n✗ Failed to move {len(errors)} files")
        for err in errors:
            print(f"  • {err['file']}: {err['error']}")

    # Clean up empty directories (optional)
    print("\n🧹 Cleaning up empty directories...")
    cleaned = []
    for subdir in root_dir.iterdir():
        if subdir.is_dir() and subdir.name not in exclude_dirs:
            # Check if directory is empty (recursively)
            if not any(subdir.rglob('*')):
                try:
                    shutil.rmtree(str(subdir))
                    cleaned.append(subdir.name)
                    print(f"  ✓ Removed empty directory: {subdir.name}")
                except:
                    pass

    if not cleaned:
        print("  No empty directories to remove")

    print("\n✨ Flattening complete!")
    print("Run 'python3 update-tools-manifest.py' to update the manifest")

    return moved_files

if __name__ == '__main__':
    # Confirm with user
    print("⚠️  This will move all HTML files from subdirectories to the root directory")
    print("⚠️  Files with the same name will be renamed (e.g., tool.html → tool-1.html)")
    response = input("\nContinue? (y/N): ").strip().lower()

    if response == 'y':
        flatten_html_files()
    else:
        print("Cancelled")