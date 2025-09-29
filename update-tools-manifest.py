#!/usr/bin/env python3
"""
Scans the root directory for HTML files and generates a manifest JSON file
that can be fetched via GitHub raw content URL without API limitations.
Run this before committing to update the tools list.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def get_html_files():
    """Find all HTML files in the root directory, excluding index.html"""
    root_dir = Path('.')
    html_files = []

    for file in root_dir.glob('*.html'):
        if file.name != 'index.html':
            # Get file metadata
            stat = file.stat()
            html_files.append({
                'name': file.name,
                'size': stat.st_size,
                'modified': stat.st_mtime
            })

    # Sort by name
    html_files.sort(key=lambda x: x['name'])
    return html_files

def generate_manifest():
    """Generate the tools manifest JSON"""
    html_files = get_html_files()

    manifest = {
        'version': '1.0',
        'generated': datetime.now().isoformat(),
        'tools': html_files,
        'count': len(html_files)
    }

    # Write manifest to JSON file
    with open('tools-manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"✓ Generated tools-manifest.json with {len(html_files)} tools")

    # List the tools found
    if html_files:
        print("\nTools found:")
        for file in html_files:
            print(f"  - {file['name']}")
    else:
        print("\nNo HTML tools found in root directory (excluding index.html)")

if __name__ == '__main__':
    generate_manifest()