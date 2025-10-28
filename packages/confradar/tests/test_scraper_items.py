"""Tests for Scrapy items."""

from __future__ import annotations

import pytest
import scrapy

from confradar.scrapers.items import ConferenceItem


def test_conference_item_fields():
    """Test that ConferenceItem has all expected fields."""
    item = ConferenceItem()
    
    # Test that all fields exist
    assert "key" in item.fields
    assert "name" in item.fields
    assert "year" in item.fields
    assert "homepage" in item.fields
    assert "deadlines" in item.fields
    assert "source" in item.fields
    assert "scraped_at" in item.fields
    assert "url" in item.fields


def test_conference_item_set_values():
    """Test setting values on ConferenceItem."""
    item = ConferenceItem()
    
    item["key"] = "neurips2025"
    item["name"] = "NeurIPS 2025"
    item["year"] = 2025
    item["homepage"] = "https://neurips.cc"
    item["deadlines"] = [{"kind": "submission", "due_at": "2025-05-20"}]
    item["source"] = "ai_deadlines"
    item["scraped_at"] = "2025-01-01T00:00:00Z"
    item["url"] = "https://aideadlin.es"
    
    assert item["key"] == "neurips2025"
    assert item["name"] == "NeurIPS 2025"
    assert item["year"] == 2025
    assert item["homepage"] == "https://neurips.cc"
    assert len(item["deadlines"]) == 1
    assert item["source"] == "ai_deadlines"
    assert item["scraped_at"] == "2025-01-01T00:00:00Z"
    assert item["url"] == "https://aideadlin.es"


def test_conference_item_empty_creation():
    """Test creating an empty ConferenceItem."""
    item = ConferenceItem()
    
    # Should be able to create without setting any fields
    assert isinstance(item, scrapy.Item)


def test_conference_item_partial_fields():
    """Test ConferenceItem with only required fields."""
    item = ConferenceItem()
    item["key"] = "acl2026"
    item["name"] = "ACL 2026"
    
    assert item["key"] == "acl2026"
    assert item["name"] == "ACL 2026"
    
    # Optional fields should not be set
    assert "year" not in item
    assert "homepage" not in item


def test_conference_item_get_with_default():
    """Test getting fields with default values."""
    item = ConferenceItem()
    
    # Get non-existent field with default
    assert item.get("key", "default") == "default"
    
    # Set a field and get it
    item["key"] = "test"
    assert item.get("key", "default") == "test"


def test_conference_item_multiple_deadlines():
    """Test ConferenceItem with multiple deadlines."""
    item = ConferenceItem()
    item["key"] = "conf"
    item["name"] = "Conference"
    item["deadlines"] = [
        {"kind": "submission", "due_at": "2025-05-20"},
        {"kind": "notification", "due_at": "2025-07-15"},
        {"kind": "camera_ready", "due_at": "2025-08-30"}
    ]
    
    assert len(item["deadlines"]) == 3
    assert item["deadlines"][0]["kind"] == "submission"
    assert item["deadlines"][1]["kind"] == "notification"
    assert item["deadlines"][2]["kind"] == "camera_ready"
