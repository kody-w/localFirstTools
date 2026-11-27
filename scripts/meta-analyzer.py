#!/usr/bin/env python3
"""
META ANALYZER - Comprehensive codebase analysis tool
Analyzes all 172+ apps in localFirstTools and generates insights
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

class MetaAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.apps_data = []
        self.patterns = defaultdict(list)
        self.dependencies = defaultdict(set)

    def analyze_html_file(self, file_path):
        """Extract metadata from a single HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else file_path.name

            # Extract meta description
            desc_match = re.search(r'<meta.*?description.*?content=["\']([^"\']+)', content, re.IGNORECASE)
            description = desc_match.group(1) if desc_match else ""

            # Count lines of code
            lines = content.count('\n')

            # Detect technologies
            technologies = set()
            if 'three.js' in content.lower() or 'THREE.' in content:
                technologies.add('Three.js')
            if 'webrtc' in content.lower() or 'RTCPeerConnection' in content:
                technologies.add('WebRTC')
            if 'localStorage' in content:
                technologies.add('localStorage')
            if 'indexedDB' in content or 'IndexedDB' in content:
                technologies.add('IndexedDB')
            if 'canvas' in content.lower() or 'getContext' in content:
                technologies.add('Canvas')
            if 'webgl' in content.lower():
                technologies.add('WebGL')
            if 'worker' in content.lower():
                technologies.add('Web Workers')
            if 'websocket' in content.lower():
                technologies.add('WebSocket')

            # Detect patterns
            has_import_export = 'export' in content.lower() and 'import' in content.lower()
            has_json_storage = 'JSON.stringify' in content or 'JSON.parse' in content
            has_3d = any(tech in technologies for tech in ['Three.js', 'WebGL'])
            has_networking = any(tech in technologies for tech in ['WebRTC', 'WebSocket'])

            # Extract dependencies (external scripts/libraries)
            script_matches = re.findall(r'<script.*?src=["\']([^"\']+)', content, re.IGNORECASE)
            cdn_dependencies = [s for s in script_matches if 'http' in s or 'cdn' in s]

            # File size
            file_size = file_path.stat().st_size

            # Category (from directory)
            relative_path = file_path.relative_to(self.root_dir)
            parts = list(relative_path.parts)
            category = parts[1] if len(parts) > 1 and parts[0] == 'apps' else 'other'

            return {
                'filename': file_path.name,
                'path': str(relative_path),
                'title': title,
                'description': description,
                'category': category,
                'lines_of_code': lines,
                'file_size': file_size,
                'technologies': list(technologies),
                'has_import_export': has_import_export,
                'has_json_storage': has_json_storage,
                'has_3d': has_3d,
                'has_networking': has_networking,
                'external_dependencies': cdn_dependencies,
                'is_self_contained': len(cdn_dependencies) == 0
            }
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None

    def scan_all_apps(self):
        """Scan all HTML files in the apps directory"""
        print("🔍 Scanning all applications...")

        for html_file in self.root_dir.rglob('*.html'):
            # Skip index files and archived backups
            if html_file.name.startswith('index') and html_file.parent == self.root_dir:
                continue
            if 'node_modules' in str(html_file):
                continue

            app_data = self.analyze_html_file(html_file)
            if app_data:
                self.apps_data.append(app_data)

        print(f"✅ Analyzed {len(self.apps_data)} applications")
        return self.apps_data

    def identify_patterns(self):
        """Identify common patterns across all apps"""
        print("\n🔍 Identifying patterns...")

        patterns = {
            'local_first': [],
            '3d_visualization': [],
            'p2p_networking': [],
            'self_contained': [],
            'large_apps': [],
            'tiny_apps': [],
            'games': [],
            'tools': [],
            'ai_powered': []
        }

        for app in self.apps_data:
            if app['has_json_storage']:
                patterns['local_first'].append(app['filename'])
            if app['has_3d']:
                patterns['3d_visualization'].append(app['filename'])
            if app['has_networking']:
                patterns['p2p_networking'].append(app['filename'])
            if app['is_self_contained']:
                patterns['self_contained'].append(app['filename'])
            if app['file_size'] > 200000:  # > 200KB
                patterns['large_apps'].append(app['filename'])
            if app['file_size'] < 10000:  # < 10KB
                patterns['tiny_apps'].append(app['filename'])
            if app['category'] == 'games':
                patterns['games'].append(app['filename'])
            if 'ai' in app['title'].lower() or 'ai' in app['description'].lower():
                patterns['ai_powered'].append(app['filename'])

        self.patterns = patterns
        return patterns

    def generate_category_report(self):
        """Generate report on category distribution and gaps"""
        print("\n📊 Generating category report...")

        category_counts = Counter(app['category'] for app in self.apps_data)

        # Define ideal distribution
        ideal_counts = {
            'games': 30,
            'productivity': 25,
            'utilities': 20,
            'education': 15,
            'development': 15,
            'business': 10,
            'media': 10,
            'ai-tools': 15,
            'health': 8
        }

        gaps = {}
        for category, ideal in ideal_counts.items():
            actual = category_counts.get(category, 0)
            if actual < ideal:
                gaps[category] = {
                    'current': actual,
                    'ideal': ideal,
                    'gap': ideal - actual
                }

        return {
            'distribution': dict(category_counts),
            'gaps': gaps,
            'recommendations': self._generate_recommendations(gaps)
        }

    def _generate_recommendations(self, gaps):
        """Generate specific app recommendations based on gaps"""
        recommendations = []

        for category, data in sorted(gaps.items(), key=lambda x: x[1]['gap'], reverse=True):
            if category == 'productivity':
                recommendations.append({
                    'category': category,
                    'suggestions': [
                        'Pomodoro timer with focus mode',
                        'Mind mapping tool with collaborative features',
                        'Habit tracker with statistics',
                        'Project management kanban board'
                    ]
                })
            elif category == 'education':
                recommendations.append({
                    'category': category,
                    'suggestions': [
                        'Interactive chemistry periodic table',
                        'Math equation visualizer',
                        'Language learning flashcards',
                        'Code tutorial playground'
                    ]
                })
            elif category == 'health':
                recommendations.append({
                    'category': category,
                    'suggestions': [
                        'Calorie tracker with meal planning',
                        'Workout routine builder',
                        'Sleep cycle tracker',
                        'Meditation timer with ambient sounds'
                    ]
                })

        return recommendations

    def generate_technology_stats(self):
        """Generate statistics on technology usage"""
        tech_usage = Counter()
        for app in self.apps_data:
            for tech in app['technologies']:
                tech_usage[tech] += 1

        return dict(tech_usage)

    def export_analysis(self, output_file):
        """Export complete analysis as JSON"""
        analysis = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_apps': len(self.apps_data),
                'analyzer_version': '1.0.0'
            },
            'apps': self.apps_data,
            'patterns': {k: len(v) for k, v in self.patterns.items()},
            'pattern_details': self.patterns,
            'category_report': self.generate_category_report(),
            'technology_stats': self.generate_technology_stats(),
            'statistics': {
                'total_lines_of_code': sum(app['lines_of_code'] for app in self.apps_data),
                'total_file_size': sum(app['file_size'] for app in self.apps_data),
                'avg_file_size': sum(app['file_size'] for app in self.apps_data) / len(self.apps_data),
                'self_contained_apps': sum(1 for app in self.apps_data if app['is_self_contained'])
            }
        }

        output_path = self.root_dir / output_file
        with open(output_path, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"\n✅ Analysis exported to {output_file}")
        return analysis

def main():
    analyzer = MetaAnalyzer(Path(__file__).parent.parent)

    # Run analysis
    analyzer.scan_all_apps()
    analyzer.identify_patterns()

    # Export results
    analysis = analyzer.export_analysis('data/meta-analysis.json')

    # Print summary
    print("\n" + "="*60)
    print("📊 ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total Apps: {analysis['metadata']['total_apps']}")
    print(f"Total Lines of Code: {analysis['statistics']['total_lines_of_code']:,}")
    print(f"Total Size: {analysis['statistics']['total_file_size'] / 1024 / 1024:.2f} MB")
    print(f"Self-Contained Apps: {analysis['statistics']['self_contained_apps']}")
    print("\nTop Technologies:")
    for tech, count in sorted(analysis['technology_stats'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  - {tech}: {count} apps")
    print("\nCategory Distribution:")
    for cat, count in sorted(analysis['category_report']['distribution'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat}: {count} apps")
    print("="*60)

if __name__ == '__main__':
    main()
