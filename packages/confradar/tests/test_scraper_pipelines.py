"""Tests for Scrapy pipelines."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from confradar.scrapers.pipelines import DeduplicationPipeline, ValidationPipeline


class TestValidationPipeline:
    """Test ValidationPipeline."""
    
    def test_validate_with_required_fields(self):
        """Test validation passes with required fields."""
        pipeline = ValidationPipeline()
        spider = Mock()
        
        item = {"key": "conf1", "name": "Conference 1"}
        result = pipeline.process_item(item, spider)
        
        assert result["key"] == "conf1"
        assert result["name"] == "Conference 1"
        assert "deadlines" in result
        assert result["deadlines"] == []
    
    def test_validate_missing_key(self):
        """Test validation fails when key is missing."""
        pipeline = ValidationPipeline()
        spider = Mock()
        
        item = {"name": "Conference 1"}
        
        with pytest.raises(ValueError, match="Missing required field: key"):
            pipeline.process_item(item, spider)
    
    def test_validate_missing_name(self):
        """Test validation fails when name is missing."""
        pipeline = ValidationPipeline()
        spider = Mock()
        
        item = {"key": "conf1"}
        
        with pytest.raises(ValueError, match="Missing required field: name"):
            pipeline.process_item(item, spider)
    
    def test_validate_empty_key(self):
        """Test validation fails when key is empty."""
        pipeline = ValidationPipeline()
        spider = Mock()
        
        item = {"key": "", "name": "Conference 1"}
        
        with pytest.raises(ValueError, match="Missing required field: key"):
            pipeline.process_item(item, spider)
    
    def test_validate_empty_name(self):
        """Test validation fails when name is empty."""
        pipeline = ValidationPipeline()
        spider = Mock()
        
        item = {"key": "conf1", "name": ""}
        
        with pytest.raises(ValueError, match="Missing required field: name"):
            pipeline.process_item(item, spider)
    
    def test_validate_adds_empty_deadlines(self):
        """Test that empty deadlines list is added if not present."""
        pipeline = ValidationPipeline()
        spider = Mock()
        
        item = {"key": "conf1", "name": "Conference 1"}
        result = pipeline.process_item(item, spider)
        
        assert "deadlines" in result
        assert result["deadlines"] == []
    
    def test_validate_preserves_existing_deadlines(self):
        """Test that existing deadlines are preserved."""
        pipeline = ValidationPipeline()
        spider = Mock()
        
        item = {
            "key": "conf1",
            "name": "Conference 1",
            "deadlines": [{"kind": "submission", "due_at": "2025-05-20"}]
        }
        result = pipeline.process_item(item, spider)
        
        assert len(result["deadlines"]) == 1
        assert result["deadlines"][0]["kind"] == "submission"


class TestDeduplicationPipeline:
    """Test DeduplicationPipeline."""
    
    def test_dedup_allows_first_item(self):
        """Test that first item with a key is allowed."""
        pipeline = DeduplicationPipeline()
        spider = Mock()
        pipeline.open_spider(spider)
        
        item = {"key": "conf1", "name": "Conference 1"}
        result = pipeline.process_item(item, spider)
        
        assert result["key"] == "conf1"
    
    def test_dedup_rejects_duplicate_key(self):
        """Test that duplicate key is rejected."""
        pipeline = DeduplicationPipeline()
        spider = Mock()
        pipeline.open_spider(spider)
        
        item1 = {"key": "conf1", "name": "Conference 1"}
        pipeline.process_item(item1, spider)
        
        item2 = {"key": "conf1", "name": "Conference 1 Duplicate"}
        
        with pytest.raises(ValueError, match="Duplicate conference key: conf1"):
            pipeline.process_item(item2, spider)
    
    def test_dedup_allows_different_keys(self):
        """Test that different keys are allowed."""
        pipeline = DeduplicationPipeline()
        spider = Mock()
        pipeline.open_spider(spider)
        
        item1 = {"key": "conf1", "name": "Conference 1"}
        result1 = pipeline.process_item(item1, spider)
        
        item2 = {"key": "conf2", "name": "Conference 2"}
        result2 = pipeline.process_item(item2, spider)
        
        assert result1["key"] == "conf1"
        assert result2["key"] == "conf2"
    
    def test_dedup_resets_on_spider_open(self):
        """Test that seen keys are reset when spider opens."""
        pipeline = DeduplicationPipeline()
        spider = Mock()
        
        # Add a key
        pipeline.open_spider(spider)
        item = {"key": "conf1", "name": "Conference 1"}
        pipeline.process_item(item, spider)
        
        # Reset by opening spider again
        pipeline.open_spider(spider)
        
        # Same key should be allowed after reset
        item2 = {"key": "conf1", "name": "Conference 1"}
        result = pipeline.process_item(item2, spider)
        
        assert result["key"] == "conf1"
    
    def test_dedup_multiple_items(self):
        """Test deduplication with multiple items."""
        pipeline = DeduplicationPipeline()
        spider = Mock()
        pipeline.open_spider(spider)
        
        items = [
            {"key": "conf1", "name": "Conference 1"},
            {"key": "conf2", "name": "Conference 2"},
            {"key": "conf3", "name": "Conference 3"}
        ]
        
        for item in items:
            result = pipeline.process_item(item, spider)
            assert "key" in result
        
        # Try to add duplicate
        duplicate = {"key": "conf2", "name": "Duplicate"}
        with pytest.raises(ValueError, match="Duplicate conference key: conf2"):
            pipeline.process_item(duplicate, spider)
    
    def test_dedup_init_state(self):
        """Test initial state of deduplication pipeline."""
        pipeline = DeduplicationPipeline()
        
        assert hasattr(pipeline, "seen_keys")
        assert isinstance(pipeline.seen_keys, set)
        assert len(pipeline.seen_keys) == 0
