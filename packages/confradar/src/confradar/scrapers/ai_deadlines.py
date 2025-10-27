from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx
from bs4 import BeautifulSoup

from confradar.scrapers.base import Scraper


@dataclass
class DeadlineItem:
    kind: str
    due_at: datetime
    timezone: str | None = None


@dataclass
class ConferenceItem:
    key: str
    name: str
    year: int | None
    homepage: str | None
    deadlines: list[DeadlineItem]


DEFAULT_URL = "https://aideadlin.es"


class AIDeadlinesScraper(Scraper):
    """Scraper for aideadlin.es website (HTML scraping).

    Schema v1.0: Returns list of conference dicts with key, name, year,
    homepage, and deadlines list.

    Note: This scraper parses HTML since there's no official API.
    The page structure may change - be prepared to update parse() logic.
    """

    def __init__(self, url: str = DEFAULT_URL):
        self._url = url

    @property
    def source_name(self) -> str:
        return "aideadlines"

    @property
    def schema_version(self) -> str:
        return "1.0"

    def fetch(self, **kwargs: Any) -> str:
        """Fetch HTML from aideadlin.es."""
        url = kwargs.get("url", self._url)
        timeout = kwargs.get("timeout", 20.0)

        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            resp = client.get(url)
            resp.raise_for_status()
            return resp.text

    def parse(self, raw: str, **kwargs: Any) -> list[dict[str, Any]]:
        """Parse HTML into normalized ConferenceItem records.

        The AI Deadlines site embeds deadline information in JavaScript code blocks.
        We extract this using regex patterns to find moment.tz() calls.
        """
        soup = BeautifulSoup(raw, "html.parser")
        conferences = {}  # Use dict to deduplicate by key

        # Find conference entries - structure may vary, this is a best-effort parse
        # Look for conference links and deadline info
        for link in soup.find_all("a", href=re.compile(r"/conference\?id=")):
            try:
                conf_id = re.search(r"id=([^&]+)", link.get("href", ""))
                if not conf_id:
                    continue

                key = conf_id.group(1)

                # Skip if we already have this conference (avoid duplicates)
                if key in conferences:
                    continue

                name = link.get_text(strip=True)

                # Try to find the conference's website link (usually nearby)
                homepage = None
                parent = link.parent
                if parent:
                    parent_parent = parent.parent
                    if parent_parent:
                        website_link = parent_parent.find(
                            "a", href=re.compile(r"^https?://"), title="Conference Website"
                        )
                        if website_link:
                            homepage = website_link.get("href")

                # Extract year from key if present (e.g., 'icml25' -> 2025)
                year = None
                year_match = re.search(r"(\d{2})$", key)
                if year_match:
                    yr = int(year_match.group(1))
                    year = 2000 + yr if yr < 50 else 1900 + yr

                conferences[key] = {
                    "key": key,
                    "name": name,
                    "year": year,
                    "homepage": homepage,
                    "deadlines": [],
                }
            except Exception:
                # Skip malformed entries
                continue

        # Extract deadline information from JavaScript blocks
        # Pattern: var timezone = "UTC-12"; moment.tz("YYYY-MM-DD HH:MM:SS", timezone)
        # We need to match conference IDs with their timezone and deadline
        script_tags = soup.find_all("script", string=True)
        for script in script_tags:
            script_text = script.string
            if not script_text:
                continue

            # Find conference deadline blocks
            # Each block looks like: $('#confkey') ... var timezone = "..."; moment.tz("date", timezone)
            conf_block_pattern = re.compile(
                r'\$\([\'"]#(\w+).*?var\s+timezone\s*=\s*[\'"]([^\'\"]+)[\'"].*?moment\.tz\([\'"]([^\'\"]+)[\'"]',
                re.DOTALL,
            )

            for match in conf_block_pattern.finditer(script_text):
                conf_key = match.group(1)
                timezone_str = match.group(2)
                deadline_str = match.group(3)

                # Skip non-conference entries (like 'subject')
                if conf_key not in conferences:
                    continue

                try:
                    # Parse the deadline string (handle both with and without seconds)
                    try:
                        deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        # Try without seconds
                        deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

                    # Add deadline to conference
                    # Note: We're assuming this is a submission deadline
                    # The site doesn't always distinguish between abstract/submission
                    conferences[conf_key]["deadlines"].append(
                        {
                            "kind": "submission",
                            "due_at": deadline_dt.isoformat(),
                            "timezone": timezone_str,
                        }
                    )
                except ValueError:
                    # Skip if date parsing fails
                    continue

        return list(conferences.values())

    def validate(self, normalized: list[dict[str, Any]]) -> None:
        """Validate normalized output has required fields."""
        for item in normalized:
            if not isinstance(item, dict):
                raise ValueError(f"Expected dict, got {type(item)}")
            if "key" not in item or "name" not in item:
                raise ValueError(f"Missing key/name: {item}")
            if "deadlines" not in item or not isinstance(item["deadlines"], list):
                raise ValueError(f"Invalid deadlines field: {item}")
