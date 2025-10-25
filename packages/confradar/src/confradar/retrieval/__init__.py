"""Retrieval modules for external sources (scrapers/APIs).

Each source implements the Scraper interface for consistent extraction,
error handling, and Airflow integration. Scrapers return both raw data
(for debugging/reprocessing) and normalized output (schema-versioned).
"""

from .base import Scraper, ScrapeResult

__all__ = ["Scraper", "ScrapeResult"]
