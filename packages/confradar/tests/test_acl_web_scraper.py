"""Unit tests for ACL Web scraper."""
import pytest
from datetime import date, datetime, timezone

from confradar.scrapers.spiders.acl_web import ACLWebSpider


@pytest.fixture
def spider():
    """Create ACL Web spider instance."""
    return ACLWebSpider()


class TestACLWebSpider:
    """Test ACL Web spider functionality."""
    
    def test_spider_name(self, spider):
        """Test spider has correct name."""
        assert spider.name == "acl_web"
    
    def test_spider_domains(self, spider):
        """Test spider allowed domains."""
        assert "aclweb.org" in spider.allowed_domains
    
    def test_extract_year(self, spider):
        """Test year extraction from text."""
        assert spider._extract_year("EMNLP 2025 Conference") == 2025
        assert spider._extract_year("Workshop 2024") == 2024
        assert spider._extract_year("5 Nov 2025") == 2025
        assert spider._extract_year("No year here") is None
        assert spider._extract_year("") is None
    
    def test_generate_key_with_year(self, spider):
        """Test key generation with year."""
        assert spider._generate_key("EMNLP 2025", 2025) == "emnlp25"
        assert spider._generate_key("ACL", 2024) == "acl24"
        assert spider._generate_key("Workshop on NLP", 2025) == "nlp25"
    
    def test_generate_key_without_year(self, spider):
        """Test key generation without year (should add hash suffix)."""
        key1 = spider._generate_key("NLP Workshop", None)
        key2 = spider._generate_key("NLP Conference", None)
        
        # Should both start with 'nlp' but have different hashes
        assert key1.startswith("nlp_")
        assert key2.startswith("nlp_")
        assert key1 != key2  # Different names should have different keys
        
        # Same name should generate same key
        key3 = spider._generate_key("NLP Workshop", None)
        assert key1 == key3
    
    def test_generate_key_with_acronym(self, spider):
        """Test key generation extracts longest acronym."""
        # Should use longest acronym
        assert spider._generate_key("CRAC 2025 Shared Task", 2025).startswith("crac")
        assert spider._generate_key("DISRPT 2025", 2025).startswith("disrpt")
    
    def test_generate_key_fallback(self, spider):
        """Test key generation fallback for no acronyms."""
        key = spider._generate_key("workshop on topics", 2025)
        assert key == "workshop25"  # Should skip 'on' (common word)
        
        key_no_year = spider._generate_key("workshop on topics", None)
        assert key_no_year.startswith("workshop_")
    
    def test_parse_date_common_formats(self, spider):
        """Test date parsing for common formats."""
        # Format: "15 May 2025"
        dt = spider._parse_date("15 May 2025")
        assert dt is not None
        assert dt.year == 2025
        assert dt.month == 5
        assert dt.day == 15
        assert dt.tzinfo == timezone.utc
        
        # Format: "2 Jun 2025"
        dt = spider._parse_date("2 Jun 2025")
        assert dt is not None
        assert dt.year == 2025
        assert dt.month == 6
        assert dt.day == 2
    
    def test_parse_date_iso_format(self, spider):
        """Test date parsing for ISO format."""
        dt = spider._parse_date("2025-05-15")
        assert dt is not None
        assert dt.year == 2025
        assert dt.month == 5
        assert dt.day == 15
    
    def test_parse_date_invalid(self, spider):
        """Test date parsing returns None for invalid dates."""
        assert spider._parse_date("") is None
        assert spider._parse_date("not a date") is None
        assert spider._parse_date("32 May 2025") is None


class TestACLWebIntegration:
    """Integration tests for ACL Web scraper with real data structure."""
    
    def test_conference_structure(self):
        """Test that conferences have expected structure."""
        from confradar.scrapers.items import ConferenceItem
        
        # Create a sample item
        item = ConferenceItem(
            key="emnlp25",
            name="EMNLP 2025",
            year=2025,
            homepage="https://2025.emnlp.org",
            deadlines=[{
                "kind": "submission",
                "due_date": date(2025, 5, 15),
                "timezone": "AoE",
            }],
            source="acl_web",
            scraped_at=datetime.now(timezone.utc).isoformat(),
            url="https://www.aclweb.org/portal/acl_sponsored_events",
        )
        
        assert item["key"] == "emnlp25"
        assert item["name"] == "EMNLP 2025"
        assert item["year"] == 2025
        assert len(item["deadlines"]) == 1
        assert item["deadlines"][0]["kind"] == "submission"
        assert item["deadlines"][0]["due_date"] == date(2025, 5, 15)
        assert item["deadlines"][0]["timezone"] == "AoE"
