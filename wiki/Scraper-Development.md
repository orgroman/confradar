# Scraper Development Guide

This guide explains how to develop new scrapers for ConfRadar using Scrapy.

## Architecture Overview

ConfRadar uses **Scrapy** as the scraping framework, providing:
- Built-in rate limiting and retries
- HTTP caching for development
- Item pipelines for validation and storage
- Middleware system for customization
- Robust error handling

## Project Structure

```
confradar/scrapers/
├── settings.py          # Scrapy project settings
├── items.py            # Item definitions (ConferenceItem)
├── pipelines.py        # Validation, deduplication, DB storage
└── spiders/            # Individual spiders
    ├── ai_deadlines.py
    ├── acl_web.py
    ├── chairing_tool.py
    └── ...
```

## Creating a New Spider

### 1. Basic Spider Template

```python
"""Spider for [source name]."""
from datetime import datetime, timezone
from typing import Iterator
import re

import scrapy
from scrapy.http import Response

from confradar.scrapers.items import ConferenceItem


class MySourceSpider(scrapy.Spider):
    """Scrape conferences from [source].
    
    Usage:
        scrapy crawl my_source -o conferences.json
    """
    
    name = "my_source"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com/conferences"]
    
    custom_settings = {
        "DOWNLOAD_DELAY": 2,  # Be respectful
    }
    
    def parse(self, response: Response) -> Iterator[ConferenceItem]:
        """Parse the main page."""
        self.logger.info(f"Parsing {response.url}")
        
        # Extract conference data using CSS or XPath selectors
        for conf in response.css('.conference-item'):
            yield ConferenceItem(
                key=self._extract_key(conf),
                name=conf.css('.name::text').get('').strip(),
                year=self._extract_year(conf),
                homepage=conf.css('a.website::attr(href)').get(),
                deadlines=[],
                source=self.name,
                scraped_at=datetime.now(timezone.utc).isoformat(),
                url=response.url,
            )
```

### 2. Working with Different HTML Structures

**CSS Selectors (Recommended for simple structures):**
```python
# Get text
name = response.css('.conference-name::text').get()

# Get attribute
url = response.css('a.link::attr(href)').get()

# Get all matching elements
conferences = response.css('.conference-item')

# Complex selector
deadline = response.css('div.dates span.submission::text').get()
```

**XPath (For complex navigation):**
```python
# Find element by text content
link = response.xpath('//a[contains(text(), "Conference")]/@href').get()

# Navigate parent/sibling
name = response.xpath('//div[@class="deadline"]/../h2/text()').get()

# Multiple conditions
items = response.xpath('//div[@class="item" and @data-type="conference"]')
```

### 3. Handling Pagination

```python
def parse(self, response: Response) -> Iterator[ConferenceItem]:
    # Extract items from current page
    for item in self.parse_page(response):
        yield item
    
    # Follow pagination link
    next_page = response.css('a.next::attr(href)').get()
    if next_page:
        yield response.follow(next_page, callback=self.parse)
```

### 4. Following Links

```python
def parse(self, response: Response) -> Iterator[scrapy.Request]:
    """Parse listing page, follow detail links."""
    for link in response.css('.conference-link::attr(href)').getall():
        yield response.follow(link, callback=self.parse_detail)

def parse_detail(self, response: Response) -> Iterator[ConferenceItem]:
    """Parse individual conference page."""
    yield ConferenceItem(
        key=self._extract_key(response),
        name=response.css('h1::text').get(),
        # ... extract more details
    )
```

### 5. Handling JavaScript-Heavy Sites

For sites requiring JS execution, enable Playwright:

```python
class MyJSSpider(scrapy.Spider):
    name = "my_js_source"
    
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://example.com",
            meta={"playwright": True, "playwright_include_page": True}
        )
```

### 6. Using LLM for Structured Extraction

For complex, unstructured sources:

