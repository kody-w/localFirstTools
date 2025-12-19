#!/usr/bin/env python3
"""
LEVIATHAN Cleanup Pass 2 - More aggressive cleanup
"""

import re

def cleanup_pass2(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    # 1. Remove lines that are just section markers (======)
    content = re.sub(r'\n\s*//\s*={5,}\s*\n', '\n', content)

    # 2. Remove "END" comments
    content = re.sub(r'\n\s*//\s*(?:END|end)[^\n]*\n', '\n', content)

    # 3. Remove standalone version comments that slipped through
    content = re.sub(r'\n\s*//\s*v\d+\.?\d*[:.][^\n]{0,30}\n', '\n', content)

    # 4. Collapse multiple empty lines into max 2
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 5. Remove trailing whitespace
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]
    content = '\n'.join(lines)

    # 6. Remove empty comment lines
    content = re.sub(r'\n\s*//\s*\n', '\n', content)

    # 7. Clean up version references in remaining comments (just strip the v#.# prefix)
    content = re.sub(r'// v\d+\.?\d*: ', '// ', content)
    content = re.sub(r'/\* v\d+\.?\d*: ', '/* ', content)

    # 8. Remove "Agent consensus" type comments
    content = re.sub(r'\s*\([^)]*[Aa]gent[^)]*consensus[^)]*\)', '', content)
    content = re.sub(r'\s*\([^)]*[Cc]ycle \d+[^)]*\)', '', content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    final_len = len(content)
    final_lines = content.count('\n') + 1

    print(f"Pass 2 complete:")
    print(f"  Size: {original_len:,} -> {final_len:,} chars ({100*(original_len-final_len)/original_len:.1f}% reduction)")
    print(f"  Final lines: {final_lines:,}")

if __name__ == '__main__':
    cleanup_pass2('leviv2.html', 'leviv2.html')
