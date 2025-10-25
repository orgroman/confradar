from __future__ import annotations

from datetime import datetime, timezone

import httpx
import pytest

from confradar.retrieval.ai_deadlines import AIDeadlinesScraper, normalize_record


def test_normalize_record_basic():
    rec = {
        "title": "NeurIPS",
        "acronym": "NeurIPS",
        "year": 2025,
        "link": "https://neurips.cc",
        "deadline": "2025-05-20 23:59:59 AoE",
        "abstract_deadline": "2025-05-15 23:59:59 AoE",
    }
    item = normalize_record(rec)
    assert item.key == "neurips"
    assert item.name == "NeurIPS"
    assert item.year == 2025
    assert item.homepage == "https://neurips.cc"
    kinds = {d.kind for d in item.deadlines}
    assert kinds == {"submission", "abstract"}


def test_scraper_with_mocked_http(monkeypatch):
    """Test AIDeadlinesScraper.scrape() with mocked httpx."""
    sample = [
        {
            "title": "ACL",
            "acronym": "ACL",
            "year": "2025",
            "link": "https://aclweb.org",
            "deadline": "2025-02-01T23:59:59",
        }
    ]

    class FakeResponse:
        def __init__(self, data):
            self._data = data

        def raise_for_status(self):
            return None

        def json(self):
            return self._data

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get(self, url, **kwargs):
            return FakeResponse(sample)

    monkeypatch.setattr(httpx, "Client", FakeClient)

    scraper = AIDeadlinesScraper("https://example/api")
    result = scraper.scrape()
    
    assert result.source_name == "aideadlines"
    assert result.schema_version == "1.0"
    assert len(result.normalized) == 1
    assert result.normalized[0]["key"] == "acl"
    assert any(d["kind"] == "submission" for d in result.normalized[0]["deadlines"])