"""Spider for ELRA events.

Scrapes conference and event listings from ELRA (European Language Resources Association).
"""
from datetime import datetime, timezone
from typing import Iterator
import re

import scrapy
from scrapy.http import Response

from confradar.scrapers.items import ConferenceItem


class ELRASpider(scrapy.Spider):
    """Scrape ELRA events and conferences.
    
    Source: https://www.elra.info/elra-events/
    
    Usage:
        scrapy crawl elra -o elra_conferences.json
    """
    
    name = "elra"
    allowed_domains = ["elra.info"]
    start_urls = ["https://www.elra.info/elra-events/"]
    
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }
    
    def parse(self, response: Response) -> Iterator[ConferenceItem]:
        """Parse ELRA events page."""
        self.logger.info(f"Parsing {response.url}")
        
        # ELRA typically has events in a list or article format
        for event in response.css('.event, article, .post, div.entry'):
            # Try multiple selectors for title
            name = event.css('h2::text, h3::text, .entry-title::text, .event-title::text').get('')
            if not name:
                continue
                
            name = name.strip()
            
            # Skip if not a conference/workshop
            name_lower = name.lower()
            if not any(keyword in name_lower for keyword in ['conference', 'workshop', 'symposium', 'summit', 'meeting']):
                continue
            
            # Extract year
            year = self._extract_year(name)
            if not year:
                # Try from date or content
                date_text = event.css('.date::text, .event-date::text, time::text').get('')
                year = self._extract_year(date_text)
                if not year:
                    content = event.css('::text').getall()
                    year = self._extract_year(' '.join(content))
            
            # Extract homepage URL
            homepage = event.css('a[href*="http"]::attr(href)').get()
            if homepage and 'elra.info' in homepage:
                # Look for external links
                links = event.css('a[href*="http"]::attr(href)').getall()
                for link in links:
                    if 'elra.info' not in link:
                        homepage = link
                        break
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
        # Extract acronym
        acronym = re.findall(r'[A-Z0-9]+', name)
        if acronym:
            key = acronym[0].lower()
        else:
            words = re.findall(r'\w+', name)
            key = words[0].lower() if words else 'unknown'
        
        if year:
            key += str(year)[-2:]
        
        return key
