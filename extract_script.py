import re

with open('apps/games/leviv4.html', 'r') as f:
    content = f.read()

matches = list(re.finditer(r'<script[^>]*>(.*?)</script>', content, re.DOTALL))
for i, match in enumerate(matches):
    script_content = match.group(1)
    filename = f'temp_script_{i}.js'
    with open(filename, 'w') as f:
        f.write(script_content)
    print(f"Extracted script {i} to {filename}")
