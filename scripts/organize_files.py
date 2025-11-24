#!/usr/bin/env python3
"""
File Organization Script for localFirstTools2
Moves all files from root directory to appropriate category directories
"""

import os
import shutil
import json
from pathlib import Path

def get_file_category(filename, file_path=None):
    """Determine which category a file belongs to based on its name and content"""
    
    filename_lower = filename.lower()
    
    # Files that should stay in root
    if filename in ['index.html', 'CLAUDE.md', 'README.md']:
        return 'root'
    
    # Scripts and configuration files
    if filename.endswith('.sh'):
        return 'scripts'
    if filename.endswith('.py'):
        return 'scripts'
    if filename.endswith('.json'):
        return 'data/config'
    
    # Archive old index variants
    if 'index' in filename_lower and filename.endswith('.html'):
        return 'apps/index-variants'
    
    # HTML files - categorize by keywords
    if filename.endswith('.html'):
        # Games
        game_keywords = ['game', 'snake', 'racing', 'poker', 'balatro', 'gameboy', 
                        'emulator', 'play', 'solitaire', 'life', 'fpspic', 'gameoflife']
        for keyword in game_keywords:
            if keyword in filename_lower:
                return 'apps/games'
        
        # AI Tools
        ai_keywords = ['ai', 'agent', 'claude', 'copilot', 'workshop', 'wrist']
        for keyword in ai_keywords:
            if keyword in filename_lower:
                return 'apps/ai-tools'
        
        # Business
        business_keywords = ['crm', 'dashboard', 'presentation', 'sales', 'd365', 
                           'dynamics', 'executive', 'influence']
        for keyword in business_keywords:
            if keyword in filename_lower:
                return 'apps/business'
        
        # Development
        dev_keywords = ['browser', 'github', 'terminal', 'artifact', 'cdn', 
                       'texture', 'generator']
        for keyword in dev_keywords:
            if keyword in filename_lower:
                return 'apps/development'
        
        # Media
        media_keywords = ['camera', 'recorder', 'drum', 'youtube', 'dual', 
                         'hologram', '808', 'music']
        for keyword in media_keywords:
            if keyword in filename_lower:
                return 'apps/media'
        
        # Productivity
        productivity_keywords = ['notes', 'journal', 'writer', 'ghost', 'book', 
                                'factory', 'task', 'tracker', 'workflow', 'memory',
                                'prompt', 'library', 'record', 'review', 'sneaker']
        for keyword in productivity_keywords:
            if keyword in filename_lower:
                return 'apps/productivity'
        
        # Education
        education_keywords = ['tutorial', 'trainer', 'teacher', 'learner']
        for keyword in education_keywords:
            if keyword in filename_lower:
                return 'apps/education'
        
        # Utilities
        utility_keywords = ['converter', 'splitter', 'crawler', 'flattener', 
                          'timezone', 'tool', 'manager']
        for keyword in utility_keywords:
            if keyword in filename_lower:
                return 'apps/utilities'
        
        # 3D/Graphics
        graphics_keywords = ['3d', 'tile', 'room', 'world', 'drone', 'simulator']
        for keyword in graphics_keywords:
            if keyword in filename_lower:
                return 'apps/games'  # Most 3D content seems to be games
        
        # Communication
        comm_keywords = ['chat', 'gesture', 'message', 'snap']
        for keyword in comm_keywords:
            if keyword in filename_lower:
                return 'apps/productivity'
        
        # Default for uncategorized HTML
        return 'apps/utilities'
    
    # HTM files
    if filename.endswith('.htm'):
        return 'archive'
    
    # Default
    return 'archive'

def create_directories():
    """Create necessary directory structure"""
    directories = [
        'apps/games',
        'apps/productivity',
        'apps/business',
        'apps/development',
        'apps/media',
        'apps/education',
        'apps/ai-tools',
        'apps/health',
        'apps/utilities',
        'apps/index-variants',
        'data/config',
        'data/games',
        'archive',
        'scripts'
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Ensured directory exists: {dir_path}")

def organize_files(dry_run=True):
    """Main function to organize files"""
    
    # Get current directory
    root_dir = Path.cwd()
    
    # Create directories first
    print("\n=== Creating Directory Structure ===")
    create_directories()
    
    # Get all files in root directory (not directories)
    files_to_move = []
    for item in root_dir.iterdir():
        if item.is_file():
            category = get_file_category(item.name)
            if category != 'root':
                files_to_move.append((item, category))
    
    if dry_run:
        print("\n=== DRY RUN MODE - No files will be moved ===")
    else:
        print("\n=== MOVING FILES ===")
    
    # Group files by category for better output
    moves_by_category = {}
    for file_path, category in files_to_move:
        if category not in moves_by_category:
            moves_by_category[category] = []
        moves_by_category[category].append(file_path)
    
    # Display and/or move files
    for category, files in sorted(moves_by_category.items()):
        print(f"\n📁 {category}:")
        for file_path in files:
            dest_path = root_dir / category / file_path.name
            if dry_run:
                print(f"  • {file_path.name} → {category}/{file_path.name}")
            else:
                try:
                    shutil.move(str(file_path), str(dest_path))
                    print(f"  ✓ Moved: {file_path.name}")
                except Exception as e:
                    print(f"  ✗ Failed to move {file_path.name}: {e}")
    
    # Summary
    total_files = sum(len(files) for files in moves_by_category.values())
    print(f"\n=== SUMMARY ===")
    print(f"Total files to organize: {total_files}")
    print(f"Categories: {len(moves_by_category)}")
    
    if dry_run:
        print("\n⚠️  This was a dry run. No files were moved.")
        print("Run with --execute flag to actually move files.")
    else:
        print("\n✅ File organization complete!")
    
    # List files that will remain in root
    remaining_files = []
    for item in root_dir.iterdir():
        if item.is_file() and get_file_category(item.name) == 'root':
            remaining_files.append(item.name)
    
    if remaining_files:
        print(f"\n📌 Files remaining in root directory:")
        for filename in remaining_files:
            print(f"  • {filename}")

def main():
    import sys
    
    print("=" * 50)
    print("localFirstTools2 File Organizer")
    print("=" * 50)
    
    # Check for execute flag
    execute = '--execute' in sys.argv or '-e' in sys.argv
    
    if not execute:
        print("\n🔍 Running in DRY RUN mode...")
        print("No files will be moved. Review the proposed changes below.")
        organize_files(dry_run=True)
        print("\n💡 To execute these changes, run:")
        print("   python organize_files.py --execute")
    else:
        response = input("\n⚠️  This will move files to new directories. Continue? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            organize_files(dry_run=False)
        else:
            print("Operation cancelled.")

if __name__ == "__main__":
    main()