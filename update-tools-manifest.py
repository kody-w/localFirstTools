#!/usr/bin/env python3
"""
Scans the current directory for HTML files and generates a manifest JSON file
that can be used by the Local First Tools gallery.
Run this script in your tools directory to update the tools list.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def get_html_files(directory='.'):
    """Find all HTML files in the specified directory, excluding index.html"""
    root_dir = Path(directory)
    html_files = []
    
    # Ensure directory exists
    if not root_dir.exists():
        print(f"Directory {directory} does not exist!")
        return []

    for file in root_dir.glob('*.html'):
        # Skip index files and other system files
        if file.name.lower() in ['index.html', 'index_old.html']:
            continue
            
        try:
            # Get file metadata
            stat = file.stat()
            html_files.append({
                'name': file.name,
                'size': stat.st_size,
                'modified': stat.st_mtime
            })
        except Exception as e:
            print(f"Warning: Could not read metadata for {file.name}: {e}")

    # Sort by name
    html_files.sort(key=lambda x: x['name'])
    return html_files

def generate_manifest(directory='.', output_file='tools-manifest.json'):
    """Generate the tools manifest JSON"""
    html_files = get_html_files(directory)
    
    manifest = {
        'version': '1.0',
        'generated': datetime.now().isoformat(),
        'tools': html_files,
        'count': len(html_files)
    }
    
    # Write manifest to JSON file
    output_path = Path(directory) / output_file
    try:
        with open(output_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"✓ Generated {output_file} with {len(html_files)} tools")
        
        # List the tools found
        if html_files:
            print("\nTools found:")
            for file in html_files:
                size_kb = file['size'] / 1024
                print(f"  - {file['name']} ({size_kb:.1f} KB)")
        else:
            print("\nNo HTML tools found in directory (excluding index.html)")
            print("Make sure you're running this script in the directory containing your HTML tools.")
        
        return True
        
    except Exception as e:
        print(f"Error writing manifest file: {e}")
        return False

def main():
    """Main function with argument parsing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate tools manifest for Local First Tools gallery')
    parser.add_argument('-d', '--directory', default='.', 
                        help='Directory to scan for HTML files (default: current directory)')
    parser.add_argument('-o', '--output', default='tools-manifest.json',
                        help='Output manifest filename (default: tools-manifest.json)')
    
    args = parser.parse_args()
    
    success = generate_manifest(args.directory, args.output)
    
    if success:
        print(f"\nNext steps:")
        print("1. Place your HTML tools in the same directory as index.html")
        print("2. Run this script to update the manifest")
        print("3. Commit both the tools and the manifest to your repository")
        print("4. The gallery will automatically load your tools")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())