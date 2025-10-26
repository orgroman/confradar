"""Debug deadline extraction - check exact format."""
import re

with open('ai_deadlines_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find moment.tz calls with any quote type
pattern = r'moment\.tz\(([^)]+)\)'
matches = re.findall(pattern, html)
print(f"Found {len(matches)} moment.tz() calls")
if matches:
    print("\nFirst 10 calls:")
    for i, match in enumerate(matches[:10]):
        print(f"{i+1}. {repr(match)}")

# Also look for the conference ID mapping
pattern2 = r'\$\([\'"](#\w+).*?moment'
matches2 = re.findall(pattern2, html, re.DOTALL)
print(f"\nFound {len(matches2)} conference ID patterns")
if matches2:
    print("First 10:")
    for i, match in enumerate(matches2[:10]):
        print(f"{i+1}. {match}")