```python
from confradar.llm.openai import OpenAIClient

class LLMSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.llm = OpenAIClient()
    
    def parse(self, response: Response) -> Iterator[ConferenceItem]:
        # Extract text content
        text = ' '.join(response.css('body *::text').getall())
        
        # Use LLM to extract structured data
        prompt = f"""Extract conference information from this text:
        - Conference name
        - Key deadlines (submission, notification, camera-ready)
        - Location and dates
        
        Text: {text[:2000]}
        
        Return JSON with keys: name, deadlines, location, dates
        """
        
        result = self.llm.complete(prompt, response_format="json_object")
        # Parse and yield ConferenceItem
```

## Item Pipelines

Pipelines process scraped items in order. Current pipelines:

### ValidationPipeline (Priority 100)
Validates required fields (key, name, deadlines list).

### DeduplicationPipeline (Priority 200)
Removes duplicate conferences within a scraping session.

### DatabasePipeline (Priority 300) - Future
Stores conferences in database using SQLAlchemy models.

**Custom Pipeline Example:**
```python
class MyCustomPipeline:
    def process_item(self, item, spider):
        # Transform or validate item
        item['name'] = item['name'].upper()
        return item
    
    def open_spider(self, spider):
        # Setup (e.g., open DB connection)
        pass
    
    def close_spider(self, spider):
        # Cleanup
        pass
```

Enable in `settings.py`:
```python
ITEM_PIPELINES = {
    'confradar.scrapers.pipelines.ValidationPipeline': 100,
    'confradar.scrapers.pipelines.MyCustomPipeline': 150,
    'confradar.scrapers.pipelines.DeduplicationPipeline': 200,
}
```

## Testing Scrapers

### Unit Tests (Mock Responses)

```python
from scrapy.http import HtmlResponse, Request

def test_spider_parse():
    spider = MySourceSpider()
    
    # Create fake response
    html = b"""<html>
        <div class="conference">
            <h2>ICML 2025</h2>
        </div>
    </html>"""
    
    response = HtmlResponse(
        url="https://example.com",
        request=Request(url="https://example.com"),
        body=html,
    )
    
    items = list(spider.parse(response))
    assert len(items) > 0
    assert items[0]['name'] == 'ICML 2025'
```

### Integration Tests (Real HTTP)

```python
import pytest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

@pytest.mark.integration
def test_spider_real():
    collected_items = []
    
    def collect_item(item, response, spider):
        collected_items.append(dict(item))
    
    settings = get_project_settings()
    settings.set('HTTPCACHE_ENABLED', False)
    
    process = CrawlerProcess(settings)
    
    from scrapy import signals
    from scrapy.signalmanager import dispatcher
    dispatcher.connect(collect_item, signal=signals.item_scraped)
    
    process.crawl(MySourceSpider)
    process.start()
    
    assert len(collected_items) > 0
    print(f"✓ Scraped {len(collected_items)} conferences")
```

Run integration tests:
```bash
uv run pytest -m integration -v
```

## Running Spiders

### Command Line

```bash
# Basic scraping
scrapy crawl ai_deadlines

# Output to JSON
scrapy crawl ai_deadlines -o conferences.json

# Output to CSV
scrapy crawl ai_deadlines -o conferences.csv

# Multiple spiders
scrapy crawl ai_deadlines -o ai.json
scrapy crawl acl_web -o acl.json
```

### From Python

```python
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from confradar.scrapers.spiders.ai_deadlines import AIDeadlinesSpider

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(AIDeadlinesSpider)
process.start()  # Blocks until finished
```

## Dagster Integration

Each spider becomes a Dagster asset:

```python
from dagster import asset
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

@asset
def ai_deadlines_conferences() -> list[dict]:
    """Scrape AI Deadlines conferences."""
    collected = []
    
    def collect_item(item, response, spider):
        collected.append(dict(item))
    
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    
    from scrapy import signals
    from scrapy.signalmanager import dispatcher
    dispatcher.connect(collect_item, signal=signals.item_scraped)
    
    process.crawl('ai_deadlines')  # Spider name
    process.start()
    
    return collected

@asset
def merged_conferences(
    ai_deadlines_conferences: list[dict],
    acl_web_conferences: list[dict],
) -> list[dict]:
    """Merge and deduplicate conferences from multiple sources."""
    all_confs = ai_deadlines_conferences + acl_web_conferences
    # Dedupe by (name, year) tuple
    seen = set()
    unique = []
    for conf in all_confs:
        key = (conf['name'], conf.get('year'))
        if key not in seen:
            seen.add(key)
            unique.append(conf)
    return unique
```

