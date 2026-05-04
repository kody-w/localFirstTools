
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'const EMBEDDED_MANIFEST\s*=\s*\[.*?\]\s*;'
match = re.search(pattern, content, flags=re.DOTALL)

if match:
    print("Match found!")
    print(f"Match length: {len(match.group(0))}")
else:
    print("No match found.")
    # Try to find where it starts
    start_pattern = r'const EMBEDDED_MANIFEST\s*=\s*\['
    start_match = re.search(start_pattern, content)
    if start_match:
        print("Start of pattern found.")
        start_pos = start_match.start()
        print(f"Context around start: {content[start_pos:start_pos+100]}")
    else:
        print("Start of pattern NOT found.")
