"""Dagster assets for web scraping conference data.

Each asset represents a scraper that fetches conference data from a specific source.
Assets return lists of conference dictionaries that can be consumed by downstream assets.
"""

from typing import Any

from dagster import MetadataValue, Output, asset
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from confradar.scrapers.spiders.acl_web import ACLWebSpider
from confradar.scrapers.spiders.ai_deadlines import AIDeadlinesSpider
from confradar.scrapers.spiders.chairing_tool import ChairingToolSpider
from confradar.scrapers.spiders.elra import ELRASpider
from confradar.scrapers.spiders.wikicfp import WikiCFPSpider
from confradar.scrapers.spiders.seeded import SeededSpider


def run_spider(spider_class) -> list[dict[str, Any]]:
    """Run a Scrapy spider and collect items.

    Args:
        spider_class: The spider class to run

    Returns:
        List of scraped conference items as dictionaries
    """
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

    return collected_items


@asset(
    description="Scrape NLP conference data from AI Deadlines",
    group_name="scrapers",
)
def ai_deadlines_conferences() -> Output[list[dict[str, Any]]]:
    """Scrape conferences from aideadlines.org (NLP focus)."""
    items = run_spider(AIDeadlinesSpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "aideadlines",
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
    items = run_spider(ACLWebSpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "acl_web",
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
    items = run_spider(ChairingToolSpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "chairing_tool",
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
    items = run_spider(ELRASpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "elra",
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
    items = run_spider(WikiCFPSpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "wikicfp",
            "preview": (
                MetadataValue.md("\n".join([f"- {item['name']}" for item in items[:5]]))
                if items
                else "No items scraped"
            ),
        },
    )


@asset(
    description="Seed core conference series (no parsing)",
    group_name="scrapers",
)
def seeded_conferences() -> Output[list[dict[str, Any]]]:
    """Emit curated seed conferences as items via a simple spider.

    This ensures canonical keys and homepages exist in storage even if other
    scrapers are unavailable or rate-limited.
    """
    items = run_spider(SeededSpider)

    return Output(
        value=items,
        metadata={
            "count": len(items),
            "source": "seeded",
            "preview": (
                MetadataValue.md("\n".join([f"- {item['name']}" for item in items[:8]]))
                if items
                else "No seeds emitted"
            ),
        },
    )