## Best Practices

### 1. Be Respectful
- Use appropriate `DOWNLOAD_DELAY` (1-3 seconds)
- Respect `robots.txt` (enabled by default)
- Enable `AUTOTHROTTLE` for adaptive delays
- Use HTTP caching during development

### 2. Handle Errors Gracefully
```python
def parse(self, response: Response):
    try:
        name = response.css('.name::text').get()
        if not name:
            self.logger.warning(f"No name found at {response.url}")
            return
        
        yield ConferenceItem(name=name, ...)
    except Exception as e:
        self.logger.error(f"Failed to parse {response.url}: {e}")
```

### 3. Log Useful Information
```python
self.logger.info(f"Found {len(items)} conferences")
self.logger.warning(f"Missing deadline for {conf_name}")
self.logger.error(f"Failed to parse date: {date_str}")
```

### 4. Make Extractors Reusable
```python
class MySpider(scrapy.Spider):
    def _extract_year(self, text: str) -> int | None:
        """Extract 4-digit year from text."""
        match = re.search(r'\b(20\d{2})\b', text)
        return int(match.group(1)) if match else None
    
    def _extract_key(self, name: str, year: int | None) -> str:
        """Generate conference key from name and year."""
        slug = re.sub(r'[^a-z0-9]+', '', name.lower())
        if year:
            slug += str(year)[-2:]  # Last 2 digits
        return slug
```

## Debugging Tips

### 1. Scrapy Shell
```bash
scrapy shell "https://example.com"
```

Then interactively test selectors:
```python
>>> response.css('.conference-name::text').getall()
>>> response.xpath('//div[@class="item"]').getall()
```

### 2. Enable Debug Logging
```python
custom_settings = {
    'LOG_LEVEL': 'DEBUG',
}
```

### 3. Save Response for Analysis
```python
def parse(self, response):
    # Save HTML for inspection
    with open('debug.html', 'wb') as f:
        f.write(response.body)
```

## Example: AI Deadlines Scraper (Complete Implementation)

The AI Deadlines scraper demonstrates parsing JavaScript-embedded data and database integration.

### Challenge: JavaScript-Embedded Deadlines

The aideadlines.org site embeds deadline information in JavaScript rather than static HTML:

```javascript
$('#icml25 .ML-tag').html('ml');
var timezone = "UTC-12";
var confDate = moment.tz("2024-05-15 23:59:59", timezone);
```

### Solution: Regex Parsing of Script Blocks

```python
def parse(self, response: Response) -> Iterator[ConferenceItem]:
    # First, extract all conference entries
    conferences = {}
    
    for link in response.css('a[href*="/conference?id="]'):
        key = re.search(r'id=([^&]+)', link.attrib.get('href', '')).group(1)
        if key not in conferences:
            conferences[key] = {
                'key': key,
                'name': link.css('::text').get('').strip(),
                'year': self._extract_year(key),
                'homepage': self._find_homepage(link),
                'deadlines': []
            }
    
    # Then extract deadlines from JavaScript
    for script_text in response.xpath('//script/text()').getall():
        # Pattern: $('#confkey') ... var timezone = "..."; moment.tz("date", timezone)
        pattern = re.compile(
            r'\$\([\'"]#(\w+).*?var\s+timezone\s*=\s*[\'"]([^\'\"]+)[\'"]'
            r'.*?moment\.tz\([\'"]([^\'\"]+)[\'"]',
            re.DOTALL
        )
        
        for match in pattern.finditer(script_text):
            conf_key, timezone_str, deadline_str = match.groups()
            
            if conf_key in conferences:
                try:
                    # Handle both "YYYY-MM-DD HH:MM:SS" and "YYYY-MM-DD HH:MM"
                    try:
                        dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
                    
                    conferences[conf_key]['deadlines'].append({
                        'kind': 'submission',
                        'due_at': dt.isoformat(),
                        'timezone': timezone_str
                    })
                except ValueError:
                    continue
    
    # Yield items
    for conf_data in conferences.values():
        yield ConferenceItem(**conf_data, source=self.name, ...)
```

