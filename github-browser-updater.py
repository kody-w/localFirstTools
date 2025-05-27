#!/usr/bin/env python3
"""
Update Local First Tools App List
This script scans the current directory for HTML files and updates the apps list
in the Local First Tools browser HTML file.
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
        self.in_h1 = False
        self.h1_content = None
        
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'h1' and not self.h1_content:
            self.in_h1 = True
            
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'h1':
            self.in_h1 = False
            
    def handle_data(self, data):
        if self.in_title and not self.title:
            self.title = data.strip()
        elif self.in_h1 and not self.h1_content:
            self.h1_content = data.strip()

def get_html_title(filepath):
    """Extract title from HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        parser = TitleExtractor()
        parser.feed(content)
        
        # Return title tag content, or h1 content, or filename
        if parser.title:
            return parser.title
        elif parser.h1_content:
            return parser.h1_content
        else:
            return Path(filepath).stem.replace('-', ' ').replace('_', ' ').title()
            
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return Path(filepath).stem.replace('-', ' ').replace('_', ' ').title()

def categorize_app(filename, title):
    """Determine app category based on filename and title"""
    filename_lower = filename.lower()
    title_lower = title.lower()
    
    tags = []
    
    # Category mappings
    category_keywords = {
        'games': ['game', 'play', 'arcade', 'puzzle', 'fps', 'retroplay', 'snake', 'worm'],
        'productivity': ['task', 'todo', 'kanban', 'pomodoro', 'tracker', 'flow'],
        'visualization': ['viewer', 'visualiz', 'chart', 'graph', 'diagram', 'mermaid', 'dashboard'],
        'development': ['terminal', 'code', 'debug', 'workflow', 'agent', 'developer'],
        'business': ['crm', 'copilot', 'business', 'dashboard', 'migration', 'assessment', 'mac'],
        'finance': ['finance', 'financial', 'money', 'budget', 'investment'],
        'media': ['video', 'youtube', 'webcam', 'sync', 'media', 'audio'],
        'health': ['health', 'medical', 'therapy', 'emdr', 'wellness'],
        'education': ['teach', 'learn', 'education', 'study', 'tutorial'],
        'tools': ['tool', 'utility', 'converter', 'calculator'],
        'utility': ['utility', 'helper', 'assistant', 'refiner']
    }
    
    # Check for category keywords
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in filename_lower or keyword in title_lower:
                if category not in tags:
                    tags.append(category)
                    
    # If no category found, add 'utility' as default
    if not tags:
        tags.append('utility')
        
    return tags

def get_icon_for_app(filename, title, tags):
    """Determine appropriate icon based on app type"""
    filename_lower = filename.lower()
    title_lower = title.lower()
    
    # Icon mappings
    icon_map = {
        'game': '🎮',
        'task': '📋',
        'todo': '📋',
        'kanban': '📋',
        'visual': '📊',
        'chart': '📊',
        'graph': '📊',
        'dashboard': '📊',
        'terminal': '💻',
        'code': '💻',
        'workflow': '🤖',
        'agent': '🤖',
        'copilot': '🤖',
        'video': '📹',
        'youtube': '📹',
        'webcam': '📹',
        'health': '💊',
        'therapy': '👁️',
        'emdr': '👁️',
        'teach': '🎓',
        'learn': '🎓',
        'crm': '👁️',
        'viewer': '👁️',
        'mermaid': '📊'
    }
    
    # Check for icon keywords
    for keyword, icon in icon_map.items():
        if keyword in filename_lower or keyword in title_lower:
            return icon
            
    # Default icons based on tags
    tag_icons = {
        'games': '🎮',
        'productivity': '📋',
        'visualization': '📊',
        'development': '💻',
        'business': '💼',
        'finance': '💰',
        'media': '📹',
        'health': '💊',
        'education': '🎓',
        'tools': '🔧',
        'utility': '📄'
    }
    
    if tags:
        return tag_icons.get(tags[0], '📄')
        
    return '📄'

