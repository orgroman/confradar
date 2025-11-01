"""Seeded spider for top CS conference series.

This spider yields a curated set of core conference series entries to
bootstrap the knowledge base and ensure canonical keys exist early.

It performs a lightweight request to each homepage (primarily to record
the source URL and avoid special-casing Scrapy flow). No parsing is done; 
we simply emit ConferenceItem objects based on the curated list.

Seeds include: ACL, NeurIPS, ICML, ICLR, AAAI, EMNLP, CVPR, KDD.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone

import scrapy
from scrapy.http import Request, Response

from confradar.scrapers.items import ConferenceItem


SEEDS: list[dict[str, str]] = [
    {"key": "acl", "name": "Association for Computational Linguistics (ACL)", "homepage": "https://www.aclweb.org/"},
    {"key": "neurips", "name": "Conference on Neural Information Processing Systems (NeurIPS)", "homepage": "https://neurips.cc/"},
    {"key": "icml", "name": "International Conference on Machine Learning (ICML)", "homepage": "https://icml.cc/"},
    {"key": "iclr", "name": "International Conference on Learning Representations (ICLR)", "homepage": "https://iclr.cc/"},
    {"key": "aaai", "name": "AAAI Conference on Artificial Intelligence (AAAI)", "homepage": "https://aaai.org/"},
    {"key": "emnlp", "name": "Conference on Empirical Methods in Natural Language Processing (EMNLP)", "homepage": "https://www.emnlp.org/"},
    {"key": "cvpr", "name": "IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)", "homepage": "https://cvpr.thecvf.com/"},
    {"key": "kdd", "name": "ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD)", "homepage": "https://www.kdd.org/"},
]


class SeededSpider(scrapy.Spider):
    name = "seeded"
    allowed_domains = [
        "aclweb.org",
        "neurips.cc",
        "icml.cc",
        "iclr.cc",
        "aaai.org",
        "emnlp.org",
        "thecvf.com",
        "kdd.org",
    ]
    # Ensure we receive callbacks even for non-200 responses (e.g., 409)
    handle_httpstatus_all = True

    custom_settings = {
        "DOWNLOAD_DELAY": 0.25,
        "COOKIES_ENABLED": False,
        "HTTPCACHE_ENABLED": True,
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        },
        # Keep pipelines minimal here; Dagster asset may override
    }

    async def start(self):
        """Emit seed items directly without requiring network access."""
        for seed in SEEDS:
            yield ConferenceItem(
                key=seed["key"],
                name=seed["name"],
                homepage=seed["homepage"],
                deadlines=[],
                source=self.name,
                scraped_at=datetime.now(timezone.utc).isoformat(),
                url=seed["homepage"],
            )

    def parse(self, response: Response) -> Iterator[ConferenceItem]:
        # Fallback path (not used when start() emits items directly)
        seed = response.meta.get("seed")
        if seed:
            yield ConferenceItem(
                key=seed["key"],
                name=seed["name"],
                homepage=seed["homepage"],
                deadlines=[],
                source=self.name,
                scraped_at=datetime.now(timezone.utc).isoformat(),
                url=response.url,
            )
