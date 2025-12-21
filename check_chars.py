with open('apps/games/leviv4.html', 'rb') as f:
    content = f.read()

# Check for U+2028 (Line Separator) and U+2029 (Paragraph Separator)
# In UTF-8:
# U+2028 is E2 80 A8
# U+2029 is E2 80 A9

if b'\xe2\x80\xa8' in content:
    print("Found U+2028")
if b'\xe2\x80\xa9' in content:
    print("Found U+2029")

# Check for null bytes
if b'\x00' in content:
    print("Found null byte")
