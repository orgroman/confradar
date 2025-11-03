"""Check if ChairingTool has a REST API we can use instead of Playwright."""

import requests
import json

base_url = "https://chairingtool.com"
headers = {
    "User-Agent": "confradar (+https://github.com/orgroman/confradar)"
}

print("Checking potential API endpoints...")
print("=" * 80)

# Try common API patterns
api_urls_to_try = [
    f"{base_url}/api/conferences",
    f"{base_url}/api/v1/conferences",
    f"{base_url}/conferences/api",
    f"{base_url}/data/conferences",
    f"{base_url}/conferences.json",
]

for url in api_urls_to_try:
    try:
        print(f"\nTrying: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            print(f"Content-Type: {content_type}")
            
            if "json" in content_type.lower():
                try:
                    data = response.json()
                    print(f"✓ Found JSON API!")
                    print(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'array'}")
                    print(f"Sample (first 500 chars): {json.dumps(data, indent=2)[:500]}")
                    break
                except json.JSONDecodeError:
                    print("✗ Not valid JSON")
            else:
                print(f"Response length: {len(response.text)} chars")
                print(f"First 200 chars: {response.text[:200]}")
    except requests.RequestException as e:
        print(f"✗ Error: {e}")

print("\n" + "=" * 80)
print("\nConclusion: Need to use Playwright if no API found")
