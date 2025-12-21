import re

def check_braces(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Find all script tags with their positions
    matches = list(re.finditer(r'<script[^>]*>(.*?)</script>', content, re.DOTALL))
    
    if not matches:
        print("No script tags found")
        return

    # Check the last script
    match = matches[-1]
    script_start = content[:match.start()].count('\n') + 1
    script = match.group(1)
    
    print(f"Checking script starting at line {script_start}")
    
    stack = []
    lines = script.split('\n')
    
    for i, line in enumerate(lines):
        # Simple check, ignores strings and comments which is risky but a start
        # To be more robust, we should strip comments and strings
        clean_line = re.sub(r'//.*', '', line) # Remove single line comments
        # We are not handling multi-line comments or strings containing braces here
        
        for char in clean_line:
            if char == '{':
                stack.append((char, i + 1))
            elif char == '}':
                if not stack:
                    print(f"Error: Unexpected '}}' at line {script_start + i}")
                    print(f"Line content: {line.strip()}")
                    return
                stack.pop()
    
    if stack:
        print(f"Error: Unclosed '{{' at line {stack[-1][1]}")
    else:
        print("Braces are balanced")

import sys
if len(sys.argv) > 1:
    check_braces(sys.argv[1])
else:
    print("Usage: python3 check_braces.py <filename>")
