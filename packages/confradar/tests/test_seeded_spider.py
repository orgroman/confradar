from __future__ import annotations

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from confradar.scrapers.spiders.seeded import SeededSpider


def _run_seeded() -> list[dict]:
    items: list[dict] = []

    def collect_item(item, response, spider):
        items.append(dict(item))

    settings = get_project_settings()
    settings.set("HTTPCACHE_ENABLED", True)
    settings.set(
        "ITEM_PIPELINES",
        {
            "confradar.scrapers.pipelines.ValidationPipeline": 100,
            "confradar.scrapers.pipelines.DeduplicationPipeline": 200,
        },
    )

    process = CrawlerProcess(settings)

    from scrapy import signals
    from scrapy.signalmanager import dispatcher

    dispatcher.connect(collect_item, signal=signals.item_scraped)

    process.crawl(SeededSpider)
    process.start()
    return items


def test_seeded_spider_emits_items():
    items = _run_seeded()
    # Expect at least the curated 8 seeds
    assert len(items) >= 8

    # Validate structure
    first = items[0]
    assert "key" in first and first["key"]
    assert "name" in first and first["name"]
    assert first.get("source") == "seeded"
