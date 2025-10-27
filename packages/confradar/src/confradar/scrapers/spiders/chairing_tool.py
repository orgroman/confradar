"""Spider for ChairingTool conferences.

Scrapes conference listings from ChairingTool platform.
"""

import re
from collections.abc import Iterator
from datetime import datetime, timezone

import scrapy
from scrapy.http import Response

from confradar.scrapers.items import ConferenceItem


class ChairingToolSpider(scrapy.Spider):
    """Scrape conferences from ChairingTool.

    Source: https://chairingtool.com/conferences

    Usage:
        scrapy crawl chairing_tool -o chairing_conferences.json
    """

    name = "chairing_tool"
    allowed_domains = ["chairingtool.com"]
    start_urls = ["https://chairingtool.com/conferences"]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }

    def parse(self, response: Response) -> Iterator[ConferenceItem]:
        """Parse ChairingTool conferences page."""
        self.logger.info(f"Parsing {response.url}")

        # ChairingTool typically lists conferences in cards or table rows
        for conf in response.css(".conference-card, .conference-item, tr.conference"):
            name = conf.css(".name::text, .title::text, td.name::text, h3::text").get("")
            if not name:
                continue

            name = name.strip()

            # Extract year
            year = self._extract_year(name)
            if not year:
                date_text = conf.css(".date::text, .year::text, td.date::text").get("")
                year = self._extract_year(date_text)

            # Extract homepage
            homepage = conf.css('a.website::attr(href), a[href*="http"]::attr(href)').get()
            if homepage and "chairingtool.com" in homepage:
                homepage = None  # Skip internal links

            # Generate key
            key = self._generate_key(name, year)

            if key and name:
                yield ConferenceItem(
                    key=key,
                    name=name,
                    year=year,
                    homepage=homepage,
                    deadlines=[],
                    source=self.name,
                    scraped_at=datetime.now(timezone.utc).isoformat(),
                    url=response.url,
                )
                self.logger.debug(f"Found: {name}")

        # Handle pagination if exists
        next_page = response.css('a.next::attr(href), a[rel="next"]::attr(href)').get()
        if next_page:
            self.logger.info(f"Following next page: {next_page}")
            yield response.follow(next_page, callback=self.parse)

        self.logger.info(f"Finished parsing {response.url}")

    def _extract_year(self, text: str) -> int | None:
        """Extract 4-digit year from text."""
        if not text:
            return None
        match = re.search(r"\b(20\d{2})\b", text)
        return int(match.group(1)) if match else None

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
