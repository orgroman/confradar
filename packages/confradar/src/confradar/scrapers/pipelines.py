"""Scrapy pipelines for processing conference items."""
from datetime import datetime, timezone
from typing import Any


class ValidationPipeline:
    """Validate conference items have required fields."""
    
    def process_item(self, item: dict, spider: Any) -> dict:
        """Validate item has required fields."""
        required = ["key", "name"]
        for field in required:
            if not item.get(field):
                raise ValueError(f"Missing required field: {field}")
        
        if "deadlines" not in item:
            item["deadlines"] = []
        
        return item


class DeduplicationPipeline:
    """Remove duplicate conferences within a scraping session."""
    
    def __init__(self):
        self.seen_keys = set()
    
    def open_spider(self, spider: Any) -> None:
        """Reset seen keys at start of spider."""
        self.seen_keys = set()
    
    def process_item(self, item: dict, spider: Any) -> dict:
        """Drop item if we've seen this conference key already."""
        key = item.get("key")
        if key in self.seen_keys:
            raise ValueError(f"Duplicate conference key: {key}")
        
        self.seen_keys.add(key)
        return item


class DatabasePipeline:
    """Store conferences in database (future)."""
    
    def open_spider(self, spider: Any) -> None:
        """Connect to database."""
        # TODO: Initialize database session
        pass
    
    def close_spider(self, spider: Any) -> None:
        """Close database connection."""
        # TODO: Close database session
        pass
    
    def process_item(self, item: dict, spider: Any) -> dict:
        """Save conference to database."""
        # TODO: Implement database storage using SQLAlchemy models
        return item
