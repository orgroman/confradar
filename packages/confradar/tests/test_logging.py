"""Tests for structured logging configuration."""

import json
import logging
from io import StringIO

import pytest

from confradar.logging import (
    ContextFilter,
    CustomJsonFormatter,
    add_logging_context,
    get_logger,
    setup_logging,
)


class TestLoggingSetup:
    """Tests for logging setup and configuration."""

    def test_setup_logging_console_format(self):
        """Test that console format logging is set up correctly."""
        setup_logging(log_level="INFO", log_format="console", force=True)
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO
        assert len(root_logger.handlers) > 0
        
        # Check that handler has console formatter
        handler = root_logger.handlers[0]
        assert isinstance(handler.formatter, logging.Formatter)
        assert "%(asctime)s" in handler.formatter._fmt

    def test_setup_logging_json_format(self):
        """Test that JSON format logging is set up correctly."""
        setup_logging(log_level="DEBUG", log_format="json", force=True)
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG
        
        # Check that handler has JSON formatter
        handler = root_logger.handlers[0]
        assert isinstance(handler.formatter, CustomJsonFormatter)

    def test_setup_logging_different_levels(self):
        """Test that different log levels are configured correctly."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            setup_logging(log_level=level, force=True)
            root_logger = logging.getLogger()
            assert root_logger.level == getattr(logging, level)

    def test_setup_logging_idempotent(self):
        """Test that setup_logging is idempotent when force=False."""
        setup_logging(log_level="INFO", force=True)
        handler_count_1 = len(logging.getLogger().handlers)
        
        # Call again without force - should not add more handlers
        setup_logging(log_level="DEBUG", force=False)
        handler_count_2 = len(logging.getLogger().handlers)
        
        assert handler_count_1 == handler_count_2


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_logger(self):
        """Test that get_logger returns a logger instance."""
        logger = get_logger(__name__)
        assert isinstance(logger, logging.Logger)
        assert logger.name == __name__

    def test_get_logger_ensures_setup(self):
        """Test that get_logger ensures logging is set up."""
        # Clear all handlers to simulate uninitialized state
        root = logging.getLogger()
        root.handlers.clear()
        
        # Get logger should set up logging
        logger = get_logger("test")
        assert len(root.handlers) > 0


class TestContextFilter:
    """Tests for ContextFilter."""

    def test_context_filter_adds_fields(self):
        """Test that ContextFilter adds context fields to log records."""
        ctx_filter = ContextFilter(request_id="abc123", user_id=42)
        
        # Create a dummy log record
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        
        # Apply filter
        ctx_filter.filter(record)
        
        # Check that context fields were added
        assert hasattr(record, "request_id")
        assert record.request_id == "abc123"
        assert hasattr(record, "user_id")
        assert record.user_id == 42

    def test_add_logging_context(self):
        """Test add_logging_context helper function."""
        ctx_filter = add_logging_context(session="xyz789", operation="test_op")
        
        assert isinstance(ctx_filter, ContextFilter)
        assert ctx_filter.context["session"] == "xyz789"
        assert ctx_filter.context["operation"] == "test_op"


class TestCustomJsonFormatter:
    """Tests for CustomJsonFormatter."""

    def test_json_formatter_output(self):
        """Test that JSON formatter produces valid JSON output."""
        setup_logging(log_level="INFO", log_format="json", force=True)
        
        # Capture log output
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(
            CustomJsonFormatter("%(timestamp)s %(level)s %(logger)s %(message)s")
        )
        
        logger = logging.getLogger("test_json")
        logger.handlers = [handler]
        logger.setLevel(logging.INFO)
        
        # Log a message
        logger.info("Test message")
        
        # Parse output as JSON
        output = stream.getvalue().strip()
        log_data = json.loads(output)
        
        # Check required fields
        assert "timestamp" in log_data
        assert "level" in log_data
        assert log_data["level"] == "INFO"
        assert "logger" in log_data
        assert log_data["logger"] == "test_json"
        assert "message" in log_data
        assert log_data["message"] == "Test message"
        assert "module" in log_data
        assert "function" in log_data
        assert "line" in log_data

    def test_json_formatter_with_extra_fields(self):
        """Test that JSON formatter includes extra fields."""
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(
            CustomJsonFormatter("%(timestamp)s %(level)s %(message)s")
        )
        
        logger = logging.getLogger("test_extra")
        logger.handlers = [handler]
        logger.setLevel(logging.INFO)
        
        # Log with extra fields
        logger.info("Test with extras", extra={"custom_field": "custom_value", "count": 123})
        
        output = stream.getvalue().strip()
        log_data = json.loads(output)
        
        # Check extra fields are included
        assert "custom_field" in log_data
        assert log_data["custom_field"] == "custom_value"
        assert "count" in log_data
        assert log_data["count"] == 123

    def test_json_formatter_with_exception(self):
        """Test that JSON formatter includes exception information."""
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(
            CustomJsonFormatter("%(timestamp)s %(level)s %(message)s")
        )
        
        logger = logging.getLogger("test_exc")
        logger.handlers = [handler]
        logger.setLevel(logging.ERROR)
        
        # Log an exception
        try:
            raise ValueError("Test error")
        except ValueError:
            logger.error("Exception occurred", exc_info=True)
        
        output = stream.getvalue().strip()
        log_data = json.loads(output)
        
        # Check exception info is included
        assert "exc_info" in log_data
        assert "ValueError" in log_data["exc_info"]
        assert "Test error" in log_data["exc_info"]


class TestLoggingIntegration:
    """Integration tests for logging functionality."""

    def test_logger_with_context(self):
        """Test using logger with context filter."""
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(
            CustomJsonFormatter("%(timestamp)s %(level)s %(message)s")
        )
        
        logger = logging.getLogger("test_context")
        logger.handlers = [handler]
        logger.setLevel(logging.INFO)
        
        # Add context filter
        ctx_filter = add_logging_context(request_id="req123", trace_id="trace456")
        logger.addFilter(ctx_filter)
        
        # Log message
        logger.info("Processing request")
        
        # Check output
        output = stream.getvalue().strip()
        log_data = json.loads(output)
        
        assert log_data["request_id"] == "req123"
        assert log_data["trace_id"] == "trace456"
        assert log_data["message"] == "Processing request"
        
        # Remove filter
        logger.removeFilter(ctx_filter)

    def test_multiple_loggers(self):
        """Test that multiple loggers work correctly."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        assert logger1.name == "module1"
        assert logger2.name == "module2"
        assert logger1 is not logger2
