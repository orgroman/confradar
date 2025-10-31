"""Spider for WikiCFP.

Scrapes conference calls for papers from WikiCFP.
"""

import re
from collections.abc import Iterator
from datetime import datetime, timezone

import scrapy
from scrapy.http import Request, Response

from confradar.scrapers.items import ConferenceItem


class WikiCFPSpider(scrapy.Spider):
    """Scrape conferences from WikiCFP.

    Source: http://www.wikicfp.com/cfp/

    Usage:
        scrapy crawl wikicfp -o wikicfp_conferences.json

    Can filter by category:
        scrapy crawl wikicfp -a category="natural language processing"
    """

    name = "wikicfp"
    allowed_domains = ["wikicfp.com"]

    def __init__(self, category: str | None = None, *args, **kwargs):
        """Initialize spider.

        Args:
            category: Optional category filter (e.g., "natural language processing")
        """
        super().__init__(*args, **kwargs)
        self.category = category

        if category:
            # Search for specific category
            self.start_urls = [
                f"http://www.wikicfp.com/cfp/call?conference={category.replace(' ', '+')}"
            ]
        else:
            # Get recent conferences
            self.start_urls = ["http://www.wikicfp.com/cfp/home"]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }

    def parse(self, response: Response) -> Iterator[ConferenceItem | Request]:
        """Parse WikiCFP page."""
        self.logger.info(f"Parsing {response.url}")

        # WikiCFP uses table rows for conference listings
        for row in response.css("tr.contsec, tr.cfp"):
            # Extract conference name (usually in first td or a link)
            name_elem = row.css("td a::text, td.title a::text").get()
            if not name_elem:
                continue

            name = name_elem.strip()

            # Extract year from name or dates
            year = self._extract_year(name)
            if not year:
                # Try extracting from deadline or event date columns
                date_text = " ".join(row.css("td::text").getall())
                year = self._extract_year(date_text)

            # Extract conference homepage (not WikiCFP link)
            links = row.css("td a::attr(href)").getall()
            homepage = None
            for link in links:
                if "wikicfp.com" not in link and link.startswith("http"):
                    homepage = link
                    break

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

        # Handle pagination
        next_page = response.css(
            'a:contains("Next")::attr(href), a[title="Next"]::attr(href)'
        ).get()
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
