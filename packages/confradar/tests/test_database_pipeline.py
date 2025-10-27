"""Integration tests for DatabasePipeline with PostgreSQL."""

from datetime import datetime

import pytest

from confradar.db.base import session_scope
from confradar.db.models import Conference
from confradar.scrapers.pipelines import DatabasePipeline, DeduplicationPipeline, ValidationPipeline


@pytest.fixture
def db_pipeline():
    """Create a database pipeline instance."""
    pipeline = DatabasePipeline()

    class MockSpider:
        logger = None

        class MockLogger:
            def warning(self, msg):
                print(f"WARNING: {msg}")

            def error(self, msg):
                print(f"ERROR: {msg}")

        logger = MockLogger()

    spider = MockSpider()
    pipeline.open_spider(spider)
    yield pipeline, spider
    pipeline.close_spider(spider)


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Clean up test data before and after each test."""
    test_keys = ["test_conf_1", "test_conf_2", "test_icml_db", "test_neurips_db"]

    def clean():
        with session_scope() as session:
            for key in test_keys:
                conf = session.query(Conference).filter_by(key=key).first()
                if conf:
                    session.delete(conf)
            session.commit()

    clean()  # Before test
    yield
    clean()  # After test


class TestDatabasePipeline:
    """Test database pipeline operations."""

    def test_create_new_conference(self, db_pipeline):
        """Test creating a new conference in the database."""
        pipeline, spider = db_pipeline

        item = {
            "key": "test_icml_db",
            "name": "ICML 2025 (Test)",
            "homepage": "https://icml.cc",
            "url": "https://aideadlines.org",
            "source": "aideadlines",
            "scraped_at": datetime.now().isoformat(),
            "deadlines": [
                {"kind": "submission", "due_at": "2025-02-01T23:59:59", "timezone": "UTC-12"}
            ],
        }

        result = pipeline.process_item(item, spider)
        assert result == item

        # Verify in database
        with session_scope() as session:
            conf = session.query(Conference).filter_by(key="test_icml_db").first()
            assert conf is not None
            assert conf.name == "ICML 2025 (Test)"
            assert conf.homepage == "https://icml.cc"

            # Check source
            assert len(conf.sources) == 1
            assert conf.sources[0].url == "https://aideadlines.org"

            # Check deadline
            assert len(conf.deadlines) == 1
            deadline = conf.deadlines[0]
            assert deadline.kind == "submission"
            assert deadline.timezone == "UTC-12"

    def test_update_existing_conference(self, db_pipeline):
        """Test updating an existing conference."""
        pipeline, spider = db_pipeline

        # Create initial conference
        item1 = {
            "key": "test_conf_1",
            "name": "Test Conference 2025",
            "homepage": "https://example.com",
            "url": "https://source1.com",
            "source": "source1",
            "scraped_at": datetime.now().isoformat(),
            "deadlines": [],
        }
        pipeline.process_item(item1, spider)

        # Update with new name and homepage
        item2 = {
            "key": "test_conf_1",
            "name": "Test Conference 2025 (Updated)",
            "homepage": "https://example.com/new",
            "url": "https://source1.com",
            "source": "source1",
            "scraped_at": datetime.now().isoformat(),
            "deadlines": [],
        }
        pipeline.process_item(item2, spider)

        # Verify update
        with session_scope() as session:
            conf = session.query(Conference).filter_by(key="test_conf_1").first()
            assert conf.name == "Test Conference 2025 (Updated)"
            assert conf.homepage == "https://example.com/new"

            # Should still be only one conference
            count = session.query(Conference).filter_by(key="test_conf_1").count()
            assert count == 1

    def test_multiple_deadlines(self, db_pipeline):
        """Test storing multiple deadlines for a conference."""
        pipeline, spider = db_pipeline

        item = {
            "key": "test_conf_2",
            "name": "Multi-Deadline Conference",
            "homepage": "https://example.com",
            "url": "https://aideadlines.org",
            "source": "aideadlines",
            "scraped_at": datetime.now().isoformat(),
            "deadlines": [
                {"kind": "abstract", "due_at": "2025-01-15T23:59:59", "timezone": "UTC-12"},
                {"kind": "submission", "due_at": "2025-01-22T23:59:59", "timezone": "UTC-12"},
                {"kind": "notification", "due_at": "2025-03-15T23:59:59", "timezone": "UTC-12"},
            ],
        }

        pipeline.process_item(item, spider)

        # Verify all deadlines stored
        with session_scope() as session:
            conf = session.query(Conference).filter_by(key="test_conf_2").first()
            assert len(conf.deadlines) == 3

            kinds = {d.kind for d in conf.deadlines}
            assert kinds == {"abstract", "submission", "notification"}

    def test_duplicate_deadline_prevention(self, db_pipeline):
        """Test that duplicate deadlines are not created."""
        pipeline, spider = db_pipeline

        item = {
            "key": "test_neurips_db",
            "name": "NeurIPS 2025",
            "homepage": "https://neurips.cc",
            "url": "https://aideadlines.org",
            "source": "aideadlines",
            "scraped_at": datetime.now().isoformat(),
            "deadlines": [
                {"kind": "submission", "due_at": "2025-05-15T23:59:59", "timezone": "UTC-12"}
            ],
        }

        # Process twice
        pipeline.process_item(item, spider)
        pipeline.process_item(item, spider)

        # Verify only one deadline created
        with session_scope() as session:
            conf = session.query(Conference).filter_by(key="test_neurips_db").first()
            assert len(conf.deadlines) == 1

    def test_invalid_date_handling(self, db_pipeline):
        """Test that invalid dates are skipped gracefully."""
        pipeline, spider = db_pipeline

        item = {
            "key": "test_conf_1",
            "name": "Test Conference",
            "homepage": "https://example.com",
            "url": "https://source.com",
            "source": "test",
            "scraped_at": datetime.now().isoformat(),
            "deadlines": [
                {
                    "kind": "submission",
                    "due_at": "invalid-date",  # Invalid format
                    "timezone": "UTC-12",
                }
            ],
        }

        # Should not raise, just skip the invalid deadline
        pipeline.process_item(item, spider)

        # Verify conference created but no deadline
        with session_scope() as session:
            conf = session.query(Conference).filter_by(key="test_conf_1").first()
            assert conf is not None
            assert len(conf.deadlines) == 0


class TestValidationPipeline:
    """Test validation pipeline."""

    def test_requires_key_and_name(self):
        """Test validation requires key and name."""
        pipeline = ValidationPipeline()

        class MockSpider:
            pass

        spider = MockSpider()

        # Valid item
        valid = {"key": "test", "name": "Test", "deadlines": []}
        assert pipeline.process_item(valid, spider) == valid

        # Missing key
        with pytest.raises(ValueError, match="Missing required field: key"):
            pipeline.process_item({"name": "Test"}, spider)

        # Missing name
        with pytest.raises(ValueError, match="Missing required field: name"):
            pipeline.process_item({"key": "test"}, spider)

    def test_adds_empty_deadlines(self):
        """Test that pipeline adds empty deadlines list if missing."""
        pipeline = ValidationPipeline()

        class MockSpider:
            pass

        item = {"key": "test", "name": "Test"}
        result = pipeline.process_item(item, MockSpider())

        assert "deadlines" in result
        assert result["deadlines"] == []


class TestDeduplicationPipeline:
    """Test deduplication pipeline."""

    def test_prevents_duplicate_keys(self):
        """Test that duplicate conference keys are rejected."""
        pipeline = DeduplicationPipeline()

        class MockSpider:
            pass

        spider = MockSpider()
        pipeline.open_spider(spider)

        item1 = {"key": "test1", "name": "Test 1"}
        item2 = {"key": "test2", "name": "Test 2"}
        item3 = {"key": "test1", "name": "Test 1 Duplicate"}

        # First two should pass
        assert pipeline.process_item(item1, spider) == item1
        assert pipeline.process_item(item2, spider) == item2

        # Third should be rejected (duplicate key)
        with pytest.raises(ValueError, match="Duplicate conference key: test1"):
            pipeline.process_item(item3, spider)

    def test_resets_on_spider_open(self):
        """Test that seen keys are reset when spider opens."""
        pipeline = DeduplicationPipeline()

        class MockSpider:
            pass

        spider = MockSpider()

        # First spider run
        pipeline.open_spider(spider)
        item1 = {"key": "test", "name": "Test"}
        pipeline.process_item(item1, spider)

        # New spider run - should reset
        pipeline.open_spider(spider)
        item2 = {"key": "test", "name": "Test"}
        assert pipeline.process_item(item2, spider) == item2  # Should not raise
