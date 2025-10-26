"""Test the enhanced AI Deadlines scraper with deadline extraction."""
from confradar.scrapers.ai_deadlines import AIDeadlinesScraper
import json

scraper = AIDeadlinesScraper()
result = scraper.scrape()

print(f'Found {len(result.normalized)} conferences')

confs_with_deadlines = [c for c in result.normalized if c['deadlines']]
print(f'Conferences with deadlines: {len(confs_with_deadlines)}')

if confs_with_deadlines:
    print('\nSample conferences with deadlines:')
    for conf in confs_with_deadlines[:5]:
        print(f"\n{conf['name']} ({conf['key']}):")
        print(f"  Year: {conf['year']}")
        print(f"  Homepage: {conf['homepage']}")
        for deadline in conf['deadlines']:
            print(f"  Deadline ({deadline['kind']}): {deadline['due_at']} [{deadline['timezone']}]")
else:
    print('\nNo conferences with deadlines found')
    print('\nSample conference without deadline:')
    print(json.dumps(result.normalized[0] if result.normalized else {}, indent=2))
