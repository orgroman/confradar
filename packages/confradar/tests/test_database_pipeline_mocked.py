"""Tests for Database pipeline with mocked database."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest

from confradar.scrapers.pipelines import DatabasePipeline


class TestDatabasePipelineMocked:
    """Test database pipeline with mocked database."""
    
    @pytest.fixture
    def mock_spider(self):
        """Create a mock spider."""
        spider = Mock()
        spider.logger = Mock()
        return spider
    
    @pytest.fixture
    def pipeline(self):
        """Create a database pipeline."""
        return DatabasePipeline()
    
    def test_init(self, pipeline):
        """Test pipeline initialization."""
        assert pipeline.session is None
    
    def test_open_spider(self, pipeline, mock_spider):
        """Test opening spider initializes session."""
        with patch("confradar.scrapers.pipelines.get_session") as mock_get_session:
            mock_session = Mock()
            mock_get_session.return_value = mock_session
            
            pipeline.open_spider(mock_spider)
            
            assert pipeline.session == mock_session
            mock_get_session.assert_called_once()
    
    def test_close_spider(self, pipeline, mock_spider):
        """Test closing spider closes session."""
        mock_session = Mock()
        pipeline.session = mock_session
        
        pipeline.close_spider(mock_spider)
        
        mock_session.close.assert_called_once()
    
    def test_close_spider_without_session(self, pipeline, mock_spider):
        """Test closing spider with no session doesn't error."""
        pipeline.session = None
        # Should not raise
        pipeline.close_spider(mock_spider)
    
    def test_process_item_without_session(self, pipeline, mock_spider):
        """Test processing item without session raises error."""
        pipeline.session = None
        item = {"key": "test", "name": "Test Conference"}
        
        with pytest.raises(RuntimeError, match="Database session not initialized"):
            pipeline.process_item(item, mock_spider)
    
    def test_process_item_new_conference(self, pipeline, mock_spider):
        """Test processing item creates new conference."""
        with patch("confradar.scrapers.pipelines.get_session") as mock_get_session:
            mock_session = MagicMock()
            mock_get_session.return_value = mock_session
            pipeline.open_spider(mock_spider)
            
            # Mock query to return no existing conference
            mock_session.query.return_value.filter_by.return_value.first.return_value = None
            
            # Mock Conference and Source classes
            with patch("confradar.scrapers.pipelines.Conference") as MockConference:
                with patch("confradar.scrapers.pipelines.Source") as MockSource:
                    mock_conf = Mock()
                    mock_conf.id = 1
                    MockConference.return_value = mock_conf
                    
                    mock_source = Mock()
                    mock_source.id = 1
                    MockSource.return_value = mock_source
                    
                    item = {
                        "key": "test_conf",
                        "name": "Test Conference",
                        "homepage": "https://test.com",
                        "url": "https://source.com",
                        "source": "test_scraper",
                        "scraped_at": "2025-01-01",
                        "deadlines": []
                    }
                    
                    result = pipeline.process_item(item, mock_spider)
                    
                    assert result == item
                    mock_session.add.assert_called()
                    mock_session.commit.assert_called()
    
    def test_process_item_with_deadline(self, pipeline, mock_spider):
        """Test processing item with deadline."""
        with patch("confradar.scrapers.pipelines.get_session") as mock_get_session:
            mock_session = MagicMock()
            mock_get_session.return_value = mock_session
            pipeline.open_spider(mock_spider)
            
            # Mock existing conference
            mock_conf = Mock()
            mock_conf.id = 1
            mock_session.query.return_value.filter_by.return_value.first.return_value = mock_conf
            
            with patch("confradar.scrapers.pipelines.Source") as MockSource:
                with patch("confradar.scrapers.pipelines.Deadline") as MockDeadline:
                    mock_source = Mock()
                    mock_source.id = 1
                    MockSource.return_value = mock_source
                    
                    item = {
                        "key": "test_conf",
                        "name": "Test Conference",
                        "url": "https://source.com",
                        "deadlines": [
                            {
                                "kind": "submission",
                                "due_at": "2025-05-20T23:59:59",
                                "timezone": "AoE"
                            }
                        ]
                    }
                    
                    result = pipeline.process_item(item, mock_spider)
                    
                    assert result == item
                    MockDeadline.assert_called()
    
    def test_process_item_invalid_date_skipped(self, pipeline, mock_spider):
        """Test that invalid dates in deadlines are skipped."""
        with patch("confradar.scrapers.pipelines.get_session") as mock_get_session:
            mock_session = MagicMock()
            mock_get_session.return_value = mock_session
            pipeline.open_spider(mock_spider)
            
            mock_conf = Mock()
            mock_conf.id = 1
            mock_session.query.return_value.filter_by.return_value.first.return_value = mock_conf
            
            with patch("confradar.scrapers.pipelines.Source") as MockSource:
                with patch("confradar.scrapers.pipelines.Deadline") as MockDeadline:
                    mock_source = Mock()
                    mock_source.id = 1
                    MockSource.return_value = mock_source
                    
                    item = {
                        "key": "test_conf",
                        "name": "Test Conference",
                        "url": "https://source.com",
                        "deadlines": [
                            {
                                "kind": "submission",
                                "due_at": "invalid-date-format",  # Invalid date
                                "timezone": "AoE"
                            }
                        ]
                    }
                    
                    result = pipeline.process_item(item, mock_spider)
                    
                    # Should skip invalid date and not create deadline
                    assert result == item
                    MockDeadline.assert_not_called()
    
    def test_process_item_integrity_error(self, pipeline, mock_spider):
        """Test handling of database integrity errors."""
        from sqlalchemy.exc import IntegrityError
        
        with patch("confradar.scrapers.pipelines.get_session") as mock_get_session:
            mock_session = MagicMock()
            mock_get_session.return_value = mock_session
            pipeline.open_spider(mock_spider)
            
            # Make commit raise IntegrityError
            mock_session.commit.side_effect = IntegrityError("test", {}, None)
            
            with patch("confradar.scrapers.pipelines.Conference"):
                item = {
                    "key": "test_conf",
                    "name": "Test Conference",
                    "deadlines": []
                }
                
                result = pipeline.process_item(item, mock_spider)
                
                # Should rollback and return item
                assert result == item
                mock_session.rollback.assert_called()
                mock_spider.logger.warning.assert_called()
    
    def test_process_item_general_error(self, pipeline, mock_spider):
        """Test handling of general database errors."""
        with patch("confradar.scrapers.pipelines.get_session") as mock_get_session:
            mock_session = MagicMock()
            mock_get_session.return_value = mock_session
            pipeline.open_spider(mock_spider)
            
            # Make query raise general exception
            mock_session.query.side_effect = RuntimeError("Database error")
            
            item = {
                "key": "test_conf",
                "name": "Test Conference",
                "deadlines": []
            }
            
            with pytest.raises(RuntimeError):
                pipeline.process_item(item, mock_spider)
            
            mock_session.rollback.assert_called()
            mock_spider.logger.error.assert_called()
