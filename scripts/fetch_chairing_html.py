"""Simple script to fetch ChairingTool HTML for inspection."""

import requests

url = "https://chairingtool.com/conferences"
headers = {
    "User-Agent": "confradar (+https://github.com/orgroman/confradar)"
}

print(f"Fetching {url}...")
response = requests.get(url, headers=headers, timeout=30)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)} chars")

# Save to file
output_file = "chairing_tool_sample.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"\nSaved HTML to: {output_file}")

# Print first 3000 chars
print("\n" + "=" * 80)
print("FIRST 3000 CHARS OF HTML:")
print("=" * 80)
print(response.text[:3000])

# Look for patterns
print("\n" + "=" * 80)
print("SEARCHING FOR KEY PATTERNS:")
print("=" * 80)

text = response.text.lower()
if "deadline" in text:
    print("✓ Found 'deadline' in HTML")
else:
    print("✗ No 'deadline' found")

if "submission" in text:
    print("✓ Found 'submission' in HTML")
else:
    print("✗ No 'submission' found")

if "conference" in text:
    print("✓ Found 'conference' in HTML")
else:
    print("✗ No 'conference' found")

if "moment.tz" in text or "moment(" in text:
    print("✓ Found moment.js usage (JavaScript dates)")
else:
    print("✗ No moment.js found")

print("\nDone. Check", output_file, "for full HTML.")
