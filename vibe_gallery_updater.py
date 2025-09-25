#!/usr/bin/env python3

import json
import os
from pathlib import Path
from datetime import datetime
import re
from html.parser import HTMLParser

class HTMLMetadataExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.description = None
        self.in_title = False
        self.meta_tags = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            attr_dict = dict(attrs)
            self.meta_tags.append(attr_dict)
            if attr_dict.get("name") == "description":
                self.description = attr_dict.get("content", "")

    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

def extract_metadata_from_html(filepath):
    """Extract title and description from HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()[:5000]  # Read first 5000 chars for metadata

        parser = HTMLMetadataExtractor()
        parser.feed(content)

        title = parser.title or Path(filepath).stem.replace('-', ' ').title()
        description = parser.description or ""

        # Try to extract features from content for tags
        tags = []
        content_lower = content.lower()

        # Common technology/feature keywords
        tech_keywords = {
            '3d': ['three.js', 'webgl', '3d', 'canvas 3d', 'perspective'],
            'canvas': ['canvas', 'getcontext'],
            'svg': ['svg', 'path', 'circle', 'rect'],
            'audio': ['audio', 'sound', 'music', 'webaudio', 'audiocontext'],
            'animation': ['animate', 'requestanimationframe', 'transition'],
            'interactive': ['click', 'drag', 'touch', 'mouse', 'keyboard'],
            'game': ['game', 'score', 'level', 'player', 'enemy'],
            'generative': ['random', 'generate', 'procedural', 'noise'],
            'particles': ['particle', 'emitter'],
            'physics': ['physics', 'gravity', 'collision', 'velocity'],
            'drawing': ['draw', 'paint', 'brush', 'pen'],
            'visualization': ['visualiz', 'chart', 'graph', 'data'],
            'terminal': ['terminal', 'console', 'command'],
            'retro': ['retro', 'vintage', 'pixel', '8-bit', 'arcade'],
            'creative': ['creative', 'art', 'design', 'aesthetic']
        }

        for tag, keywords in tech_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(tag)

        # Determine complexity based on file size and features
        file_size = len(content)
        if file_size > 50000 or '3d' in tags or 'webgl' in tags:
            complexity = "advanced"
        elif file_size > 20000 or 'game' in tags:
            complexity = "intermediate"
        else:
            complexity = "simple"

        # Determine interaction type
        if 'game' in tags:
            interaction_type = "game"
        elif 'drawing' in tags or 'paint' in tags:
            interaction_type = "drawing"
        elif 'terminal' in tags or 'console' in content_lower:
            interaction_type = "interface"
        elif 'music' in tags or 'audio' in tags:
            interaction_type = "audio"
        elif any(word in content_lower for word in ['click', 'drag', 'touch']):
            interaction_type = "interactive"
        else:
            interaction_type = "visual"

        return {
            "title": title,
            "description": description if description else f"Interactive {title.lower()} experience",
            "tags": tags[:6],  # Limit to 6 tags
            "complexity": complexity,
            "interactionType": interaction_type
        }
    except Exception as e:
        print(f"Error extracting metadata from {filepath}: {e}")
        return None

def categorize_app(filepath, metadata):
    """Determine the best category for an app based on its path and metadata"""
    path_str = str(filepath).lower()
    tags = metadata.get("tags", [])
    title_lower = metadata.get("title", "").lower()
    desc_lower = metadata.get("description", "").lower()

    # Category mapping based on directory and content
    if "games" in path_str or "game" in tags or "game" in title_lower:
        if "3d" in tags or "webgl" in tags:
            return "3d_immersive"
        elif "puzzle" in title_lower or "puzzle" in desc_lower:
            return "games_puzzles"
        else:
            return "games_puzzles"

    elif "media" in path_str or "music" in tags or "audio" in tags:
        return "audio_music"

    elif any(art_word in path_str or art_word in title_lower or art_word in desc_lower
             for art_word in ["art", "draw", "paint", "design", "creative", "svg", "canvas"]):
        if "generative" in tags or "generative" in desc_lower:
            return "generative_art"
        else:
            return "visual_art"

    elif "education" in path_str or "learn" in title_lower or "tutorial" in title_lower:
        if any(tech in tags for tech in ["terminal", "code", "programming"]):
            return "educational_tools"
        else:
            return "visual_art"

    elif "ai" in path_str or "ai" in tags or "neural" in title_lower:
        return "experimental_ai"

    elif "productivity" in path_str or "utilities" in path_str:
        return "creative_tools"

    elif "3d" in tags or "webgl" in tags or "three" in title_lower:
        return "3d_immersive"

    elif "particles" in tags or "physics" in tags or "simulation" in desc_lower:
        return "particle_physics"

    elif "generative" in tags or "procedural" in desc_lower:
        return "generative_art"

    else:
        # Default category based on interaction type
        interaction = metadata.get("interactionType", "visual")
        if interaction == "game":
            return "games_puzzles"
        elif interaction == "audio":
            return "audio_music"
        elif interaction == "drawing":
            return "visual_art"
        else:
            return "experimental_ai"  # Default fallback

def scan_directories_for_apps(base_path):
    """Scan directories for HTML files and extract their metadata"""
    apps_by_category = {
        "visual_art": [],
        "3d_immersive": [],
        "audio_music": [],
        "generative_art": [],
        "games_puzzles": [],
        "particle_physics": [],
        "creative_tools": [],
        "experimental_ai": [],
        "educational_tools": []
    }

    # Scan ALL directories for HTML files
    # First scan apps directory and its subdirectories
    apps_path = Path(base_path) / "apps"
    if apps_path.exists():
        for html_file in apps_path.rglob("*.html"):
            if html_file.name.startswith('.'):
                continue  # Skip hidden files

            print(f"Processing: {html_file}")
            metadata = extract_metadata_from_html(html_file)

            if metadata:
                category = categorize_app(html_file, metadata)
                relative_path = html_file.relative_to(base_path)

                app_entry = {
                    "title": metadata["title"],
                    "filename": html_file.name,
                    "path": str(relative_path),
                    "description": metadata["description"],
                    "tags": metadata["tags"],
                    "category": category,
                    "featured": len(metadata["tags"]) >= 3,
                    "complexity": metadata["complexity"],
                    "interactionType": metadata["interactionType"]
                }

                apps_by_category[category].append(app_entry)

    # Also scan root directory for HTML files
    root_path = Path(base_path)
    for html_file in root_path.glob("*.html"):
        if html_file.name.startswith('.') or html_file.name == 'index.html':
            continue  # Skip hidden files and index.html

        print(f"Processing: {html_file}")
        metadata = extract_metadata_from_html(html_file)

        if metadata:
            category = categorize_app(html_file, metadata)

            app_entry = {
                "title": metadata["title"],
                "filename": html_file.name,
                "path": html_file.name,  # Just filename for root files
                "description": metadata["description"],
                "tags": metadata["tags"],
                "category": category,
                "featured": len(metadata["tags"]) >= 3,
                "complexity": metadata["complexity"],
                "interactionType": metadata["interactionType"]
            }

            apps_by_category[category].append(app_entry)

    # Scan other directories at root level (artifacts, archive, etc.)
    other_dirs = ["artifacts", "archive", "notes", "edgeAddons"]
    for dir_name in other_dirs:
        dir_path = Path(base_path) / dir_name
        if not dir_path.exists():
            continue

        # Recursively scan for HTML files in these directories
        for html_file in dir_path.rglob("*.html"):
            if html_file.name.startswith('.'):
                continue  # Skip hidden files

            print(f"Processing: {html_file}")
            metadata = extract_metadata_from_html(html_file)

            if metadata:
                category = categorize_app(html_file, metadata)
                relative_path = html_file.relative_to(base_path)

                app_entry = {
                    "title": metadata["title"],
                    "filename": html_file.name,
                    "path": str(relative_path),
                    "description": metadata["description"],
                    "tags": metadata["tags"],
                    "category": category,
                    "featured": len(metadata["tags"]) >= 3,
                    "complexity": metadata["complexity"],
                    "interactionType": metadata["interactionType"]
                }

                apps_by_category[category].append(app_entry)

    return apps_by_category

def update_vibe_gallery_config(base_path):
    """Update the vibe_gallery_config.json file with discovered apps"""
    config_path = Path(base_path) / "vibe_gallery_config.json"  # Root directory

    # Load existing config or create new structure
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "vibeGallery": {
                "title": "Vibe Gallery - Interactive Artworks & Creative Applications",
                "description": "A curated collection of interactive artworks, generative art pieces, and creative digital experiences",
                "lastUpdated": "",
                "version": "1.0.0",
                "categories": {}
            }
        }

    # Category definitions
    category_info = {
        "visual_art": {
            "title": "Visual Art & Design",
            "description": "Interactive visual experiences, generative art, and design tools",
            "color": "#ff6b9d"
        },
        "3d_immersive": {
            "title": "3D & Immersive Worlds",
            "description": "Three-dimensional experiences and explorable virtual environments",
            "color": "#4ecdc4"
        },
        "audio_music": {
            "title": "Audio & Music",
            "description": "Sound synthesis, music creation, and audio visualization tools",
            "color": "#95e1d3"
        },
        "generative_art": {
            "title": "Generative Art",
            "description": "Algorithmic and procedural art generation systems",
            "color": "#c9b1ff"
        },
        "games_puzzles": {
            "title": "Games & Puzzles",
            "description": "Interactive games, puzzles, and playful experiences",
            "color": "#feca57"
        },
        "particle_physics": {
            "title": "Particle & Physics",
            "description": "Particle systems, physics simulations, and dynamic interactions",
            "color": "#48dbfb"
        },
        "creative_tools": {
            "title": "Creative Tools",
            "description": "Utilities and tools for creative expression and productivity",
            "color": "#ff9ff3"
        },
        "experimental_ai": {
            "title": "Experimental & AI",
            "description": "Experimental interfaces, AI-powered experiences, and cutting-edge demos",
            "color": "#54a0ff"
        },
        "educational_tools": {
            "title": "Educational Tools",
            "description": "Learning resources, tutorials, and educational interactives",
            "color": "#00d2d3"
        }
    }

    # Scan for apps
    apps_by_category = scan_directories_for_apps(base_path)

    # Update config with discovered apps
    for category_key, category_meta in category_info.items():
        if apps_by_category.get(category_key):
            config["vibeGallery"]["categories"][category_key] = {
                **category_meta,
                "apps": sorted(apps_by_category[category_key],
                             key=lambda x: (not x.get("featured", False), x["title"]))
            }

    # Update timestamp
    config["vibeGallery"]["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")

    # Write updated config to root directory
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    # Print summary
    total_apps = sum(len(apps) for apps in apps_by_category.values())
    print(f"\n✅ Successfully updated vibe_gallery_config.json")
    print(f"📊 Found {total_apps} total apps across {len([c for c in apps_by_category if apps_by_category[c]])} categories:")
    for category, apps in apps_by_category.items():
        if apps:
            print(f"  • {category_info[category]['title']}: {len(apps)} apps")

    return config_path

if __name__ == "__main__":
    # Get the base directory (where this script is located or current directory)
    base_dir = Path.cwd()

    print(f"🔍 Scanning for apps in: {base_dir}")
    print("=" * 50)

    try:
        config_file = update_vibe_gallery_config(base_dir)
        print(f"\n📁 Config file updated: {config_file}")
    except Exception as e:
        print(f"\n❌ Error updating config: {e}")
        import traceback
        traceback.print_exc()