"""Quick script to explore AI Deadlines HTML structure."""
import httpx
from bs4 import BeautifulSoup
import json

# Fetch the page
url = "https://aideadlin.es/?sub=NLP"
print(f"Fetching {url}...")
with httpx.Client(timeout=20.0, follow_redirects=True) as client:
    resp = client.get(url)
    resp.raise_for_status()
    html = resp.text

# Parse with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Save raw HTML for inspection
with open("ai_deadlines_page.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Saved HTML to ai_deadlines_page.html")

# Look for conference entries
print("\n=== Looking for conference links ===")
conf_links = soup.find_all('a', href=lambda h: h and '/conference?id=' in h)
print(f"Found {len(conf_links)} conference links")

if conf_links:
    # Examine first few entries
    for i, link in enumerate(conf_links[:5]):
        print(f"\n--- Conference {i+1} ---")
        print(f"Link: {link.get('href')}")
        print(f"Text: {link.get_text(strip=True)}")
        
        # Look at parent element
        parent = link.parent
        if parent:
            print(f"Parent tag: {parent.name}")
            print(f"Parent classes: {parent.get('class', [])}")
            
            # Look for siblings/nearby elements
            print("\nSiblings:")
            for sibling in parent.find_all(recursive=False):
                print(f"  - {sibling.name}: {sibling.get('class', [])} = {sibling.get_text(strip=True)[:80]}")

# Look for deadline-related elements
print("\n=== Looking for deadline patterns ===")
deadline_keywords = ['deadline', 'submission', 'abstract', 'notification', 'camera']
for keyword in deadline_keywords:
    elements = soup.find_all(string=lambda t: t and keyword.lower() in t.lower())
    print(f"\n'{keyword}' appears in {len(elements)} elements")
    if elements:
        for elem in elements[:3]:
            parent = elem.parent
            print(f"  - {parent.name} [{parent.get('class', [])}]: {elem.strip()[:100]}")

print("\n=== Done ===")
