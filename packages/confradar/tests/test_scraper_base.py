"""Tests for base scraper classes."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from confradar.scrapers.base import ScrapeResult, Scraper


class TestScrapeResult:
    """Test ScrapeResult dataclass."""
    
    def test_scrape_result_creation(self):
        """Test creating a ScrapeResult."""
        now = datetime.now(timezone.utc)
        result = ScrapeResult(
            source_name="test_source",
            schema_version="1.0",
            scraped_at=now,
            raw_data={"key": "value"},
            normalized=[{"key": "conf1", "name": "Conference 1"}],
            metadata={"count": 1}
        )
        
        assert result.source_name == "test_source"
        assert result.schema_version == "1.0"
        assert result.scraped_at == now
        assert result.raw_data == {"key": "value"}
        assert len(result.normalized) == 1
        assert result.metadata["count"] == 1
    
    def test_scrape_result_default_metadata(self):
        """Test ScrapeResult with default metadata."""
        result = ScrapeResult(
            source_name="test",
            schema_version="1.0",
            scraped_at=datetime.now(timezone.utc),
            raw_data={},
            normalized=[]
        )
        
        assert result.metadata == {}


class MockScraper(Scraper):
    """Mock scraper implementation for testing."""
    
    def __init__(self):
        self._source_name = "mock_scraper"
        self._schema_version = "1.0"
        self._raw_data = {"test": "data"}
        self._normalized = [{"key": "conf1", "name": "Conference 1"}]
    
    @property
    def source_name(self) -> str:
        return self._source_name
    
    @property
    def schema_version(self) -> str:
        return self._schema_version
    
    def fetch(self, **kwargs):
        return self._raw_data
    
    def parse(self, raw, **kwargs):
        return self._normalized


class TestScraper:
    """Test Scraper abstract base class."""
    
    def test_scraper_requires_implementation(self):
        """Test that Scraper cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Scraper()
    
    def test_mock_scraper_properties(self):
        """Test mock scraper properties."""
        scraper = MockScraper()
        assert scraper.source_name == "mock_scraper"
        assert scraper.schema_version == "1.0"
    
    def test_scraper_fetch(self):
        """Test scraper fetch method."""
        scraper = MockScraper()
        raw = scraper.fetch()
        assert raw == {"test": "data"}
    
    def test_scraper_parse(self):
        """Test scraper parse method."""
        scraper = MockScraper()
        normalized = scraper.parse({})
        assert len(normalized) == 1
        assert normalized[0]["key"] == "conf1"
    
    def test_scraper_validate_success(self):
        """Test validation with valid data."""
        scraper = MockScraper()
        normalized = [
            {"key": "conf1", "name": "Conference 1"},
            {"key": "conf2", "name": "Conference 2"}
        ]
        # Should not raise
        scraper.validate(normalized)
    
    def test_scraper_validate_missing_key(self):
        """Test validation fails on missing key field."""
        scraper = MockScraper()
        normalized = [{"name": "Conference 1"}]
        
        with pytest.raises(ValueError, match="Missing required fields"):
            scraper.validate(normalized)
    
    def test_scraper_validate_missing_name(self):
        """Test validation fails on missing name field."""
        scraper = MockScraper()
        normalized = [{"key": "conf1"}]
        
        with pytest.raises(ValueError, match="Missing required fields"):
            scraper.validate(normalized)
    
    def test_scraper_validate_not_dict(self):
        """Test validation fails on non-dict items."""
        scraper = MockScraper()
        normalized = ["not a dict"]
        
        with pytest.raises(ValueError, match="Expected dict"):
            scraper.validate(normalized)
    
    def test_scraper_scrape_full_pipeline(self):
        """Test full scrape pipeline."""
        scraper = MockScraper()
        result = scraper.scrape()
        
        assert isinstance(result, ScrapeResult)
        assert result.source_name == "mock_scraper"
        assert result.schema_version == "1.0"
        assert result.raw_data == {"test": "data"}
        assert len(result.normalized) == 1
        assert result.metadata["count"] == 1
    
    def test_scraper_scrape_with_kwargs(self):
        """Test scrape with keyword arguments."""
        class KwargScraper(MockScraper):
            def fetch(self, **kwargs):
                return {"fetched_with": kwargs.get("param")}
            
            def parse(self, raw, **kwargs):
                return [{"key": "conf", "name": kwargs.get("param", "default")}]
        
        scraper = KwargScraper()
        result = scraper.scrape(param="test_value")
        
        assert result.raw_data == {"fetched_with": "test_value"}
        assert result.normalized[0]["name"] == "test_value"
    
    def test_scraper_scrape_validation_failure(self):
        """Test that scrape fails on validation error."""
        class InvalidScraper(MockScraper):
            def parse(self, raw, **kwargs):
                return [{"key": "conf"}]  # Missing 'name'
        
        scraper = InvalidScraper()
        with pytest.raises(ValueError, match="Missing required fields"):
            scraper.scrape()
