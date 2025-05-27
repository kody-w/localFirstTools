#!/usr/bin/env python3
"""
GitHub Browser Page Updater
Updates local-browser.html to work with GitHub Pages deployment
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
    clean_title = re.sub(r'\s*-\s*Complete$', '', title, flags=re.IGNORECASE)
    clean_title = re.sub(r'\s*Tool$', '', clean_title, flags=re.IGNORECASE)
    clean_title = re.sub(r'\s*App$', '', clean_title, flags=re.IGNORECASE)
    
    return f"A utility for {clean_title.lower()} tasks and operations"

def guess_tags_from_title(title):
    """Guess appropriate tags based on the title"""
    title_lower = title.lower()
    tags = []
    
    tag_mappings = {
        'productivity': ['task', 'todo', 'planner', 'schedule', 'organize', 'track', 'kanban', 'pomodoro'],
        'visualization': ['diagram', 'chart', 'graph', 'view', 'display', 'mermaid', 'visual'],
        'health': ['health', 'medical', 'therapy', 'emdr', 'wellness'],
        'development': ['code', 'dev', 'api', 'debug', 'test', 'terminal', 'workflow'],
        'tools': ['tool', 'utility', 'helper', 'assistant'],
        'data': ['data', 'csv', 'json', 'excel', 'database'],
        'communication': ['chat', 'message', 'email', 'contact'],
        'finance': ['finance', 'money', 'budget', 'expense', 'invoice', 'business'],
        'education': ['learn', 'study', 'quiz', 'flash', 'education', 'teacher'],
        'media': ['image', 'video', 'audio', 'media', 'photo', 'youtube', 'webcam'],
        'security': ['security', 'password', 'encrypt', 'auth'],
        'games': ['game', 'puzzle', 'play', 'console', 'retroplay', 'snake', 'worm', 'fps'],
        'business': ['business', 'crm', 'dashboard', 'copilot', 'migration', 'assessment'],
    }
    
    for tag, keywords in tag_mappings.items():
        if any(keyword in title_lower for keyword in keywords):
            tags.append(tag)
    
    if not tags:
        tags.append('utility')
        
    return tags

def choose_icon_from_title(title):
    """Choose an appropriate emoji icon based on the title"""
    title_lower = title.lower()
    
    icon_mappings = {
        '📋': ['task', 'todo', 'list', 'checklist', 'kanban'],
        '📊': ['chart', 'graph', 'diagram', 'data', 'mermaid', 'dashboard'],
        '👁️': ['eye', 'emdr', 'vision', 'view', 'viewer'],
        '🏥': ['health', 'medical', 'therapy'],
        '💻': ['code', 'dev', 'api', 'program', 'terminal'],
        '🔧': ['tool', 'utility', 'fix'],
        '📈': ['finance', 'money', 'budget', 'expense', 'business'],
        '🎮': ['game', 'play', 'puzzle', 'console', 'retroplay', 'fps'],
        '🔒': ['security', 'password', 'lock'],
        '📚': ['learn', 'study', 'education', 'quiz', 'teacher'],
        '🖼️': ['image', 'photo', 'picture'],
        '🎵': ['audio', 'music', 'sound'],
        '📹': ['video', 'media', 'youtube', 'webcam'],
        '💬': ['chat', 'message', 'talk'],
        '⏰': ['time', 'clock', 'schedule', 'calendar', 'pomodoro'],
        '🔍': ['search', 'find', 'lookup'],
        '📝': ['write', 'note', 'text', 'document'],
        '🤖': ['agent', 'copilot', 'ai', 'automated'],
        '🏢': ['business', 'corporate', 'lumon', 'industries'],
        '🐍': ['snake', 'worm'],
        '🚀': ['migration', 'mac'],
    }
    
    for icon, keywords in icon_mappings.items():
        if any(keyword in title_lower for keyword in keywords):
            return icon
            
    return '📄'

def scan_html_files(directory="."):
    """Scan directory for HTML files and extract metadata"""
    apps = []
    
    exclude_files = {'index.html', 'template.html', 'example.html', 'test.html', 'local-browser.html'}
    
    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename.lower() not in exclude_files:
            filepath = os.path.join(directory, filename)
            
            title = extract_title_from_html(filepath)
            app_id = os.path.splitext(filename)[0]
            
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

def update_local_browser_html(apps, github_username, repo_name):
    """Update the local-browser.html file for GitHub Pages deployment"""
    try:
        with open('local-browser.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create the updated HTML content
        updated_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local First Tools - App Browser</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5rem;
            font-weight: 600;
        }}
        
        .header p {{
            margin: 0.5rem 0 0;
            opacity: 0.9;
            font-size: 1.1rem;
        }}
        
        .content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .stats {{
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .stat-item {{
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }}
        
        .filter-bar {{
            background: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        .search-input {{
            flex: 1;
            min-width: 200px;
            padding: 0.75rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .tag-filters {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .tag-filter {{
            padding: 0.5rem 1rem;
            background: #f0f0f0;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.9rem;
        }}
        
        .tag-filter:hover {{
            background: #e0e0e0;
        }}
        
        .tag-filter.active {{
            background: #667eea;
            color: white;
        }}
        
        .app-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
        }}
        
        .app-card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }}
        
        .app-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}
        
        .app-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transform: scaleX(0);
            transition: transform 0.3s;
        }}
        
        .app-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .app-header {{
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }}
        
        .app-icon {{
            font-size: 2rem;
            margin-right: 0.75rem;
        }}
        
        .app-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin: 0;
            color: #333;
        }}
        
        .app-description {{
            color: #666;
            margin-bottom: 1rem;
            line-height: 1.5;
        }}
        
        .app-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}
        
        .app-tag {{
            background: #f0f0f0;
            color: #555;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.85rem;
        }}
        
        .app-button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            cursor: pointer;
            width: 100%;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s;
        }}
        
        .app-button:hover {{
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        
        .no-results {{
            text-align: center;
            padding: 3rem;
            color: #666;
        }}
        
        @media (max-width: 640px) {{
            .content {{
                padding: 1rem;
            }}
            
            .app-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Local First Tools</h1>
        <p>Browser-based utilities that work offline</p>
    </div>
    
    <div class="content">
        <div class="stats">
            <h2>App Collection</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number" id="total-apps">{len(apps)}</div>
                    <div class="stat-label">Total Apps</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="total-categories">0</div>
                    <div class="stat-label">Categories</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="last-updated">{datetime.now().strftime('%-m/%-d')}</div>
                    <div class="stat-label">Last Updated</div>
                </div>
            </div>
        </div>
        
        <div class="filter-bar">
            <input type="text" class="search-input" id="search-input" placeholder="Search apps...">
            <div class="tag-filters" id="tag-filters">
                <button class="tag-filter active" data-tag="all">All</button>
            </div>
        </div>
        
        <div class="app-grid" id="app-grid">
            <!-- Apps will be populated here -->
        </div>
    </div>

    <script>
        // App data
        const apps = {json.dumps(apps, indent=8)};
        
        // State
        let selectedTag = 'all';
        let searchQuery = '';
        
        // Get unique tags
        const allTags = [...new Set(apps.flatMap(app => app.tags || []))].sort();
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            setupTagFilters();
            setupSearch();
            updateStats();
            renderApps();
        }});
        
        function setupTagFilters() {{
            const tagFilters = document.getElementById('tag-filters');
            
            allTags.forEach(tag => {{
                const button = document.createElement('button');
                button.className = 'tag-filter';
                button.dataset.tag = tag;
                button.textContent = tag.charAt(0).toUpperCase() + tag.slice(1);
                button.addEventListener('click', () => {{
                    document.querySelectorAll('.tag-filter').forEach(btn => {{
                        btn.classList.remove('active');
                    }});
                    button.classList.add('active');
                    selectedTag = tag;
                    renderApps();
                }});
                tagFilters.appendChild(button);
            }});
            
            // All button click handler
            document.querySelector('[data-tag="all"]').addEventListener('click', () => {{
                document.querySelectorAll('.tag-filter').forEach(btn => {{
                    btn.classList.remove('active');
                }});
                document.querySelector('[data-tag="all"]').classList.add('active');
                selectedTag = 'all';
                renderApps();
            }});
        }}
        
        function setupSearch() {{
            const searchInput = document.getElementById('search-input');
            searchInput.addEventListener('input', (e) => {{
                searchQuery = e.target.value.toLowerCase();
                renderApps();
            }});
        }}
        
        function updateStats() {{
            document.getElementById('total-categories').textContent = allTags.length;
        }}
        
        function filterApps() {{
            return apps.filter(app => {{
                const matchesTag = selectedTag === 'all' || (app.tags && app.tags.includes(selectedTag));
                const matchesSearch = !searchQuery || 
                    app.title.toLowerCase().includes(searchQuery) ||
                    app.description.toLowerCase().includes(searchQuery) ||
                    (app.tags && app.tags.some(tag => tag.includes(searchQuery)));
                
                return matchesTag && matchesSearch;
            }});
        }}
        
        function renderApps() {{
            const appGrid = document.getElementById('app-grid');
            const filteredApps = filterApps();
            
            if (filteredApps.length === 0) {{
                appGrid.innerHTML = '<div class="no-results">No apps found matching your criteria</div>';
                return;
            }}
            
            appGrid.innerHTML = filteredApps.map(app => `
                <div class="app-card">
                    <div class="app-header">
                        <div class="app-icon">${{app.icon || '📄'}}</div>
                        <h3 class="app-title">${{app.title}}</h3>
                    </div>
                    <p class="app-description">${{app.description}}</p>
                    <div class="app-tags">
                        ${{(app.tags || []).map(tag => `<span class="app-tag">${{tag}}</span>`).join('')}}
                    </div>
                    <button class="app-button" onclick="window.location.href='${{app.path}}'">
                        Open App
                    </button>
                </div>
            `).join('');
        }}
    </script>
</body>
</html>'''
        
        # Write the updated file
        with open('local-browser.html', 'w', encoding='utf-8') as f:
            f.write(updated_html)
            
        print(f"\nSuccessfully updated local-browser.html with {len(apps)} apps")
        
    except Exception as e:
        print(f"Error updating local-browser.html: {e}")

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
    """Main function to run the GitHub browser updater"""
    print("GitHub Browser Page Updater")
    print("=" * 50)
    
    # Get GitHub username and repository name
    github_username = input("Enter your GitHub username (default: kody-w): ").strip() or "kody-w"
    repo_name = input("Enter your repository name (default: localFirstTools): ").strip() or "localFirstTools"
    
    print(f"\nScanning for HTML files in current directory...")
    print(f"Will configure for: https://{github_username}.github.io/{repo_name}/\n")
    
    # Scan for HTML files
    apps = scan_html_files()
    
    if not apps:
        print("No HTML files found (excluding index.html and local-browser.html)")
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
    response = input("Update local-browser.html with these apps? (y/n): ")
    if response.lower() == 'y':
        update_local_browser_html(apps, github_username, repo_name)
        create_config_file(apps)
        print("\nDone! Your GitHub browser page has been updated.")
        print(f"Once pushed to GitHub, it will be available at:")
        print(f"https://{github_username}.github.io/{repo_name}/local-browser.html")
    else:
        print("Cancelled. No changes made.")

if __name__ == "__main__":
    main()