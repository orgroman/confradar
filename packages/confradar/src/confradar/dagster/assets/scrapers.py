"""Dagster assets for web scraping conference data.

Each asset represents a scraper that fetches conference data from a specific source.
Assets return lists of conference dictionaries that can be consumed by downstream assets.
"""

import time
from typing import Any

from dagster import MetadataValue, Output, asset
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from confradar.scrapers.spiders.acl_web import ACLWebSpider
from confradar.scrapers.spiders.ai_deadlines import AIDeadlinesSpider
from confradar.scrapers.spiders.chairing_tool import ChairingToolSpider
from confradar.scrapers.spiders.elra import ELRASpider
from confradar.scrapers.spiders.wikicfp import WikiCFPSpider


def run_spider(spider_class) -> tuple[list[dict[str, Any]], float]:
    """Run a Scrapy spider and collect items with execution time tracking.

    Args:
        spider_class: The spider class to run

    Returns:
        Tuple of (list of scraped conference items, execution time in seconds)
    """
    start_time = time.time()
    collected_items = []

    def collect_item(item, response, spider):
        """Signal handler to collect scraped items."""
        collected_items.append(dict(item))

    # Configure Scrapy settings
    settings = get_project_settings()
    settings.set("HTTPCACHE_ENABLED", True)  # Enable caching for production
    settings.set("LOG_LEVEL", "INFO")
    settings.set(
        "ITEM_PIPELINES",
        {
            "confradar.scrapers.pipelines.ValidationPipeline": 100,
            "confradar.scrapers.pipelines.DeduplicationPipeline": 200,
        },
    )

    # Create crawler process
    process = CrawlerProcess(settings)

    # Connect signal to collect items
    from scrapy import signals
    from scrapy.signalmanager import dispatcher

    dispatcher.connect(collect_item, signal=signals.item_scraped)

    # Run spider
    process.crawl(spider_class)
    process.start()

    execution_time = time.time() - start_time
    return collected_items, execution_time


@asset(
    description="Scrape NLP conference data from AI Deadlines",
    group_name="scrapers",
)
def ai_deadlines_conferences() -> Output[list[dict[str, Any]]]:
    """Scrape conferences from aideadlines.org (NLP focus)."""
    items, execution_time = run_spider(AIDeadlinesSpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "aideadlines",
            "execution_time_seconds": round(execution_time, 2),
            "conferences_per_second": round(len(items) / execution_time, 2) if execution_time > 0 else 0,
            "preview": (
                MetadataValue.md("\n".join([f"- {item['name']}" for item in items[:5]]))
                if items
                else "No items scraped"
            ),
        },
    )


@asset(
    description="Scrape ACL sponsored events",
    group_name="scrapers",
)
def acl_web_conferences() -> Output[list[dict[str, Any]]]:
    """Scrape conferences from ACL Web."""
    items, execution_time = run_spider(ACLWebSpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "acl_web",
            "execution_time_seconds": round(execution_time, 2),
            "conferences_per_second": round(len(items) / execution_time, 2) if execution_time > 0 else 0,
            "preview": (
                MetadataValue.md("\n".join([f"- {item['name']}" for item in items[:5]]))
                if items
                else "No items scraped"
            ),
        },
    )


@asset(
    description="Scrape conferences from ChairingTool",
    group_name="scrapers",
)
def chairing_tool_conferences() -> Output[list[dict[str, Any]]]:
    """Scrape conferences from ChairingTool platform."""
    items, execution_time = run_spider(ChairingToolSpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "chairing_tool",
            "execution_time_seconds": round(execution_time, 2),
            "conferences_per_second": round(len(items) / execution_time, 2) if execution_time > 0 else 0,
            "preview": (
                MetadataValue.md("\n".join([f"- {item['name']}" for item in items[:5]]))
                if items
                else "No items scraped"
            ),
        },
    )


@asset(
    description="Scrape ELRA language resources events",
    group_name="scrapers",
)
def elra_conferences() -> Output[list[dict[str, Any]]]:
    """Scrape conferences from ELRA."""
    items, execution_time = run_spider(ELRASpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "elra",
            "execution_time_seconds": round(execution_time, 2),
            "conferences_per_second": round(len(items) / execution_time, 2) if execution_time > 0 else 0,
            "preview": (
                MetadataValue.md("\n".join([f"- {item['name']}" for item in items[:5]]))
                if items
                else "No items scraped"
            ),
        },
    )


@asset(
    description="Scrape call for papers from WikiCFP",
    group_name="scrapers",
)
def wikicfp_conferences() -> Output[list[dict[str, Any]]]:
    """Scrape conferences from WikiCFP."""
    items, execution_time = run_spider(WikiCFPSpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "wikicfp",
            "execution_time_seconds": round(execution_time, 2),
            "conferences_per_second": round(len(items) / execution_time, 2) if execution_time > 0 else 0,
            "preview": (
                MetadataValue.md("\n".join([f"- {item['name']}" for item in items[:5]]))
                if items
                else "No items scraped"
            ),
        },
    )
