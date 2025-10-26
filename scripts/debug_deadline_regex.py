"""Debug the deadline extraction regex."""
import re

# Read the saved HTML
with open('ai_deadlines_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for the aistats25 deadline specifically
pattern1 = r"#aistats25.*?moment\.tz"
matches1 = re.findall(pattern1, html, re.DOTALL)
print(f"Pattern 1 matches (#aistats25...moment.tz): {len(matches1)}")
if matches1:
    print(f"First match (truncated): {matches1[0][:200]}")

# Try the full pattern
deadline_pattern = re.compile(
    r'\$\([\'"]#(\w+).*?moment\.tz\([\'"]([^\'\"]+)[\'"]\s*,\s*[\'"]([^\'\"]+)[\'\"]\)',
    re.DOTALL
)

matches2 = list(deadline_pattern.finditer(html))
print(f"\nFull pattern matches: {len(matches2)}")
if matches2:
    print("First 5 matches:")
    for i, match in enumerate(matches2[:5]):
        print(f"  {i+1}. {match.group(1)}: {match.group(2)} [{match.group(3)}]")
else:
    # Try simpler pattern
    simple_pattern = re.compile(r'moment\.tz\("([^"]+)"\s*,\s*"([^"]+)"\)')
    simple_matches = list(simple_pattern.finditer(html))
    print(f"\nSimpler pattern (moment.tz only) matches: {len(simple_matches)}")
    if simple_matches:
        print("First 5:")
        for i, match in enumerate(simple_matches[:5]):
            print(f"  {i+1}. {match.group(1)} [{match.group(2)}]")
