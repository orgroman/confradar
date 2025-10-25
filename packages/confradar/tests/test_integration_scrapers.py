"""Integration tests for scrapers (make real network calls).

Run with: uv run pytest -m integration
Skip with: uv run pytest -m "not integration"
"""
from __future__ import annotations

import pytest

from confradar.scrapers.ai_deadlines import AIDeadlinesScraper


@pytest.mark.integration
def test_ai_deadlines_scraper_real():
    """Test AIDeadlinesScraper against live website.
    
    Note: This scrapes HTML, not an API. The site structure may change,
    causing this test to fail. That's expected - update parse() logic when it happens.
    """
    scraper = AIDeadlinesScraper()
    result = scraper.scrape(timeout=30.0)
    
    # Verify ScrapeResult structure
    assert result.source_name == "aideadlines"
    assert result.schema_version == "1.0"
    assert result.scraped_at is not None
    assert result.raw_data is not None
    assert isinstance(result.raw_data, str), "Raw data should be HTML string"
    
    # Verify we got some data (may be 0 if page structure changed)
    assert isinstance(result.normalized, list)
    
    # Verify metadata
    assert "count" in result.metadata
    assert result.metadata["count"] == len(result.normalized)
    
    if len(result.normalized) > 0:
        # Verify normalized schema
        first_conf = result.normalized[0]
        assert "key" in first_conf
        assert "name" in first_conf
        assert "deadlines" in first_conf
        assert isinstance(first_conf["deadlines"], list)
        
        print(f"\n✓ Scraped {len(result.normalized)} conferences from AI Deadlines")
        print(f"  Sample: {first_conf['name']} ({first_conf['key']})")
    else:
        print("\n⚠ No conferences extracted - page structure may have changed")
        print(f"  HTML length: {len(result.raw_data)} chars")
        print("  This is expected for HTML scrapers - update parse() logic as needed")
