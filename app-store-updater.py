#!/usr/bin/env python3
"""
App Store Index Updater
Scans the current directory for HTML files and updates index.html with all found apps.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser

class TitleExtractor(HTMLParser):
    """Extract title from HTML file"""
    def __init__(self):
        super().__init__()
        self.title = None
        self.in_title = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
            
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
            
    def handle_data(self, data):
        if self.in_title and self.title is None:
            self.title = data.strip()

def extract_title_from_html(filepath):
    """Extract the <title> tag content from an HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        parser = TitleExtractor()
        parser.feed(content)
        return parser.title or "Untitled App"
    except Exception as e:
        print(f"Error extracting title from {filepath}: {e}")
        return "Untitled App"

def generate_description_from_title(title):
    """Generate a simple description based on the title"""
    # Remove common suffixes
    clean_title = re.sub(r'\s*-\s*Complete$', '', title, flags=re.IGNORECASE)
    clean_title = re.sub(r'\s*Tool$', '', clean_title, flags=re.IGNORECASE)
    clean_title = re.sub(r'\s*App$', '', clean_title, flags=re.IGNORECASE)
    
    return f"A utility for {clean_title.lower()} tasks and operations"

def guess_tags_from_title(title):
    """Guess appropriate tags based on the title"""
    title_lower = title.lower()
    tags = []
    
    # Category mappings
    tag_mappings = {
        'productivity': ['task', 'todo', 'planner', 'schedule', 'organize', 'track'],
        'visualization': ['diagram', 'chart', 'graph', 'view', 'display', 'mermaid'],
        'health': ['health', 'medical', 'therapy', 'emdr', 'wellness'],
        'development': ['code', 'dev', 'api', 'debug', 'test'],
        'tools': ['tool', 'utility', 'helper', 'assistant'],
        'data': ['data', 'csv', 'json', 'excel', 'database'],
        'communication': ['chat', 'message', 'email', 'contact'],
        'finance': ['finance', 'money', 'budget', 'expense', 'invoice'],
        'education': ['learn', 'study', 'quiz', 'flash', 'education'],
        'media': ['image', 'video', 'audio', 'media', 'photo'],
        'security': ['security', 'password', 'encrypt', 'auth'],
        'games': ['game', 'puzzle', 'play'],
    }
    
    for tag, keywords in tag_mappings.items():
        if any(keyword in title_lower for keyword in keywords):
            tags.append(tag)
    
    # If no tags found, add 'utility' as default
    if not tags:
        tags.append('utility')
        
    return tags

def choose_icon_from_title(title):
    """Choose an appropriate emoji icon based on the title"""
    title_lower = title.lower()
    
    # Icon mappings
    icon_mappings = {
        '📋': ['task', 'todo', 'list', 'checklist'],
        '📊': ['chart', 'graph', 'diagram', 'data', 'mermaid'],
        '👁️': ['eye', 'emdr', 'vision', 'view'],
        '🏥': ['health', 'medical', 'therapy'],
        '💻': ['code', 'dev', 'api', 'program'],
        '🔧': ['tool', 'utility', 'fix'],
        '📈': ['finance', 'money', 'budget', 'expense'],
        '🎮': ['game', 'play', 'puzzle'],
        '🔒': ['security', 'password', 'lock'],
        '📚': ['learn', 'study', 'education', 'quiz'],
        '🖼️': ['image', 'photo', 'picture'],
        '🎵': ['audio', 'music', 'sound'],
        '📹': ['video', 'media'],
        '💬': ['chat', 'message', 'talk'],
        '⏰': ['time', 'clock', 'schedule', 'calendar'],
        '🔍': ['search', 'find', 'lookup'],
        '📝': ['write', 'note', 'text', 'document'],
    }
    
    for icon, keywords in icon_mappings.items():
        if any(keyword in title_lower for keyword in keywords):
            return icon
            
    return '📄'  # Default icon

def scan_html_files(directory="."):
    """Scan directory for HTML files and extract metadata"""
    apps = []
    
    # Files to exclude
    exclude_files = {'index.html', 'template.html', 'example.html', 'test.html'}
    
    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename.lower() not in exclude_files:
            filepath = os.path.join(directory, filename)
            
            # Extract title from HTML
            title = extract_title_from_html(filepath)
            
            # Generate ID from filename
            app_id = os.path.splitext(filename)[0]
            
            # Generate or extract other metadata
            description = generate_description_from_title(title)
            tags = guess_tags_from_title(title)
            icon = choose_icon_from_title(title)
            
            app = {
                'id': app_id,
                'title': title,
                'description': description,
                'tags': tags,
                'path': f'./{filename}',
                'icon': icon
            }
            
            apps.append(app)
            print(f"Found app: {title} ({filename})")
    
    return sorted(apps, key=lambda x: x['title'])

def update_index_html(apps):
    """Update the apps array in index.html"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create the new apps array
        apps_json = json.dumps(apps, indent=12)
        # Add proper indentation for the JavaScript context
        apps_json = '\n'.join(['        ' + line if i > 0 else line 
                              for i, line in enumerate(apps_json.split('\n'))])
        
        # Pattern to find the apps array
        pattern = r'(let apps = )\[[\s\S]*?\](\s*;)'
        
        # Replace the apps array
        new_content = re.sub(pattern, rf'\1{apps_json}\2', content)
        
        # Write back to file
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"\nSuccessfully updated index.html with {len(apps)} apps")
        
    except Exception as e:
        print(f"Error updating index.html: {e}")

def create_config_file(apps):
    """Create a configuration JSON file for backup"""
    config = {
        'version': '1.0',
        'lastUpdated': datetime.now().isoformat(),
        'apps': apps
    }
    
    with open('utility_apps_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
        
    print("Created utility_apps_config.json backup file")

def main():
    """Main function to run the app store updater"""
    print("App Store Index Updater")
    print("=" * 50)
    print("Scanning for HTML files in current directory...\n")
    
    # Scan for HTML files
    apps = scan_html_files()
    
    if not apps:
        print("No HTML files found (excluding index.html)")
        return
    
    print(f"\nFound {len(apps)} apps total")
    print("\nApp List:")
    print("-" * 50)
    for app in apps:
        print(f"{app['icon']} {app['title']}")
        print(f"   File: {app['path']}")
        print(f"   Tags: {', '.join(app['tags'])}")
        print()
    
    # Ask for confirmation
    response = input("Update index.html with these apps? (y/n): ")
    if response.lower() == 'y':
        update_index_html(apps)
        create_config_file(apps)
        print("\nDone! Your app store has been updated.")
    else:
        print("Cancelled. No changes made.")

if __name__ == "__main__":
    main()
