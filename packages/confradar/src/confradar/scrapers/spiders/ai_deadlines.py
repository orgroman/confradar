"""Spider for aideadlines.org website."""

import re
from collections.abc import Iterator
from datetime import datetime, timezone
from typing import Any

import scrapy
from scrapy.http import Response

from confradar.scrapers.items import ConferenceItem


class AIDeadlinesSpider(scrapy.Spider):
    """Scrape conference deadlines from aideadlines.org (NLP focus).

    Source: https://aideadlines.org/?sub=NLP

    This spider parses the HTML structure to extract conference information.
    The site structure may change, requiring updates to the parsing logic.

    Usage:
        scrapy crawl ai_deadlines -o conferences.json
    """

    name = "ai_deadlines"
    allowed_domains = ["aideadlines.org"]
    start_urls = ["https://aideadlines.org/?sub=NLP"]

    custom_settings = {
        # Override default delay for this specific spider
        "DOWNLOAD_DELAY": 2,
    }

    def parse(self, response: Response) -> Iterator[ConferenceItem]:
        """Parse the main page and extract conference information.

        Args:
            response: Scrapy response object

        Yields:
            ConferenceItem objects
        """
        self.logger.info(f"Parsing {response.url}")

        # Build a dict of conferences first to avoid duplicates
        conferences = {}

        # Find all conference links
        conference_links = response.css('a[href*="/conference?id="]')

        for link in conference_links:
            try:
                # Extract conference ID from link
                href = link.attrib.get("href", "")
                conf_match = re.search(r"id=([^&]+)", href)
                if not conf_match:
                    continue

                key = conf_match.group(1)

                # Skip if we already have this conference
                if key in conferences:
                    continue

                name = link.css("::text").get("").strip()

                if not name:
                    continue

                # Extract year from key if present (e.g., 'icml25' -> 2025)
                year = self._extract_year(key)

                # Try to find homepage link nearby
                homepage = self._find_homepage(link)

                conferences[key] = {
                    "key": key,
                    "name": name,
                    "year": year,
                    "homepage": homepage,
                    "deadlines": [],
                }

            except Exception as e:
                self.logger.warning(f"Failed to parse conference link: {e}")
                continue

        # Extract deadlines from JavaScript
        script_tags = response.xpath("//script/text()").getall()
        for script_text in script_tags:
            if not script_text:
                continue

            # Find conference deadline blocks
            # Pattern: $('#confkey') ... var timezone = "..."; moment.tz("date", timezone)
            conf_block_pattern = re.compile(
                r'\$\([\'"]#(\w+).*?var\s+timezone\s*=\s*[\'"]([^\'\"]+)[\'"].*?moment\.tz\([\'"]([^\'\"]+)[\'"]',
                re.DOTALL,
            )

            for match in conf_block_pattern.finditer(script_text):
                conf_key = match.group(1)
                timezone_str = match.group(2)
                deadline_str = match.group(3)

                # Skip if not a conference we're tracking
                if conf_key not in conferences:
                    continue

                # Parse deadline (handle with/without seconds)
                try:
                    try:
                        deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

                    conferences[conf_key]["deadlines"].append(
                        {
                            "kind": "submission",
                            "due_at": deadline_dt.isoformat(),
                            "timezone": timezone_str,
                        }
                    )
                except ValueError:
                    # Skip invalid dates
                    continue

        # Yield conference items
        for conf_data in conferences.values():
            item = ConferenceItem(
                key=conf_data["key"],
                name=conf_data["name"],
                year=conf_data["year"],
                homepage=conf_data["homepage"],
                deadlines=conf_data["deadlines"],
                source="aideadlines",
                scraped_at=datetime.now(timezone.utc).isoformat(),
                url=response.url,
            )

            yield item

    def _extract_year(self, key: str) -> int | None:
        """Extract year from conference key.

        Args:
            key: Conference key like 'icml25'

        Returns:
            Year as integer, or None if not found
        """
        year_match = re.search(r"(\d{2})$", key)
        if year_match:
            yr = int(year_match.group(1))
            # Assume 00-49 is 2000-2049, 50-99 is 1950-1999
            return 2000 + yr if yr < 50 else 1900 + yr
        return None

    def _find_homepage(self, link_selector: Any) -> str | None:
        """Find the homepage URL near the conference link.

        Args:
            link_selector: Scrapy selector for the conference link

        Returns:
            Homepage URL or None
        """
        # Try to find a nearby external link (conference website)
        parent = link_selector.xpath("..")
        if parent:
            website_link = parent.xpath('.//a[starts-with(@href, "http")]/@href').get()
            if website_link and "aideadlin.es" not in website_link:
                return website_link
        return None
