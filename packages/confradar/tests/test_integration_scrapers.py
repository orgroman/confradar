"""Integration tests for scrapers (make real network calls).

Run with: uv run pytest -m integration
Skip with: uv run pytest -m "not integration"
"""
from __future__ import annotations

import pytest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from confradar.scrapers.spiders.ai_deadlines import AIDeadlinesSpider


@pytest.mark.integration
def test_ai_deadlines_spider_real():
    """Test AIDeadlinesSpider against live website using Scrapy.
    
    Note: This scrapes HTML, not an API. The site structure may change,
    causing this test to fail. That's expected - update spider logic when it happens.
    """
    # Collect items from spider
    collected_items = []
    
    def collect_item(item, response, spider):
        collected_items.append(dict(item))
    
    # Configure and run spider
    settings = get_project_settings()
    settings.set('ITEM_PIPELINES', {
        'confradar.scrapers.pipelines.ValidationPipeline': 100,
    })
    settings.set('HTTPCACHE_ENABLED', False)  # Don't use cache for integration test
    
    process = CrawlerProcess(settings)
    
    # Connect item signal
    from scrapy import signals
    from scrapy.signalmanager import dispatcher
    dispatcher.connect(collect_item, signal=signals.item_scraped)
    
    process.crawl(AIDeadlinesSpider)
    process.start()  # Blocks until spider finishes
    
    # Verify we got some data
    assert len(collected_items) > 0, "Should scrape at least one conference"
    
    # Verify item structure
    first_item = collected_items[0]
    assert "key" in first_item
    assert "name" in first_item
    assert "source" in first_item
    assert first_item["source"] == "aideadlines"
    assert "scraped_at" in first_item
    
    print(f"\n✓ Scraped {len(collected_items)} conferences from AI Deadlines")
    print(f"  Sample: {first_item['name']} ({first_item['key']})")


@pytest.mark.integration  
def test_ai_deadlines_spider_output_json(tmp_path):
    """Test spider can output to JSON file."""
    output_file = tmp_path / "conferences.json"
    
    settings = get_project_settings()
    settings.set('FEEDS', {
        str(output_file): {'format': 'json', 'overwrite': True}
    })
    settings.set('HTTPCACHE_ENABLED', False)
    
    process = CrawlerProcess(settings)
    process.crawl(AIDeadlinesSpider)
    process.start()
    
    # Verify file was created and has content
    assert output_file.exists()
    
    import json
    with open(output_file) as f:
        data = json.load(f)
    
    assert isinstance(data, list)
    assert len(data) > 0
    print(f"\n✓ Exported {len(data)} conferences to {output_file}")
