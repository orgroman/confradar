"""Spider for ACL Web sponsored events.

Scrapes conference listings from ACL (Association for Computational Linguistics).
"""

import hashlib
import re
from collections.abc import Iterator
from datetime import datetime, timezone
from typing import Any

import scrapy
from scrapy.http import Response

from confradar.scrapers.items import ConferenceItem


class ACLWebSpider(scrapy.Spider):
    """Scrape ACL sponsored events.

    Source: https://www.aclweb.org/portal/acl_sponsored_events

    The page displays events in a table with columns:
    - Title (with link to detail page)
    - Location
    - City
    - Country
    - Submission Deadline
    - Event Dates

    Usage:
        scrapy crawl acl_web -o acl_conferences.json
    """

    name = "acl_web"
    allowed_domains = ["aclweb.org"]
    start_urls = ["https://www.aclweb.org/portal/acl_sponsored_events"]

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True,
        "HTTPCACHE_ENABLED": False,  # Disable cache to avoid 409 issues
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    }

    def start_requests(self):
        """Start requests with the required cookie."""
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                cookies={"humans_21909": "1"},
                callback=self.parse,
            )

    def parse(self, response: Response) -> Iterator[ConferenceItem]:
        """Parse ACL events page."""
        self.logger.info(f"Parsing {response.url}")

        # Find the main table
        table = response.css("table").get()
        if not table:
            self.logger.warning("No table found on page")
            return

        # Parse table rows (skip header row)
        rows = response.css("table tr")[1:]  # Skip header
        self.logger.info(f"Found {len(rows)} event rows")

        # Group deadlines by conference key to handle duplicates
        conferences_map = {}

        for row in rows:
            cells = row.css("td")
            if len(cells) < 6:
                self.logger.debug(f"Skipping row with {len(cells)} cells (need 6)")
                continue

            # Extract title and link
            title_cell = cells[0]
            # Get all text content from the cell (including nested elements)
            name = " ".join(
                title_cell.css("*::text, ::text").getall()
            ).strip()
            if not name:
                self.logger.debug("Skipping row with empty name")
                continue

            # Detail page link (may have more info)
            detail_link = title_cell.css("a::attr(href)").get()
            if detail_link and not detail_link.startswith("http"):
                detail_link = response.urljoin(detail_link)

            # Extract location info (not currently used, but available for future features)
            # location = ' '.join(cells[1].css('*::text, ::text').getall()).strip()
            # city = ' '.join(cells[2].css('*::text, ::text').getall()).strip()
            # country = ' '.join(cells[3].css('*::text, ::text').getall()).strip()

            # Extract submission deadline (column 4)
            deadline_text = " ".join(
                cells[4].css("*::text, ::text").getall()
            ).strip()

            # Extract event dates (column 5)
            event_dates_text = " ".join(
                cells[5].css("*::text, ::text").getall()
            ).strip()

            # Extract year from name or event dates
            year = self._extract_year(name)
            if not year:
                year = self._extract_year(event_dates_text)

            # Generate key
            key = self._generate_key(name, year)

            self.logger.debug(f"Processing: name={name[:50]}, year={year}, key={key}")

            # Build deadlines list
            deadlines: list[dict[str, Any]] = []

            if deadline_text:
                # Parse deadline (format: "15 May 2025" or "2 Jun 2025")
                deadline_dt = self._parse_date(deadline_text)
                if deadline_dt:
                    deadlines.append(
                        {
                            "kind": "submission",
                            "due_date": deadline_dt.date(),
                            "timezone": "AoE",  # ACL typically uses AoE
                        }
                    )

            # Try to extract homepage from location or detail link
            homepage = None
            if detail_link and "aclweb.org" in detail_link:
                # Detail page is internal; homepage might be extracted later
                homepage = None
            elif detail_link:
                homepage = detail_link

            # Aggregate by key (handle multiple rows for same conference)
            if key not in conferences_map:
                conferences_map[key] = {
                    "key": key,
                    "name": name,
                    "year": year,
                    "homepage": homepage,
                    "deadlines": [],
                    "source": self.name,
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                    "url": response.url,
                }

            # Add deadline to conference if present
            if deadlines:
                # Avoid duplicate deadlines for the same conference
                existing_dates = {d["due_date"] for d in conferences_map[key]["deadlines"]}
                for deadline in deadlines:
                    if deadline["due_date"] not in existing_dates:
                        conferences_map[key]["deadlines"].append(deadline)
                        existing_dates.add(deadline["due_date"])

            self.logger.debug(
                f"Processed: name={name[:50]}, year={year}, key={key}"
            )

        # Yield all unique conferences
        for conf_data in conferences_map.values():
            if not conf_data["key"] or not conf_data["name"]:
                self.logger.warning(
                    "Skipping conference with invalid key or name: "
                    f"key={conf_data['key']}, name={conf_data['name'][:50]}"
                )
                continue

            yield ConferenceItem(**conf_data)
            self.logger.debug(
                f"Found: {conf_data['name']} (deadlines: {len(conf_data['deadlines'])})"
            )

        self.logger.info(
            f"Finished parsing {response.url} - found {len(conferences_map)} unique conferences"
        )

    def _parse_date(self, date_str: str) -> datetime | None:
        """Parse date string like '15 May 2025' or '2 Jun 2025'."""
        if not date_str:
            return None

        # Try common formats
        formats = [
            "%d %b %Y",  # 15 May 2025
            "%d %B %Y",  # 15 May 2025 (full month)
            "%Y-%m-%d",  # 2025-05-15
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                continue

        self.logger.debug(f"Could not parse date: {date_str}")
        return None

    def _extract_year(self, text: str) -> int | None:
        """Extract 4-digit year from text."""
        if not text:
            return None
        match = re.search(r"\b(20\d{2})\b", text)
        return int(match.group(1)) if match else None

    def _generate_key(self, name: str, year: int | None) -> str:
        """Generate conference key from name and year."""
        # Extract acronym (uppercase letters/numbers)
        acronym = re.findall(r"[A-Z0-9]+", name)
        if acronym:
            # Use longest acronym to avoid single-letter keys
            key = max(acronym, key=len).lower()
        else:
            # Fallback: first significant word (skip common words)
            words = re.findall(r"\w+", name.lower())
            skip_words = {"the", "a", "an", "on", "for", "of", "in", "at", "to"}
            significant_words = [
                w for w in words if w not in skip_words and len(w) > 2
            ]
            key = significant_words[0] if significant_words else (words[0] if words else "unknown")

        if year:
            key += str(year)[-2:]  # Last 2 digits
        else:
            # No year available - add a short hash suffix to ensure uniqueness
            # Using MD5 for non-security purpose (generating short unique key)
            name_hash = hashlib.md5(name.encode()).hexdigest()[:4]  # nosec B324
            key += f"_{name_hash}"

        return key
