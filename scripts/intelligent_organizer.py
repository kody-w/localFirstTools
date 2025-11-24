#!/usr/bin/env python3
"""
Intelligent Application Organizer for localFirstTools
Analyzes HTML application content to automatically categorize and organize files
"""

import os
import re
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

class IntelligentOrganizer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.apps_dir = self.base_path / "apps"
        self.data_dir = self.base_path / "data" / "config"
        self.archive_dir = self.base_path / "archive"
        
        # Category definitions with keywords and patterns
        self.categories = {
            'games': {
                'keywords': ['game', 'play', 'score', 'level', 'player', 'enemy', 'sprite', 
                           'collision', 'gameloop', 'canvas', 'fps', 'joystick', 'controller'],
                'patterns': [r'requestAnimationFrame', r'canvas\.getContext', r'keyCode|key\s*===',
                           r'score\s*[+=]', r'lives\s*-=', r'gameOver', r'startGame'],
                'file_keywords': ['game', 'snake', 'racing', 'poker', 'solitaire', 'tetris', 
                                'invaders', 'breakout', 'simulator', 'emulator'],
                'weight': 1.0
            },
            'ai-tools': {
                'keywords': ['ai', 'agent', 'llm', 'gpt', 'claude', 'model', 'prompt', 
                           'completion', 'embedding', 'inference', 'neural', 'machine learning'],
                'patterns': [r'fetch.*api.*openai', r'fetch.*anthropic', r'prompt\s*=', 
                           r'completion', r'\.generate\(', r'model\s*:', r'temperature\s*:'],
                'file_keywords': ['ai', 'agent', 'claude', 'gpt', 'copilot', 'llm', 'ml'],
                'weight': 1.2
            },
            'productivity': {
                'keywords': ['task', 'todo', 'note', 'document', 'write', 'editor', 'markdown',
                           'organize', 'schedule', 'calendar', 'reminder', 'journal'],
                'patterns': [r'localStorage\.(get|set)Item.*todo', r'contenteditable', 
                           r'document\.execCommand', r'markdown', r'\.save\(\)', r'autosave'],
                'file_keywords': ['note', 'todo', 'task', 'writer', 'editor', 'journal', 'diary'],
                'weight': 0.9
            },
            'business': {
                'keywords': ['crm', 'sales', 'customer', 'revenue', 'dashboard', 'analytics',
                           'report', 'chart', 'presentation', 'invoice', 'finance'],
                'patterns': [r'chart|Chart', r'graph|Graph', r'revenue|Revenue', 
                           r'customer|Customer', r'sales|Sales', r'\.toLocaleString.*currency'],
                'file_keywords': ['crm', 'dashboard', 'presentation', 'sales', 'business', 'invoice'],
                'weight': 0.95
            },
            'media': {
                'keywords': ['video', 'audio', 'record', 'camera', 'microphone', 'stream',
                           'media', 'capture', 'playback', 'volume', 'mixer'],
                'patterns': [r'getUserMedia', r'MediaRecorder', r'video|audio', r'stream',
                           r'AudioContext', r'canvas.*drawImage.*video', r'mediaDevices'],
                'file_keywords': ['recorder', 'camera', 'audio', 'video', 'media', 'drum', 'music'],
                'weight': 1.1
            },
            'development': {
                'keywords': ['code', 'debug', 'compile', 'git', 'github', 'api', 'json',
                           'terminal', 'console', 'syntax', 'highlight', 'lint'],
                'patterns': [r'console\.(log|error|debug)', r'JSON\.(parse|stringify)', 
                           r'fetch.*github', r'SyntaxHighlight', r'eval\(', r'Function\('],
                'file_keywords': ['code', 'github', 'git', 'debug', 'terminal', 'console', 'dev'],
                'weight': 0.85
            },
            'education': {
                'keywords': ['learn', 'teach', 'quiz', 'test', 'tutorial', 'guide', 'course',
                           'student', 'lesson', 'practice', 'training', 'skill'],
                'patterns': [r'question|Question', r'answer|Answer', r'correct|incorrect',
                           r'score.*quiz', r'lesson', r'tutorial', r'practice'],
                'file_keywords': ['learn', 'teach', 'tutorial', 'trainer', 'quiz', 'education'],
                'weight': 0.9
            },
            'health': {
                'keywords': ['health', 'fitness', 'exercise', 'workout', 'meditation', 'breath',
                           'wellness', 'medical', 'therapy', 'mindful', 'relax'],
                'patterns': [r'breath|Breath', r'inhale|exhale', r'meditation', r'workout',
                           r'exercise', r'heart.*rate', r'calories'],
                'file_keywords': ['health', 'fitness', 'breath', 'meditation', 'workout', 'emdr'],
                'weight': 1.0
            },
            'utilities': {
                'keywords': ['convert', 'calculate', 'transform', 'utility', 'tool', 'helper',
                           'format', 'parse', 'process', 'analyze'],
                'patterns': [r'convert|Convert', r'calculate|Calculate', r'transform|Transform',
                           r'parse|Parse', r'format|Format'],
                'file_keywords': ['converter', 'calculator', 'utility', 'tool', 'helper'],
                'weight': 0.7
            }
        }
        
        self.analysis_cache = {}
        
    def analyze_html_content(self, file_path: Path) -> Dict[str, float]:
        """Analyze HTML file content and return category scores"""
        
        if str(file_path) in self.analysis_cache:
            return self.analysis_cache[str(file_path)]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return {}
        
        scores = {}
        filename = file_path.name.lower()
        
        # Extract meaningful text from HTML
        # Remove script and style content for text analysis
        text_content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        text_content = re.sub(r'<style[^>]*>.*?</style>', '', text_content, flags=re.DOTALL)
        text_content = re.sub(r'<[^>]+>', ' ', text_content)  # Remove HTML tags
        
        # Keep full content for pattern matching
        full_content = content
        
        for category, config in self.categories.items():
            score = 0.0
            
            # Check filename keywords (higher weight)
            for keyword in config['file_keywords']:
                if keyword in filename:
                    score += 3.0
            
            # Check content keywords
            for keyword in config['keywords']:
                # Count occurrences (normalized)
                count = text_content.count(keyword)
                if count > 0:
                    score += min(count * 0.5, 3.0)  # Cap at 3.0 per keyword
            
            # Check patterns in full content (including scripts)
            for pattern in config['patterns']:
                matches = re.findall(pattern, full_content, re.IGNORECASE)
                if matches:
                    score += min(len(matches) * 0.7, 4.0)  # Cap at 4.0 per pattern
            
            # Apply category weight
            score *= config['weight']
            
            # Special boost for strong indicators
            if category == 'games' and 'canvas' in full_content and 'requestanimationframe' in full_content:
                score += 5.0
            elif category == 'ai-tools' and ('anthropic' in full_content or 'openai' in full_content):
                score += 5.0
            elif category == 'media' and 'getusermedia' in full_content:
                score += 5.0
            
            scores[category] = score
        
        # Cache the result
        self.analysis_cache[str(file_path)] = scores
        return scores
    
    def determine_category(self, file_path: Path) -> str:
        """Determine the best category for a file based on content analysis"""
        
        # Special cases - files that should stay in specific locations
        filename = file_path.name
        if filename in ['index.html', 'CLAUDE.md', 'README.md']:
            return 'root'
        
        # Check if it's an index variant
        if 'index' in filename.lower() and filename.endswith('.html'):
            return 'apps/index-variants'
        
        # Analyze content
        scores = self.analyze_html_content(file_path)
        
        if not scores:
            return 'utilities'  # Default category
        
        # Find category with highest score
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]
        
        # If score is too low, default to utilities
        if best_score < 2.0:
            return 'utilities'
        
        return best_category
    
    def extract_app_metadata(self, file_path: Path) -> Dict:
        """Extract metadata from HTML file for config generation"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return None
        
        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
        title = title_match.group(1) if title_match else file_path.stem.replace('-', ' ').title()
        
        # Extract description from comments or meta tags
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content, re.IGNORECASE)
        if not desc_match:
            # Try to find a comment with description
            desc_match = re.search(r'<!--\s*Description:\s*([^-]+)-->', content, re.IGNORECASE)
        
        description = desc_match.group(1) if desc_match else f"A {self.determine_category(file_path)} application"
        
        # Generate ID from filename
        app_id = file_path.stem.replace('-', '_').replace(' ', '_').lower()
        
        # Determine icon based on category
        category = self.determine_category(file_path)
        icons = {
            'games': '🎮',
            'ai-tools': '🤖',
            'productivity': '📝',
            'business': '💼',
            'media': '🎬',
            'development': '💻',
            'education': '📚',
            'health': '🧘',
            'utilities': '🔧'
        }
        icon = icons.get(category, '📱')
        
        # Generate tags based on content analysis
        tags = [category]
        scores = self.analyze_html_content(file_path)
        for cat, score in scores.items():
            if cat != category and score > 3.0:
                tags.append(cat)
        
        return {
            'id': app_id,
            'title': title,
            'description': description,
            'tags': tags[:3],  # Limit to 3 tags
            'path': str(file_path.relative_to(self.base_path)),
            'icon': icon,
            'category': category,
            'confidence': scores.get(category, 0) if scores else 0
        }
    
    def organize_files(self, dry_run: bool = True, verbose: bool = False):
        """Main organization function"""
        
        print(f"{'[DRY RUN] ' if dry_run else ''}Intelligent File Organization Starting...")
        print(f"Analyzing applications in: {self.base_path}")
        print("-" * 60)
        
        # Collect all HTML files
        html_files = []
        
        # Check root directory
        for file_path in self.base_path.glob("*.html"):
            if file_path.name != 'index.html':  # Skip main index
                html_files.append(file_path)
        
        # Check apps directory recursively
        if self.apps_dir.exists():
            for file_path in self.apps_dir.rglob("*.html"):
                html_files.append(file_path)
        
        # Check archive directory
        if self.archive_dir.exists():
            for file_path in self.archive_dir.glob("*.html"):
                html_files.append(file_path)
        
        print(f"Found {len(html_files)} HTML files to analyze\n")
        
        # Organize files
        moves = []
        app_configs = []
        
        for file_path in html_files:
            category = self.determine_category(file_path)
            
            if category == 'root':
                continue
            
            # Determine target directory
            if category.startswith('apps/'):
                target_dir = self.base_path / category
            else:
                target_dir = self.apps_dir / category
            
            target_path = target_dir / file_path.name
            
            # Check if file needs to move
            if file_path.parent != target_dir:
                moves.append((file_path, target_path))
                
                if verbose:
                    scores = self.analyze_html_content(file_path)
                    print(f"\n📄 {file_path.name}")
                    print(f"   Category: {category}")
                    print(f"   Confidence: {scores.get(category, 0):.1f}")
                    print(f"   From: {file_path.parent.relative_to(self.base_path)}")
                    print(f"   To:   {target_dir.relative_to(self.base_path)}")
                    if len(scores) > 1:
                        print(f"   Other scores: {', '.join(f'{k}:{v:.1f}' for k,v in sorted(scores.items(), key=lambda x: -x[1])[:3] if k != category)}")
            
            # Extract metadata for config
            metadata = self.extract_app_metadata(file_path)
            if metadata:
                # Update path to reflect new location
                metadata['path'] = f"./apps/{category}/{file_path.name}"
                app_configs.append(metadata)
        
        # Summary
        print("\n" + "=" * 60)
        print(f"Organization Summary:")
        print(f"  Total files analyzed: {len(html_files)}")
        print(f"  Files to move: {len(moves)}")
        
        if moves:
            # Count by category
            category_counts = defaultdict(int)
            for _, target in moves:
                cat = target.parent.name
                category_counts[cat] += 1
            
            print(f"\n  Distribution by category:")
            for cat, count in sorted(category_counts.items()):
                print(f"    {cat}: {count} files")
        
        if not dry_run and moves:
            print(f"\n🚀 Executing moves...")
            for source, target in moves:
                try:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source), str(target))
                    print(f"  ✓ Moved {source.name}")
                except Exception as e:
                    print(f"  ✗ Failed to move {source.name}: {e}")
            
            # Generate updated config file
            self.generate_config_file(app_configs)
            print(f"\n✓ Configuration file updated")
        elif dry_run and moves:
            print(f"\n💡 Run with --execute to perform these moves")
        else:
            print(f"\n✓ All files are already organized correctly!")
    
    def generate_config_file(self, app_configs: List[Dict]):
        """Generate the utility_apps_config.json file"""
        
        config_file = self.data_dir / "utility_apps_config.json"
        
        # Sort by category and title
        app_configs.sort(key=lambda x: (x['category'], x['title']))
        
        # Remove internal fields
        for config in app_configs:
            config.pop('category', None)
            config.pop('confidence', None)
        
        config_data = {
            'version': '3.0',
            'lastUpdated': datetime.now().isoformat(),
            'generatedBy': 'intelligent_organizer.py',
            'apps': app_configs
        }
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    def analyze_single_file(self, file_path: str):
        """Analyze a single file and show detailed results"""
        
        path = Path(file_path)
        if not path.exists():
            print(f"File not found: {file_path}")
            return
        
        print(f"\n📊 Detailed Analysis: {path.name}")
        print("=" * 60)
        
        scores = self.analyze_html_content(path)
        metadata = self.extract_app_metadata(path)
        
        if not scores:
            print("Unable to analyze file")
            return
        
        # Sort scores by value
        sorted_scores = sorted(scores.items(), key=lambda x: -x[1])
        
        print(f"\n🏷️  Category Scores:")
        for category, score in sorted_scores:
            bar = '█' * int(score * 2)
            print(f"  {category:15} {score:6.2f}  {bar}")
        
        print(f"\n🎯 Recommended Category: {sorted_scores[0][0]}")
        
        if metadata:
            print(f"\n📋 Extracted Metadata:")
            print(f"  Title:       {metadata['title']}")
            print(f"  Description: {metadata['description']}")
            print(f"  Tags:        {', '.join(metadata['tags'])}")
            print(f"  Icon:        {metadata['icon']}")


def main():
    parser = argparse.ArgumentParser(
        description='Intelligent Application Organizer for localFirstTools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Dry run - show what would be moved
  %(prog)s --execute         # Actually move files
  %(prog)s --verbose         # Show detailed analysis
  %(prog)s --analyze file.html  # Analyze a single file
        """
    )
    
    parser.add_argument('--execute', action='store_true',
                       help='Actually move files (default is dry run)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed analysis for each file')
    parser.add_argument('--analyze', '-a', metavar='FILE',
                       help='Analyze a single file and show detailed results')
    parser.add_argument('--path', default='.',
                       help='Base path for the project (default: current directory)')
    
    args = parser.parse_args()
    
    organizer = IntelligentOrganizer(args.path)
    
    if args.analyze:
        organizer.analyze_single_file(args.analyze)
    else:
        organizer.organize_files(dry_run=not args.execute, verbose=args.verbose)


if __name__ == '__main__':
    main()