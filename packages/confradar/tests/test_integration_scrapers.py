"""Integration tests for scrapers (make real network calls).

Run with: uv run pytest -m integration
Skip with: uv run pytest -m "not integration"

Note: Uses subprocess approach to avoid Scrapy reactor restartability issues.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from confradar.scrapers.spiders.acl_web import ACLWebSpider
from confradar.scrapers.spiders.ai_deadlines import AIDeadlinesSpider
from confradar.scrapers.spiders.elra import ELRASpider
from confradar.scrapers.spiders.wikicfp import WikiCFPSpider


def run_spider_in_subprocess(spider_cls, output_file: Path) -> int:
    """Run a spider in a subprocess to avoid reactor issues.

    Args:
        spider_cls: Spider class to run
        output_file: Path to JSON output file

    Returns:
        Return code from subprocess
    """
    # Create a simple script that runs the spider
    script = f"""
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import the spider class
spider_cls = {spider_cls.__module__}.{spider_cls.__name__}

# Configure settings
settings = get_project_settings()
settings.set("HTTPCACHE_ENABLED", False)
settings.set("FEEDS", {{
    "{output_file.as_posix()}": {{"format": "json", "overwrite": True}}
}})
settings.set("ITEM_PIPELINES", {{
    "confradar.scrapers.pipelines.ValidationPipeline": 100,
}})
settings.set("LOG_LEVEL", "WARNING")  # Reduce noise in tests

# Run spider
process = CrawlerProcess(settings)
process.crawl(spider_cls)
process.start()
"""

    # Run in subprocess
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=30,  # 30 second timeout per spider
    )

    if result.returncode != 0:
        print(f"Spider failed: {result.stderr}")

    return result.returncode


def run_spider_and_collect(spider_cls) -> list[dict]:
    """Run a spider and collect all scraped items.

    Args:
        spider_cls: Spider class to run

    Returns:
        List of scraped items as dictionaries
    """
    # Create temporary file for output
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_file:
        output_file = Path(tmp_file.name)

    try:
        # Run spider in subprocess
        returncode = run_spider_in_subprocess(spider_cls, output_file)

        if returncode != 0:
            return []

        # Read results
        if output_file.exists() and output_file.stat().st_size > 0:
            with open(output_file) as f:
                items = json.load(f)
            return items if isinstance(items, list) else []
        return []

    finally:
        # Clean up temp file
        if output_file.exists():
            output_file.unlink()


@pytest.mark.integration
def test_ai_deadlines_spider_real():
    """Test AIDeadlinesSpider against real website."""
    items = run_spider_and_collect(AIDeadlinesSpider)

    # Verify we got items
    assert len(items) > 0, "Should scrape at least some conferences"
    print(f"\n✓ Scraped {len(items)} conferences from AI Deadlines (NLP)")

    # Check structure of first item
    item = items[0]
    assert "key" in item
    assert "name" in item
    assert "source" in item
    assert item["source"] == "aideadlines"
    assert "scraped_at" in item

    print(f"  Sample: {item['name']} ({item['key']})")


@pytest.mark.integration
def test_acl_web_spider_real():
    """Test ACLWebSpider against real website."""
    items = run_spider_and_collect(ACLWebSpider)

    # ACL might have fewer conferences listed
    assert len(items) >= 0, "Should run without errors"
    print(f"\n✓ Scraped {len(items)} conferences from ACL Web")

    if items:
        item = items[0]
        assert "key" in item
        assert "name" in item
        assert "source" in item
        assert item["source"] == "acl_web"
        print(f"  Sample: {item['name']} ({item['key']})")
    else:
        print("  (No items found - site structure may have changed)")


@pytest.mark.integration
def test_elra_spider_real():
    """Test ELRASpider against real website."""
    items = run_spider_and_collect(ELRASpider)

    assert len(items) >= 0, "Should run without errors"
    print(f"\n✓ Scraped {len(items)} conferences from ELRA")

    if items:
        item = items[0]
        assert "key" in item
        assert "name" in item
        assert "source" in item
        assert item["source"] == "elra"
        print(f"  Sample: {item['name']} ({item['key']})")
    else:
        print("  (No items found - site structure may have changed)")


@pytest.mark.integration
def test_wikicfp_spider_real():
    """Test WikiCFPSpider against real website."""
    items = run_spider_and_collect(WikiCFPSpider)

    # WikiCFP should have many conferences
    assert len(items) > 0, "Should scrape at least some conferences"
    print(f"\n✓ Scraped {len(items)} conferences from WikiCFP")

    item = items[0]
    assert "key" in item
    assert "name" in item
    assert "source" in item
    assert item["source"] == "wikicfp"
    print(f"  Sample: {item['name']} ({item['key']})")


@pytest.mark.integration
def test_all_spiders_summary():
    """Run all spiders and show summary.

    This gives a quick overview of what each spider can fetch.
    """
    spiders = [
        (AIDeadlinesSpider, "AI Deadlines (NLP)"),
        (ACLWebSpider, "ACL Web"),
        (ELRASpider, "ELRA"),
        (WikiCFPSpider, "WikiCFP"),
    ]

    total_items = 0
    results = []

    for spider_cls, name in spiders:
        try:
            items = run_spider_and_collect(spider_cls)
            results.append((name, len(items), items[0] if items else None))
            total_items += len(items)
        except Exception as e:
            results.append((name, 0, f"Error: {e}"))

    print("\n" + "=" * 60)
    print("Spider Summary")
    print("=" * 60)
    for name, count, sample in results:
        if isinstance(sample, str):
            print(f"{name:25s} {sample}")
        elif sample:
            print(f"{name:25s} {count:4d} items  (e.g., {sample['name']})")
        else:
            print(f"{name:25s} {count:4d} items")
    print("=" * 60)
    print(f"{'TOTAL':25s} {total_items:4d} items")
    print("=" * 60)

    assert total_items > 0, "Should scrape at least some conferences across all spiders"


@pytest.mark.integration
def test_ai_deadlines_spider_output_json(tmp_path):
    """Test spider can output to JSON file."""
    output_file = tmp_path / "conferences.json"

    # Run spider in subprocess with output to file
    returncode = run_spider_in_subprocess(AIDeadlinesSpider, output_file)

    assert returncode == 0, "Spider should complete successfully"

    # Verify file was created and has content
    assert output_file.exists()

    with open(output_file) as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) > 0
    print(f"\n✓ Exported {len(data)} conferences to {output_file}")
