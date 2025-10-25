"""Scrapy items for conference data."""
import scrapy


class ConferenceItem(scrapy.Item):
    """Conference item with deadlines."""
    
    # Conference metadata
    key = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    homepage = scrapy.Field()
    
    # Deadlines list
    deadlines = scrapy.Field()
    
    # Scraping metadata
    source = scrapy.Field()
    scraped_at = scrapy.Field()
    url = scrapy.Field()
