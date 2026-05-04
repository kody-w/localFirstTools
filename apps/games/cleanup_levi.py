#!/usr/bin/env python3
"""
LEVIATHAN Cleanup Script
Removes version comments and cruft while preserving ALL functionality
"""

import re
import sys

def clean_leviathan(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    prev_empty = False
    in_multiline_comment = False

    # Patterns to remove or clean
    version_comment_only = re.compile(r'^\s*//\s*v\d+\.?\d*:.*$')  # Lines that are ONLY version comments
    version_prefix = re.compile(r'//\s*v\d+\.?\d*:\s*')  # Version prefix to strip from useful comments
    consensus_comment = re.compile(r'^\s*//.*(?:8-[Ss]trategy|8-agent|Consensus|Cycle \d+).*$')
    redundant_section_marker = re.compile(r'^\s*//\s*={10,}\s*$')  # Lines of just ====
    end_section_comment = re.compile(r'^\s*//\s*(?:END|end)\s+v\d+.*$')  # // END v6.33 FEATURES

    stats = {
        'version_comments_removed': 0,
        'consensus_comments_removed': 0,
        'empty_lines_collapsed': 0,
        'version_prefixes_stripped': 0,
        'total_lines_removed': 0
    }

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines if previous was also empty (collapse multiple empty lines)
        if stripped == '':
            if prev_empty:
                stats['empty_lines_collapsed'] += 1
                i += 1
                continue
            prev_empty = True
            cleaned_lines.append('\n')
            i += 1
            continue

        prev_empty = False

        # Remove lines that are ONLY version comments with no useful info
        # But keep ones that have actual documentation
        if version_comment_only.match(line):
            # Check if this is just a version marker or has useful info
            comment_text = re.sub(r'^\s*//\s*v\d+\.?\d*:\s*', '', line).strip()
            # Keep if it has substantial documentation (more than just a few words)
            if len(comment_text) < 50 and not any(word in comment_text.lower() for word in ['fix', 'bug', 'important', 'note', 'warning', 'todo', 'hack']):
                stats['version_comments_removed'] += 1
                i += 1
                continue

        # Remove consensus/strategy meta-comments
        if consensus_comment.match(line):
            stats['consensus_comments_removed'] += 1
            i += 1
            continue

        # Remove END section markers
        if end_section_comment.match(line):
            stats['version_comments_removed'] += 1
            i += 1
            continue

        # Strip version prefixes from inline comments but keep the description
        if version_prefix.search(line):
            # Only strip if it's a comment, not code
            if '//' in line:
                code_part = line.split('//')[0]
                comment_part = '//'.join(line.split('//')[1:])
                # Remove version prefix from comment
                cleaned_comment = version_prefix.sub('', comment_part)
                if cleaned_comment.strip():
                    line = code_part + '// ' + cleaned_comment.strip() + '\n'
                    stats['version_prefixes_stripped'] += 1
                else:
                    # Comment was only version info, remove it
                    line = code_part.rstrip() + '\n'

        cleaned_lines.append(line)
        i += 1

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

    original_lines = len(lines)
    final_lines = len(cleaned_lines)
    stats['total_lines_removed'] = original_lines - final_lines

    print(f"=== CLEANUP COMPLETE ===")
    print(f"Original lines: {original_lines:,}")
    print(f"Final lines: {final_lines:,}")
    print(f"Lines removed: {stats['total_lines_removed']:,} ({100*stats['total_lines_removed']/original_lines:.1f}%)")
    print(f"")
    print(f"Breakdown:")
    print(f"  Version comments removed: {stats['version_comments_removed']:,}")
    print(f"  Consensus comments removed: {stats['consensus_comments_removed']:,}")
    print(f"  Empty lines collapsed: {stats['empty_lines_collapsed']:,}")
    print(f"  Version prefixes stripped: {stats['version_prefixes_stripped']:,}")

    return stats

if __name__ == '__main__':
    input_file = 'levi.html'
    output_file = 'levi_cleaned.html'

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    clean_leviathan(input_file, output_file)
