"""Spider for ACL Web sponsored events.

Scrapes conference listings from ACL (Association for Computational Linguistics).
"""
from datetime import datetime, timezone
from typing import Iterator
import re

import scrapy
from scrapy.http import Response

from confradar.scrapers.items import ConferenceItem


class ACLWebSpider(scrapy.Spider):
    """Scrape ACL sponsored events.
    
    Source: https://www.aclweb.org/portal/acl_sponsored_events
    
    Usage:
        scrapy crawl acl_web -o acl_conferences.json
    """
    
    name = "acl_web"
    allowed_domains = ["aclweb.org"]
    start_urls = ["https://www.aclweb.org/portal/acl_sponsored_events"]
    
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }
    
    def parse(self, response: Response) -> Iterator[ConferenceItem]:
        """Parse ACL events page."""
        self.logger.info(f"Parsing {response.url}")
        
        # ACL lists events in a structured format
        # Look for conference entries (adjust selectors based on actual HTML)
        for event in response.css('.event-item, article.event, div.conference'):
            name = event.css('h2::text, h3::text, .title::text').get('')
            if not name:
                continue
                
            name = name.strip()
            
            # Extract year from name or date fields
            year = self._extract_year(name)
            if not year:
                # Try date fields
                date_text = event.css('.date::text, .event-date::text').get('')
                year = self._extract_year(date_text)
            
            # Extract homepage URL
            homepage = event.css('a[href*="http"]::attr(href)').get()
            if homepage and 'aclweb.org' not in homepage:
                # External link is likely the conference homepage
                pass
            else:
                homepage = None
            
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
        
        self.logger.info(f"Finished parsing {response.url}")
    
    def _extract_year(self, text: str) -> int | None:
        """Extract 4-digit year from text."""
        if not text:
            return None
        match = re.search(r'\b(20\d{2})\b', text)
        return int(match.group(1)) if match else None
    
    def _generate_key(self, name: str, year: int | None) -> str:
        """Generate conference key from name and year."""
        # Extract acronym (uppercase letters/numbers)
        acronym = re.findall(r'[A-Z0-9]+', name)
        if acronym:
            key = acronym[0].lower()
        else:
            # Fallback: first word
            words = re.findall(r'\w+', name)
            key = words[0].lower() if words else 'unknown'
        
        if year:
            key += str(year)[-2:]  # Last 2 digits
        
        return key
