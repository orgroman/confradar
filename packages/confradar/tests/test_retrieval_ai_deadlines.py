from __future__ import annotations

import httpx

from confradar.scrapers.ai_deadlines import AIDeadlinesScraper


def test_scraper_parses_html():
    """Test that AIDeadlinesScraper can parse HTML structure."""
    sample_html = """
    <html>
    <body>
        <a href="/conference?id=icml25">ICML 2025</a>
        <a href="https://icml.cc/Conferences/2025">Conference Website</a>
        <a href="/conference?id=neurips24">NeurIPS 2024</a>
    </body>
    </html>
    """

    scraper = AIDeadlinesScraper()
    result = scraper.parse(sample_html)

    assert len(result) >= 2
    conf_keys = {c["key"] for c in result}
    assert "icml25" in conf_keys
    assert "neurips24" in conf_keys


def test_scraper_with_mocked_http(monkeypatch):
    """Test AIDeadlinesScraper.scrape() with mocked httpx."""
    sample_html = """
    <html>
    <body>
        <a href="/conference?id=acl25">ACL 2025</a>
        <a href="https://aclweb.org">Conference Website</a>
    </body>
    </html>
    """

    class FakeResponse:
        def __init__(self):
            self.text = sample_html

        def raise_for_status(self):
            return None

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get(self, url, **kwargs):
            return FakeResponse()

    monkeypatch.setattr(httpx, "Client", FakeClient)

    scraper = AIDeadlinesScraper("https://example.com")
    result = scraper.scrape()

    assert result.source_name == "aideadlines"
    assert result.schema_version == "1.0"
    assert len(result.normalized) >= 1
    assert result.normalized[0]["key"] == "acl25"