def generate_description(title, filename):
    """Generate a description based on title"""
    # Clean up the title for description
    clean_title = title.lower().replace('(', '').replace(')', '').replace('-', ' ')
    return f"A utility for {clean_title} tasks and operations"

def scan_html_files(directory='.', github_repo_url=None):
    """Scan directory for HTML files and generate app list"""
    apps = []
    excluded_files = ['index.html', 'app-browser.html', 'local-first-tools.html']
    
    # Get all HTML files
    html_files = [f for f in os.listdir(directory) 
                  if f.endswith('.html') and f not in excluded_files]
    
    print(f"Found {len(html_files)} HTML files")
    
    for filename in sorted(html_files):
        filepath = os.path.join(directory, filename)
        
        # Get title from HTML
        title = get_html_title(filepath)
        
        # Generate ID from filename
        app_id = Path(filename).stem
        
        # Categorize the app
        tags = categorize_app(filename, title)
        
        # Get appropriate icon
        icon = get_icon_for_app(filename, title, tags)
        
        # Generate description
        description = generate_description(title, filename)
        
        # Create app entry
        app_entry = {
            "id": app_id,
            "title": title,
            "description": description,
            "tags": tags,
            "path": f"./{filename}",
            "icon": icon
        }
        
        # Add GitHub URL if provided
        if github_repo_url:
            # Ensure URL ends with /
            if not github_repo_url.endswith('/'):
                github_repo_url += '/'
            app_entry["url"] = f"{github_repo_url}{filename}"
        
        apps.append(app_entry)
        print(f"Added: {title} ({filename}) - Tags: {', '.join(tags)}")
    
    return apps

def update_html_file(html_file, apps):
    """Update the apps array in the HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the apps array in the JavaScript
        pattern = r'const apps = \[[\s\S]*?\];'
        
        # Generate new apps array
        apps_json = json.dumps(apps, indent=8, ensure_ascii=False)
        # Format for JavaScript
        apps_js = f"const apps = {apps_json};"
        
        # Replace the old array with the new one
        new_content = re.sub(pattern, apps_js, content)
        
        # Update the total apps count
        total_apps = len(apps)
        new_content = re.sub(
            r'<div class="stat-number" id="total-apps">\d+</div>',
            f'<div class="stat-number" id="total-apps">{total_apps}</div>',
            new_content
        )
        
        # Update last updated date
        today = datetime.now().strftime("%-m/%-d")
        new_content = re.sub(
            r'<div class="stat-number" id="last-updated">[\d/]+</div>',
            f'<div class="stat-number" id="last-updated">{today}</div>',
            new_content
        )
        
        # Write back to file
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"\nSuccessfully updated {html_file}")
        print(f"Total apps: {total_apps}")
        print(f"Last updated: {today}")
        
    except Exception as e:
        print(f"Error updating HTML file: {e}")

def main():
    """Main function"""
    print("Local First Tools - App List Updater")
    print("=" * 40)
    
    # Configuration
    directory = '.'  # Current directory
    html_file = 'index.html'  # Or whatever you name your main file
    
    # GitHub raw URL base (update this with your repo)
    github_username = "kody-w"
    github_repo = "localFirstTools"
    github_branch = "main"
    github_repo_url = f"https://raw.githubusercontent.com/{github_username}/{github_repo}/refs/heads/{github_branch}"
    
    # Check if HTML file exists
    if not os.path.exists(html_file):
        print(f"Creating new {html_file} from template...")
        # You could copy a template file here if needed
        print(f"Error: {html_file} not found. Please ensure the Local First Tools HTML file exists.")
        return
    
    # Scan for HTML files
    print(f"\nScanning directory: {os.path.abspath(directory)}")
    apps = scan_html_files(directory, github_repo_url)
    
    if not apps:
        print("No HTML files found!")
        return
    
    # Update the HTML file
    print(f"\nUpdating {html_file}...")
    update_html_file(html_file, apps)
    
    print("\nDone! Your app list has been updated.")
    print("\nTo publish to GitHub:")
    print("1. git add .")
    print("2. git commit -m 'Update app list'")
    print("3. git push")

if __name__ == "__main__":
    main()