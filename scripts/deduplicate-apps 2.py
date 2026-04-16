#!/usr/bin/env python3
"""
Deduplicate Apps Script
Finds duplicate HTML apps and identifies the best version of each.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
import shutil

# Base directory
BASE_DIR = Path(__file__).parent.parent
V2_APPS_DIR = BASE_DIR / "v2" / "apps"

def normalize_name(filename):
    """
    Normalize a filename to its base name by removing:
    - Number suffixes like " 2", " 3", etc.
    - "copy" suffixes like " copy", " copy 2", etc.
    - Leading/trailing whitespace
    """
    name = filename.replace('.html', '')

    # Remove " copy N" or " copy" suffixes
    name = re.sub(r'\s+copy(\s+\d+)?$', '', name, flags=re.IGNORECASE)

    # Remove " N" suffixes (space followed by number at end)
    name = re.sub(r'\s+\d+$', '', name)

    return name.strip()

def get_file_info(filepath):
    """Get file size and modification time."""
    stat = os.stat(filepath)
    return {
        'path': str(filepath),
        'size': stat.st_size,
        'mtime': stat.st_mtime,
        'name': filepath.name
    }

def find_all_html_files(directory):
    """Recursively find all HTML files in directory."""
    html_files = []

    # Root level files
    for f in Path(directory).glob("*.html"):
        if f.is_file() and f.name != 'index.html':
            html_files.append(get_file_info(f))

    # Exhibition_Halls files
    exhibition_dir = directory / "Exhibition_Halls"
    if exhibition_dir.exists():
        for f in exhibition_dir.rglob("*.html"):
            if f.is_file():
                html_files.append(get_file_info(f))

    return html_files

def group_by_base_name(files):
    """Group files by their normalized base name."""
    groups = defaultdict(list)

    for f in files:
        base_name = normalize_name(f['name'])
        groups[base_name].append(f)

    return groups

def select_best_version(versions):
    """
    Select the best version from a list of file versions.
    Priority:
    1. Largest file size (most content)
    2. Most recent modification time
    """
    if len(versions) == 1:
        return versions[0]

    # Sort by size (descending), then by mtime (descending)
    sorted_versions = sorted(versions, key=lambda x: (x['size'], x['mtime']), reverse=True)
    return sorted_versions[0]

def is_stub_file(filepath, size_threshold=1500):
    """
    Check if a file is a stub (placeholder with minimal content).
    Stub files are typically very small and just redirect or have no real content.
    """
    if filepath['size'] < size_threshold:
        return True
    return False

def analyze_duplicates(groups):
    """Analyze groups and identify duplicates."""
    results = {
        'unique_apps': [],
        'duplicates': [],
        'stubs': [],
        'stats': {
            'total_files': 0,
            'unique_apps': 0,
            'duplicate_files': 0,
            'stub_files': 0
        }
    }

    for base_name, versions in groups.items():
        results['stats']['total_files'] += len(versions)

        # Filter out stubs
        real_versions = [v for v in versions if not is_stub_file(v)]
        stub_versions = [v for v in versions if is_stub_file(v)]

        results['stats']['stub_files'] += len(stub_versions)
        results['stubs'].extend([{'base_name': base_name, **s} for s in stub_versions])

        if not real_versions:
            # All versions are stubs, skip this app
            continue

        best = select_best_version(real_versions)
        results['unique_apps'].append({
            'base_name': base_name,
            'selected': best,
            'version_count': len(versions),
            'real_version_count': len(real_versions)
        })
        results['stats']['unique_apps'] += 1

        # Track duplicates
        for v in real_versions:
            if v['path'] != best['path']:
                results['duplicates'].append({
                    'base_name': base_name,
                    'file': v,
                    'replaced_by': best['path']
                })
                results['stats']['duplicate_files'] += 1

    return results

def categorize_app(base_name, filepath):
    """Determine category for an app based on name and path."""
    filepath_str = str(filepath).lower()
    name_lower = base_name.lower()

    # Check path-based categories first
    if 'the_arcade' in filepath_str or 'arcade' in filepath_str:
        return 'games'
    elif 'visual_arts' in filepath_str:
        return 'visual_art'
    elif 'sound_studio' in filepath_str:
        return 'audio_music'
    elif 'simulation_lab' in filepath_str:
        return 'simulations'
    elif 'ai_research' in filepath_str:
        return 'experimental_ai'
    elif 'productivity' in filepath_str:
        return 'creative_tools'
    elif 'educational' in filepath_str:
        return 'educational'

    # Name-based categorization
    game_keywords = ['game', 'quest', 'adventure', 'rpg', 'arcade', 'battle', 'shooter',
                     'puzzle', 'chess', 'cards', 'poker', 'race', 'fighter', 'war']
    audio_keywords = ['music', 'audio', 'sound', 'synth', 'beat', 'drum', 'melody',
                      'composer', 'orchestra', 'symphony', 'daw']
    visual_keywords = ['art', 'draw', 'paint', 'canvas', 'visual', 'color', 'pixel',
                       'fractal', 'generative', 'particle']
    ai_keywords = ['ai', 'neural', 'brain', 'agent', 'consciousness', 'llm', 'gpt']
    simulation_keywords = ['simulation', 'simulator', 'evolution', 'ecosystem', 'colony',
                           'civilization', 'universe', 'world', 'physics', 'cellular']
    tool_keywords = ['tool', 'editor', 'converter', 'generator', 'tracker', 'manager',
                     'calculator', 'timer', 'planner', 'tester']

    for kw in game_keywords:
        if kw in name_lower:
            return 'games'
    for kw in audio_keywords:
        if kw in name_lower:
            return 'audio_music'
    for kw in visual_keywords:
        if kw in name_lower:
            return 'visual_art'
    for kw in ai_keywords:
        if kw in name_lower:
            return 'experimental_ai'
    for kw in simulation_keywords:
        if kw in name_lower:
            return 'simulations'
    for kw in tool_keywords:
        if kw in name_lower:
            return 'creative_tools'

    return 'uncategorized'

def copy_apps_to_v2(results, v2_apps_dir, dry_run=True):
    """Copy deduplicated apps to v2 directory."""
    copied = []

    # Create category directories
    categories = set()
    for app in results['unique_apps']:
        cat = categorize_app(app['base_name'], app['selected']['path'])
        categories.add(cat)

    if not dry_run:
        v2_apps_dir.mkdir(parents=True, exist_ok=True)
        for cat in categories:
            (v2_apps_dir / cat).mkdir(exist_ok=True)

    for app in results['unique_apps']:
        source = Path(app['selected']['path'])
        category = categorize_app(app['base_name'], source)

        # Clean filename (use base_name + .html)
        clean_name = app['base_name'].replace(' ', '-').lower()
        clean_name = re.sub(r'[^\w\-]', '', clean_name)
        dest_name = f"{clean_name}.html"
        dest = v2_apps_dir / category / dest_name

        copied.append({
            'source': str(source),
            'dest': str(dest),
            'base_name': app['base_name'],
            'category': category,
            'size': app['selected']['size']
        })

        if not dry_run:
            shutil.copy2(source, dest)

    return copied

def main():
    print("=" * 60)
    print("LocalFirstTools Deduplication Analysis")
    print("=" * 60)

    # Find all HTML files
    print("\nScanning for HTML files...")
    all_files = find_all_html_files(BASE_DIR)
    print(f"Found {len(all_files)} HTML files")

    # Group by base name
    print("\nGrouping by base name...")
    groups = group_by_base_name(all_files)
    print(f"Found {len(groups)} unique base names")

    # Analyze duplicates
    print("\nAnalyzing duplicates...")
    results = analyze_duplicates(groups)

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files scanned: {results['stats']['total_files']}")
    print(f"Unique apps: {results['stats']['unique_apps']}")
    print(f"Duplicate files: {results['stats']['duplicate_files']}")
    print(f"Stub/placeholder files: {results['stats']['stub_files']}")

    # Show apps with most duplicates
    print("\n" + "-" * 40)
    print("Apps with most duplicates:")
    print("-" * 40)
    apps_by_dupe_count = sorted(results['unique_apps'],
                                 key=lambda x: x['version_count'],
                                 reverse=True)[:20]
    for app in apps_by_dupe_count:
        if app['version_count'] > 1:
            print(f"  {app['base_name']}: {app['version_count']} versions")

    # Dry run copy
    print("\n" + "=" * 60)
    print("DRY RUN: Apps to copy to v2")
    print("=" * 60)
    copied = copy_apps_to_v2(results, V2_APPS_DIR, dry_run=True)

    # Group by category for display
    by_category = defaultdict(list)
    for c in copied:
        by_category[c['category']].append(c)

    for cat, apps in sorted(by_category.items()):
        print(f"\n{cat}/ ({len(apps)} apps)")
        for app in apps[:5]:  # Show first 5 per category
            print(f"  - {app['base_name']}")
        if len(apps) > 5:
            print(f"  ... and {len(apps) - 5} more")

    # Save results to JSON
    output_file = BASE_DIR / "v2" / "deduplication-report.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump({
            'stats': results['stats'],
            'unique_apps': [
                {
                    'base_name': a['base_name'],
                    'selected_path': a['selected']['path'],
                    'size': a['selected']['size'],
                    'version_count': a['version_count']
                }
                for a in results['unique_apps']
            ],
            'apps_to_copy': copied
        }, f, indent=2)

    print(f"\n\nReport saved to: {output_file}")
    print("\nTo perform actual copy, run with --execute flag")

    return results, copied

if __name__ == "__main__":
    import sys

    execute = '--execute' in sys.argv

    if execute:
        print("=" * 60)
        print("LocalFirstTools Deduplication - EXECUTE MODE")
        print("=" * 60)

        # Find all HTML files
        print("\nScanning for HTML files...")
        all_files = find_all_html_files(BASE_DIR)
        print(f"Found {len(all_files)} HTML files")

        # Group by base name
        print("\nGrouping by base name...")
        groups = group_by_base_name(all_files)
        print(f"Found {len(groups)} unique base names")

        # Analyze duplicates
        print("\nAnalyzing duplicates...")
        results = analyze_duplicates(groups)

        print(f"\nUnique apps to copy: {results['stats']['unique_apps']}")

        # Execute copy
        print("\n" + "=" * 60)
        print("COPYING APPS TO V2")
        print("=" * 60)
        copied = copy_apps_to_v2(results, V2_APPS_DIR, dry_run=False)

        # Show results
        by_category = defaultdict(list)
        for c in copied:
            by_category[c['category']].append(c)

        for cat, apps in sorted(by_category.items()):
            print(f"\n{cat}/: {len(apps)} apps copied")

        print(f"\n\nTotal: {len(copied)} apps copied to v2/apps/")

        # Save manifest
        manifest_file = V2_APPS_DIR / "apps-manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump({
                'generated': str(Path(__file__).name),
                'timestamp': os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip(),
                'total_apps': len(copied),
                'categories': {cat: len(apps) for cat, apps in by_category.items()},
                'apps': copied
            }, f, indent=2)
        print(f"Manifest saved to: {manifest_file}")
    else:
        results, copied = main()