### Database Integration

The `DatabasePipeline` stores scraped data in PostgreSQL:

```python
class DatabasePipeline:
    """Store conferences in PostgreSQL database."""
    
    def open_spider(self, spider):
        from confradar.db.base import get_session
        self.session = get_session()
    
    def close_spider(self, spider):
        if self.session:
            self.session.close()
    
    def process_item(self, item: dict, spider):
        from confradar.db.models import Conference, Source, Deadline
        
        # Find or create conference
        conference = self.session.query(Conference).filter_by(
            key=item['key']
        ).first()
        
        if not conference:
            conference = Conference(
                key=item['key'],
                name=item['name'],
                homepage=item.get('homepage')
            )
            self.session.add(conference)
            self.session.flush()
        else:
            # Update existing
            conference.name = item['name']
            if item.get('homepage'):
                conference.homepage = item['homepage']
        
        # Create source
        source = Source(
            conference_id=conference.id,
            url=item.get('url', ''),
            notes=f"Scraped by {item.get('source')} on {item.get('scraped_at')}"
        )
        self.session.add(source)
        self.session.flush()
        
        # Create deadlines
        for deadline_data in item.get('deadlines', []):
            due_date = datetime.fromisoformat(deadline_data['due_at'])
            
            deadline = Deadline(
                conference_id=conference.id,
                kind=deadline_data['kind'],
                due_date=due_date,
                timezone=deadline_data.get('timezone'),
                source_id=source.id
            )
            self.session.add(deadline)
        
        self.session.commit()
        return item
```

### Running the Full Pipeline

```bash
# Make sure PostgreSQL is running
docker compose up postgres -d

# Run scraper (stores in database)
cd packages/confradar
uv run scrapy crawl ai_deadlines

# Check results in database
docker compose exec postgres psql -U confradar -d confradar -c "
  SELECT c.name, c.homepage, COUNT(d.id) as deadline_count
  FROM conferences c
  LEFT JOIN deadlines d ON d.conference_id = c.id
  GROUP BY c.id
  ORDER BY c.name
  LIMIT 10;
"
```

### Testing Strategy

**Unit Tests** (`tests/test_ai_deadlines_scraper.py`):
- Parse basic conference HTML
- Extract deadlines from JavaScript
- Handle different date formats
- Deduplicate conferences
- Validate year extraction

**Integration Tests** (`tests/test_database_pipeline.py`):
- Create new conferences in database
- Update existing conferences
- Store multiple deadlines
- Prevent duplicate deadlines
- Handle invalid data gracefully

**Coverage**: 94% for scraper, 92% for pipeline

### Key Learnings

1. **JavaScript Parsing**: Use regex for simple JS patterns; consider Playwright for complex JS
2. **Deduplication**: Use dict with conference key to avoid duplicates during parsing
3. **Database Upserts**: Check if conference exists, update or create as needed
4. **Transaction Safety**: Use try/except with rollback for database errors
5. **Timezone Handling**: Store timezone string (e.g., "UTC-12") alongside datetime

## Example Spiders

See existing spiders in `src/confradar/scrapers/spiders/`:
- `ai_deadlines.py` - ✅ **Complete**: JavaScript parsing + database integration
- `acl_web.py` - Table parsing (WIP)
- `chairing_tool.py` - Complex navigation (WIP)
- `elra.py` - Multi-page scraping (WIP)

## Next Steps

1. **Create your spider** following the template
2. **Add unit tests** with mocked responses (see `test_ai_deadlines_scraper.py`)
3. **Add integration tests** for database (see `test_database_pipeline.py`)
4. **Test locally**: `scrapy crawl your_spider`
5. **Verify database**: Check data in pgAdmin or psql
6. **Create Dagster asset** once spider is stable

