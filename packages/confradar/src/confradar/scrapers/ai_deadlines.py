from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
import re

import httpx
from bs4 import BeautifulSoup

from confradar.scrapers.base import Scraper, ScrapeResult


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
    deadlines: List[DeadlineItem]


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

    def parse(self, raw: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """Parse HTML into normalized ConferenceItem records."""
        soup = BeautifulSoup(raw, 'html.parser')
        conferences = []
        
        # Find conference entries - structure may vary, this is a best-effort parse
        # Look for conference links and deadline info
        for link in soup.find_all('a', href=re.compile(r'/conference\?id=')):
            try:
                conf_id = re.search(r'id=([^&]+)', link.get('href', ''))
                if not conf_id:
                    continue
                    
                key = conf_id.group(1)
                name = link.get_text(strip=True)
                
                # Try to find the conference's website link (usually nearby)
                homepage = None
                parent = link.parent
                if parent:
                    website_link = parent.find('a', href=re.compile(r'^https?://'))
                    if website_link:
                        homepage = website_link.get('href')
                
                # Extract year from key if present (e.g., 'icml25' -> 2025)
                year = None
                year_match = re.search(r'(\d{2})$', key)
                if year_match:
                    yr = int(year_match.group(1))
                    year = 2000 + yr if yr < 50 else 1900 + yr
                
                conf_dict = {
                    'key': key,
                    'name': name,
                    'year': year,
                    'homepage': homepage,
                    'deadlines': []  # Deadline extraction would require more complex parsing
                }
                conferences.append(conf_dict)
            except Exception:
                # Skip malformed entries
                continue
        
        return conferences

    def validate(self, normalized: List[Dict[str, Any]]) -> None:
        """Validate normalized output has required fields."""
        for item in normalized:
            if not isinstance(item, dict):
                raise ValueError(f"Expected dict, got {type(item)}")
            if "key" not in item or "name" not in item:
                raise ValueError(f"Missing key/name: {item}")
            if "deadlines" not in item or not isinstance(item["deadlines"], list):
                raise ValueError(f"Invalid deadlines field: {item}")
