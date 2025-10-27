"""Unit tests for AI Deadlines scraper deadline extraction."""

import pytest

from confradar.scrapers.ai_deadlines import AIDeadlinesScraper


class TestAIDeadlinesScraperParsing:
    """Test the parsing logic of AI Deadlines scraper."""

    def test_parse_basic_conference_html(self):
        """Test parsing basic conference information from HTML."""
        html = """
        <html>
        <body>
            <a href="/conference?id=icml25">ICML 2025</a>
            <a href="https://icml.cc" title="Conference Website">Conference Website</a>
        </body>
        </html>
        """

        scraper = AIDeadlinesScraper()
        result = scraper.parse(html)

        assert len(result) == 1
        conf = result[0]
        assert conf["key"] == "icml25"
        assert conf["name"] == "ICML 2025"
        assert conf["year"] == 2025
        assert conf["homepage"] == "https://icml.cc"

    def test_parse_conference_with_deadline(self):
        """Test parsing conference with JavaScript deadline."""
        html = """
        <html>
        <body>
            <a href="/conference?id=neurips24">NeurIPS 2024</a>
        </body>
        <script>
            $('#neurips24 .ML-tag').html('ml');
            var timezone = "UTC-12";
            var confDate = moment.tz("2024-05-15 23:59:59", timezone);
        </script>
        </html>
        """

        scraper = AIDeadlinesScraper()
        result = scraper.parse(html)

        assert len(result) == 1
        conf = result[0]
        assert conf["key"] == "neurips24"
        assert len(conf["deadlines"]) == 1

        deadline = conf["deadlines"][0]
        assert deadline["kind"] == "submission"
        assert deadline["due_at"] == "2024-05-15T23:59:59"
        assert deadline["timezone"] == "UTC-12"

    def test_parse_deadline_without_seconds(self):
        """Test parsing deadline in HH:MM format (no seconds)."""
        html = """
        <html>
        <body>
            <a href="/conference?id=iclr25">ICLR 2025</a>
        </body>
        <script>
            $('#iclr25').html('test');
            var timezone = "UTC-12";
            var confDate = moment.tz("2024-09-11 23:59", timezone);
        </script>
        </html>
        """

        scraper = AIDeadlinesScraper()
        result = scraper.parse(html)

        assert len(result) == 1
        deadline = result[0]["deadlines"][0]
        assert deadline["due_at"] == "2024-09-11T23:59:00"
        assert deadline["timezone"] == "UTC-12"

    def test_deduplication_of_conferences(self):
        """Test that duplicate conference entries are deduplicated."""
        html = """
        <html>
        <body>
            <a href="/conference?id=acl25">ACL 2025</a>
            <a href="/conference?id=acl25">ACL '25</a>
        </body>
        </html>
        """

        scraper = AIDeadlinesScraper()
        result = scraper.parse(html)

        # Should only have one conference despite two links
        assert len(result) == 1
        assert result[0]["key"] == "acl25"

    def test_year_extraction_from_key(self):
        """Test extracting year from conference key."""
        html = """
        <html>
        <body>
            <a href="/conference?id=cvpr25">CVPR 2025</a>
            <a href="/conference?id=emnlp24">EMNLP 2024</a>
            <a href="/conference?id=icml99">ICML 1999</a>
        </body>
        </html>
        """

        scraper = AIDeadlinesScraper()
        result = scraper.parse(html)

        # Check year extraction
        years_by_key = {c["key"]: c["year"] for c in result}
        assert years_by_key["cvpr25"] == 2025
        assert years_by_key["emnlp24"] == 2024
        assert years_by_key["icml99"] == 1999  # 99 -> 1999 (< 50 cutoff)

    def test_multiple_conferences_with_deadlines(self):
        """Test parsing multiple conferences with different deadlines."""
        html = """
        <html>
        <body>
            <a href="/conference?id=conf1">Conference 1</a>
            <a href="/conference?id=conf2">Conference 2</a>
        </body>
        <script>
            $('#conf1').html('test');
            var timezone = "UTC-12";
            var confDate = moment.tz("2024-05-15 23:59:59", timezone);
            
            $('#conf2').html('test');
            var timezone = "GMT";
            var confDate = moment.tz("2024-06-20 12:00:00", timezone);
        </script>
        </html>
        """

        scraper = AIDeadlinesScraper()
        result = scraper.parse(html)

        assert len(result) == 2

        # Check both conferences have deadlines
        conf1 = next(c for c in result if c["key"] == "conf1")
        conf2 = next(c for c in result if c["key"] == "conf2")

        assert len(conf1["deadlines"]) == 1
        assert len(conf2["deadlines"]) == 1

        assert conf1["deadlines"][0]["timezone"] == "UTC-12"
        assert conf2["deadlines"][0]["timezone"] == "GMT"

    def test_ignore_invalid_dates(self):
        """Test that invalid dates are skipped gracefully."""
        html = """
        <html>
        <body>
            <a href="/conference?id=test25">Test 2025</a>
        </body>
        <script>
            $('#test25').html('test');
            var timezone = "UTC-12";
            var confDate = moment.tz("invalid-date", timezone);
        </script>
        </html>
        """

        scraper = AIDeadlinesScraper()
        result = scraper.parse(html)

        assert len(result) == 1
        assert len(result[0]["deadlines"]) == 0  # Invalid date should be skipped

    def test_scrape_integration(self, monkeypatch):
        """Test the full scrape() method with mocked HTTP."""
        sample_html = """
        <html>
        <body>
            <a href="/conference?id=test25">Test Conference 2025</a>
        </body>
        <script>
            $('#test25').html('test');
            var timezone = "UTC-12";
            var confDate = moment.tz("2024-12-31 23:59:59", timezone);
        </script>
        </html>
        """

        class FakeResponse:
            def __init__(self):
                self.text = sample_html

            def raise_for_status(self):
                pass

        class FakeClient:
            def __init__(self, *args, **kwargs):
                pass

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def get(self, url, **kwargs):
                return FakeResponse()

        import httpx

        monkeypatch.setattr(httpx, "Client", FakeClient)

        scraper = AIDeadlinesScraper()
        result = scraper.scrape()

        assert result.source_name == "aideadlines"
        assert result.schema_version == "1.0"
        assert len(result.normalized) == 1

        conf = result.normalized[0]
        assert conf["key"] == "test25"
        assert conf["name"] == "Test Conference 2025"
        assert len(conf["deadlines"]) == 1


class TestAIDeadlinesScraperValidation:
    """Test validation logic."""

    def test_validate_requires_key_and_name(self):
        """Test that validation requires key and name fields."""
        scraper = AIDeadlinesScraper()

        # Valid item
        valid = [{"key": "test", "name": "Test", "deadlines": []}]
        scraper.validate(valid)  # Should not raise

        # Missing key
        with pytest.raises(ValueError, match="Missing key/name"):
            scraper.validate([{"name": "Test", "deadlines": []}])

        # Missing name
        with pytest.raises(ValueError, match="Missing key/name"):
            scraper.validate([{"key": "test", "deadlines": []}])

    def test_validate_requires_deadlines_list(self):
        """Test that deadlines must be a list."""
        scraper = AIDeadlinesScraper()

        # Valid
        valid = [{"key": "test", "name": "Test", "deadlines": []}]
        scraper.validate(valid)  # Should not raise

        # Invalid deadlines type
        with pytest.raises(ValueError, match="Invalid deadlines field"):
            scraper.validate([{"key": "test", "name": "Test", "deadlines": "invalid"}])

        # Missing deadlines
        with pytest.raises(ValueError, match="Invalid deadlines field"):
            scraper.validate([{"key": "test", "name": "Test"}])
