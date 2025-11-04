"""Spider for ChairingTool conferences.

Scrapes conference listings from ChairingTool platform.
ChairingTool is a React SPA that requires JavaScript rendering via Playwright.

Parsing Strategy:
- Use Playwright to render the React application
- Extract conference cards from the dynamically loaded DOM
- Follow detail pages if deadlines require it
- Handle pagination if present

Deadline Handling:
- Extract submission, notification, and camera-ready deadlines
- Parse dates and timezones
- Normalize to ISO format for database storage
"""

import re
from collections.abc import AsyncGenerator
from datetime import datetime, timezone

import scrapy
from scrapy.http import Request, Response

from confradar.scrapers.items import ConferenceItem


class ChairingToolSpider(scrapy.Spider):
    """Scrape conferences from ChairingTool using Playwright for JS rendering.

    Source: https://chairingtool.com/conferences

    Usage:
        scrapy crawl chairing_tool -o chairing_conferences.json
    """

    name = "chairing_tool"
    allowed_domains = ["chairingtool.com"]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ITEM_PIPELINES": {
            "confradar.scrapers.pipelines.ValidationPipeline": 100,
            "confradar.scrapers.pipelines.DeduplicationPipeline": 200,
            "confradar.scrapers.pipelines.DatabasePipeline": 300,
        },
    }

    def start_requests(self):
        """Generate initial requests with Playwright enabled."""
        yield scrapy.Request(
            url="https://chairingtool.com/conferences",
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_goto_kwargs": {
                    "wait_until": "networkidle",
                    "timeout": 60000,  # 60 seconds
                },
                # Disable cache for Playwright requests
                "dont_cache": True,
            },
            callback=self.parse,
            errback=self.errback_close_page,
            dont_filter=True,  # Allow re-crawling
        )

    async def errback_close_page(self, failure):
        """Close Playwright page on error to avoid resource leaks."""
        page = failure.request.meta.get("playwright_page")
        if page:
            await page.close()
        self.logger.error(f"Request failed: {failure}")

    async def parse(self, response: Response) -> AsyncGenerator[ConferenceItem | Request, None]:
        """Parse ChairingTool conferences page after JavaScript rendering."""
        page = response.meta.get("playwright_page")
        
        if not page:
            self.logger.error("Playwright page not available in response meta")
            return
        
        try:
            self.logger.info(f"Parsing {response.url} with Playwright")
            
            # Wait a bit more for React to render if needed
            await page.wait_for_timeout(2000)
            
            # Get the rendered HTML
            content = await page.content()
            
            # Create a new response with the rendered HTML for parsing
            from scrapy.http import HtmlResponse
            rendered_response = HtmlResponse(
                url=response.url,
                body=content.encode('utf-8'),
                encoding='utf-8',
            )
            
            # Try to find conference containers - adjust selectors based on actual HTML
            # Common patterns for conference listings
            selectors_to_try = [
                ".conference-card",
                ".conference-item",
                "tr.conference",
                ".event-card",
                "[class*='Conference']",
                "[class*='conference']",
                "[data-testid*='conference']",
                "article",
                ".card",
            ]
            
            conferences_found = []
            for selector in selectors_to_try:
                conferences = rendered_response.css(selector)
                if conferences:
                    self.logger.info(f"Found {len(conferences)} conferences using selector: {selector}")
                    conferences_found = conferences
                    break
            
            if not conferences_found:
                # Log the page structure to help debug
                self.logger.warning("No conferences found with known selectors")
                self.logger.debug(f"Page title: {rendered_response.css('title::text').get()}")
                self.logger.debug(f"Body classes: {rendered_response.css('body::attr(class)').get()}")
                
                # Save HTML for manual inspection (only if debug logging enabled)
                if self.settings.get('LOG_LEVEL') == 'DEBUG':
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', prefix='chairing_tool_', 
                                                      delete=False, encoding='utf-8') as f:
                        f.write(content)
                        self.logger.info(f"Saved rendered HTML to {f.name} for inspection")
            
            for conf in conferences_found:
                # Extract basic info - adjust selectors based on actual structure
                name = self._extract_name(conf)
                if not name:
                    continue

                year = self._extract_year(conf, name)
                homepage = self._extract_homepage(conf)
                deadlines = self._extract_deadlines(conf)

                # Generate key
                key = self._generate_key(name, year)

                if key and name:
                    yield ConferenceItem(
                        key=key,
                        name=name,
                        year=year,
                        homepage=homepage,
                        deadlines=deadlines,
                        source=self.name,
                        scraped_at=datetime.now(timezone.utc).isoformat(),
                        url=response.url,
                    )
                    self.logger.debug(f"Found: {name} with {len(deadlines)} deadlines")

            # Handle pagination if exists
            next_page = rendered_response.css('a.next::attr(href), a[rel="next"]::attr(href)').get()
            if next_page:
                self.logger.info(f"Following next page: {next_page}")
                yield response.follow(
                    next_page,
                    callback=self.parse,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "playwright_page_goto_kwargs": {"wait_until": "networkidle"},
                    },
                    errback=self.errback_close_page,
                )

            self.logger.info(f"Finished parsing {response.url}")
            
        finally:
            # Always close the Playwright page
            if page:
                await page.close()

    def _extract_name(self, conf) -> str:
        """Extract conference name from various possible locations."""
        # Try common selectors
        name_selectors = [
            ".name::text",
            ".title::text",
            "h1::text",
            "h2::text",
            "h3::text",
            "h4::text",
            ".conference-name::text",
            "[class*='title']::text",
            "[class*='name']::text",
        ]
        
        for selector in name_selectors:
            name = conf.css(selector).get()
            if name:
                return name.strip()
        
        return ""

    def _extract_homepage(self, conf) -> str | None:
        """Extract conference homepage URL."""
        # Look for external links
        homepage_selectors = [
            'a.website::attr(href)',
            'a.homepage::attr(href)',
            'a[href*="http"]::attr(href)',
            '[class*="website"] a::attr(href)',
        ]
        
        for selector in homepage_selectors:
            homepage = conf.css(selector).get()
            if homepage and "chairingtool.com" not in homepage:
                return homepage
        
        return None

    def _extract_deadlines(self, conf) -> list[dict]:
        """Extract deadline information from conference element."""
        deadlines = []
        
        # Try to find deadline elements
        deadline_elements = conf.css('.deadline, .date, [class*="deadline"], [class*="date"]')
        
        for deadline_el in deadline_elements:
            # Extract deadline text
            text = ' '.join(deadline_el.css('::text').getall()).strip()
            if not text:
                continue
            
            # Try to determine deadline type
            kind = "submission"  # default
            text_lower = text.lower()
            if "abstract" in text_lower:
                kind = "abstract"
            elif "notification" in text_lower or "notify" in text_lower:
                kind = "notification"
            elif "camera" in text_lower or "final" in text_lower:
                kind = "camera-ready"
            
            # Try to extract date
            date_match = re.search(r'\b(\d{4})-(\d{2})-(\d{2})\b', text)
            if date_match:
                try:
                    year, month, day = date_match.groups()
                    dt = datetime(int(year), int(month), int(day), 23, 59, 59)
                    
                    # Try to extract timezone
                    tz_match = re.search(r'\b(UTC|GMT|AoE|PST|EST|CST)\b', text, re.IGNORECASE)
                    timezone_str = tz_match.group(1) if tz_match else "UTC"
                    
                    deadlines.append({
                        "kind": kind,
                        "due_at": dt.isoformat(),
                        "timezone": timezone_str,
                    })
                except (ValueError, IndexError):
                    continue
            else:
                # Try other date formats
                # TODO: Use dateparser for more flexible date parsing
                pass
        
        return deadlines

    def _extract_year(self, conf, name: str) -> int | None:
        """Extract 4-digit year from conference element or name."""
        # First try the name
        match = re.search(r"\b(20\d{2})\b", name)
        if match:
            return int(match.group(1))
        
        # Then try to find year in date fields
        date_selectors = [
            ".date::text",
            ".year::text",
            "[class*='date']::text",
            "[class*='year']::text",
        ]
        
        for selector in date_selectors:
            date_text = conf.css(selector).get()
            if date_text:
                match = re.search(r"\b(20\d{2})\b", date_text)
                if match:
                    return int(match.group(1))
        
        return None

    def _generate_key(self, name: str, year: int | None) -> str:
        """Generate conference key from name and year."""
        # Extract acronym
        acronym = re.findall(r"[A-Z0-9]+", name)
        if acronym:
            key = acronym[0].lower()
        else:
            words = re.findall(r"\w+", name)
            key = words[0].lower() if words else "unknown"

        if year:
            key += str(year)[-2:]

        return key
