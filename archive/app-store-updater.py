#!/usr/bin/env python3
"""
Vibe Coding Gallery Index Updater
Scans the current directory for HTML files and updates the gallery configuration.
Creates a vibe_gallery_config.json file compatible with the Vibe Coding Gallery.
Excludes files in the archive directory.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser
import random

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
        return parser.title or "Untitled Creation"
    except Exception as e:
        print(f"Error extracting title from {filepath}: {e}")
        return "Untitled Creation"

def generate_artistic_description(title):
    """Generate an artistic description based on the title"""
    templates = [
        "An experimental dive into the creative possibilities of {}",
        "Interactive art piece exploring {} through code and creativity",
        "A digital meditation on {} in the modern age",
        "Pushing browser limits to create unexpected {} experiences",
        "Real-time generative {} that evolves with each interaction",
        "Creative coding experiment blending {} with imagination",
        "A playful exploration of {} where code becomes art",
        "Digital canvas for {} where logic meets creativity",
        "Vibe coding exploration of {} at its finest",
        "An immersive journey through {} in the digital realm",
        "Experimental web art redefining how we experience {}",
        "Interactive {} piece that responds to your digital presence"
    ]
    
    # Clean and format the title for use in description
    clean_title = re.sub(r'\s*-\s*Complete$', '', title, flags=re.IGNORECASE)
    clean_title = re.sub(r'(Tool|App|Utility)$', '', clean_title, flags=re.IGNORECASE).strip()
    
    # Make it lowercase and more descriptive
    if clean_title:
        focus = clean_title.lower()
    else:
        focus = "digital expression"
    
    return random.choice(templates).format(focus)

def generate_artist_name():
    """Generate creative artist/creator names"""
    prefixes = [
        "Digital", "Cyber", "Neon", "Pixel", "Binary", "Quantum", 
        "Virtual", "Electric", "Holographic", "Algorithmic", "Fractal",
        "Synthetic", "Neural", "Cosmic", "Glitch", "Ethereal"
    ]
    
    suffixes = [
        "Dreams", "Visions", "Aesthetics", "Lab", "Studio", "Collective",
        "Workshop", "Experiments", "Explorations", "Creations", "Arts",
        "Design", "Canvas", "Playground", "Gallery", "Space"
    ]
    
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

def guess_creative_tags(title):
    """Generate creative/artistic tags based on the title"""
    title_lower = title.lower()
    tags = []
    
    # Creative tag mappings
    tag_mappings = {
        'interactive': ['task', 'todo', 'planner', 'schedule', 'organize', 'track', 'game', 'play'],
        'generative': ['chart', 'graph', 'diagram', 'view', 'display', 'data', 'random'],
        'experimental': ['tool', 'utility', 'helper', 'test', 'debug', 'api'],
        'visual': ['image', 'photo', 'picture', 'view', 'display', 'diagram', 'chart'],
        'kinetic': ['animation', 'motion', 'move', 'dynamic', 'flow'],
        'audio-reactive': ['audio', 'music', 'sound', 'voice', 'media'],
        'particles': ['particle', 'physics', 'simulation', 'flow'],
        'geometric': ['shape', 'geometry', 'math', 'calculate', 'formula'],
        'organic': ['health', 'wellness', 'natural', 'life', 'bio'],
        'abstract': ['creative', 'art', 'design', 'color', 'style'],
        'immersive': ['3d', 'vr', 'space', 'world', 'environment'],
        'minimal': ['simple', 'clean', 'basic', 'pure', 'zen'],
        'cyberpunk': ['cyber', 'tech', 'digital', 'code', 'hack'],
        'glitch': ['error', 'bug', 'corrupt', 'distort'],
        'retro': ['old', 'vintage', 'classic', 'nostalgia', '80s', '90s']
    }
    
    # Check for matches
    for tag, keywords in tag_mappings.items():
        if any(keyword in title_lower for keyword in keywords):
            tags.append(tag)
    
    # Ensure we have at least 2 tags
    if len(tags) < 2:
        # Add some random creative tags
        all_tags = list(tag_mappings.keys())
        while len(tags) < 2:
            random_tag = random.choice(all_tags)
            if random_tag not in tags:
                tags.append(random_tag)
    
    # Limit to 4 tags max
    return tags[:4]

def choose_vibe_icon(title):
    """Choose an artistic emoji icon based on the title"""
    title_lower = title.lower()
    
    # Vibe icon mappings
    icon_mappings = {
        '✨': ['magic', 'sparkle', 'special', 'star'],
        '🎨': ['art', 'paint', 'color', 'draw', 'design'],
        '🌟': ['star', 'bright', 'shine', 'glow'],
        '💫': ['dizzy', 'spin', 'whirl', 'motion'],
        '🔮': ['crystal', 'magic', 'future', 'predict', 'mystery'],
        '🎭': ['theater', 'drama', 'mask', 'play', 'game'],
        '🌈': ['rainbow', 'color', 'spectrum', 'pride'],
        '🎪': ['circus', 'fun', 'entertainment', 'show'],
        '🎯': ['target', 'goal', 'aim', 'focus', 'task'],
        '🎲': ['dice', 'random', 'chance', 'game', 'play'],
        '🎸': ['guitar', 'music', 'rock', 'audio', 'sound'],
        '🎹': ['piano', 'keyboard', 'music', 'keys'],
        '🌊': ['wave', 'flow', 'water', 'fluid', 'motion'],
        '🔥': ['fire', 'hot', 'burn', 'energy', 'power'],
        '⚡': ['lightning', 'electric', 'fast', 'speed', 'energy'],
        '🌙': ['moon', 'night', 'dark', 'dream', 'sleep'],
        '🌸': ['flower', 'bloom', 'nature', 'organic', 'life'],
        '🦋': ['butterfly', 'transform', 'change', 'flutter'],
        '🌀': ['cyclone', 'spiral', 'spin', 'vortex', 'twist'],
        '💎': ['gem', 'diamond', 'crystal', 'precious', 'value'],
        '🎆': ['firework', 'explode', 'burst', 'celebrate'],
        '🌃': ['night', 'city', 'urban', 'neon', 'cyber'],
        '🏔️': ['mountain', 'peak', 'high', 'climb', 'challenge'],
        '🌺': ['hibiscus', 'tropical', 'exotic', 'flower'],
        '🦄': ['unicorn', 'magic', 'fantasy', 'unique', 'special']
    }
    
    # Check for keyword matches
    matched_icons = []
    for icon, keywords in icon_mappings.items():
        if any(keyword in title_lower for keyword in keywords):
            matched_icons.append(icon)
    
    if matched_icons:
        return random.choice(matched_icons)
    
    # If no match, return a random vibe icon
    vibe_icons = ['✨', '🎨', '🌟', '💫', '🔮', '🎭', '🌈', '🎪', '🎯', '🎲', 
                  '🎸', '🎹', '🌊', '🔥', '⚡', '🌙', '🌸', '🦋', '🌀', '💎']
    return random.choice(vibe_icons)

def is_in_archive(filepath):
    """Check if a file is in the archive directory"""
    # Convert to Path object for easier manipulation
    path = Path(filepath)
    
    # Check if 'archive' is in any part of the path
    return 'archive' in path.parts

def scan_html_files(directory="."):
    """Scan directory for HTML files and extract metadata"""
    artworks = []
    
    # Files to exclude
    exclude_files = {'index.html', 'template.html', 'example.html', 'test.html', 'gallery.html'}
    
    # Directories to exclude
    exclude_dirs = {'archive', '.git', 'node_modules', 'dist', 'build'}
    
    for root, dirs, files in os.walk(directory):
        # Remove excluded directories from dirs to prevent os.walk from descending into them
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # Check if current directory is archive or within archive
        if is_in_archive(root):
            continue
            
        for filename in files:
            if filename.endswith('.html') and filename.lower() not in exclude_files:
                filepath = os.path.join(root, filename)
                
                # Double-check the file isn't in archive
                if is_in_archive(filepath):
                    continue
                
                # Extract title from HTML
                title = extract_title_from_html(filepath)
                
                # Generate ID from filename
                artwork_id = os.path.splitext(filename)[0]
                
                # Generate artistic metadata
                description = generate_artistic_description(title)
                tags = guess_creative_tags(title)
                icon = choose_vibe_icon(title)
                artist = generate_artist_name()
                
                # Get relative path from current directory
                rel_path = os.path.relpath(filepath, directory)
                # Ensure path uses forward slashes for web compatibility
                rel_path = rel_path.replace(os.sep, '/')
                
                artwork = {
                    'id': artwork_id,
                    'title': title,
                    'artist': artist,
                    'description': description,
                    'tags': tags,
                    'path': f'./{rel_path}',
                    'icon': icon
                }
                
                artworks.append(artwork)
                print(f"Found artwork: {icon} {title} by {artist}")
    
    return sorted(artworks, key=lambda x: x['title'])

def create_gallery_config(artworks):
    """Create a configuration JSON file for the Vibe Coding Gallery"""
    config = {
        'version': '1.0',
        'exhibition': 'Vibe Coding Showcase',
        'lastUpdated': datetime.now().isoformat(),
        'artworks': artworks
    }
    
    with open('vibe_gallery_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        
    print("\nCreated vibe_gallery_config.json")

def display_summary(artworks):
    """Display a summary of the found artworks"""
    print(f"\nFound {len(artworks)} artworks total")
    print("\n" + "="*60)
    print("VIBE CODING GALLERY COLLECTION")
    print("="*60 + "\n")
    
    for i, artwork in enumerate(artworks, 1):
        print(f"{i}. {artwork['icon']} {artwork['title']}")
        print(f"   Artist: {artwork['artist']}")
        print(f"   File: {artwork['path']}")
        print(f"   Tags: {', '.join(artwork['tags'])}")
        print(f"   Description: {artwork['description'][:60]}...")
        print()

def main():
    """Main function to run the gallery updater"""
    print("🎨 Vibe Coding Gallery Index Updater 🎨")
    print("=" * 60)
    print("Scanning for HTML artworks in current directory...")
    print("(Excluding archive directory)\n")
    
    # Scan for HTML files
    artworks = scan_html_files()
    
    if not artworks:
        print("No HTML files found (excluding gallery files and archive)")
        return
    
    display_summary(artworks)
    
    # Ask for confirmation
    response = input("\nCreate/update vibe_gallery_config.json with these artworks? (y/n): ")
    if response.lower() == 'y':
        create_gallery_config(artworks)
        print("\n✨ Done! Your vibe coding gallery has been updated.")
        print("The gallery will automatically load vibe_gallery_config.json")
        print("when opened in a browser.")
    else:
        print("\n❌ Cancelled. No changes made.")

if __name__ == "__main__":
    main()