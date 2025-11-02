"""Structured logging configuration for ConfRadar.

This module provides centralized logging configuration with support for:
- Structured JSON logging for production/machine-readable output
- Human-readable console logging for development
- Contextual information (timestamps, levels, module names)
- Integration with Dagster's logging system
"""

from __future__ import annotations

import logging
import sys
from typing import Any

from pythonjsonlogger.json import JsonFormatter

from confradar.settings import get_settings


class ContextFilter(logging.Filter):
    """Add custom context fields to log records.
    
    This filter allows injecting contextual information like request IDs,
    user IDs, or other runtime context into log records.
    """

    def __init__(self, **context: Any):
        """Initialize the filter with context.
        
        Args:
            **context: Key-value pairs to add to log records
        """
        super().__init__()
        self.context = context

    def filter(self, record: logging.LogRecord) -> bool:
        """Add context fields to the log record.
        
        Args:
            record: The log record to modify
            
        Returns:
            True to allow the record to be logged
        """
        for key, value in self.context.items():
            setattr(record, key, value)
        return True


class CustomJsonFormatter(JsonFormatter):
    """Custom JSON formatter with additional fields.
    
    Extends the base JSON formatter to include standard fields like
    timestamp, level, logger name, and message, plus any extra fields.
    """

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        """Add custom fields to the JSON log record.
        
        Args:
            log_record: The JSON log record dictionary to modify
            record: The Python log record
            message_dict: Additional message fields
        """
        super().add_fields(log_record, record, message_dict)
        
        # Add standard fields
        log_record["timestamp"] = self.formatTime(record, self.datefmt)
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["module"] = record.module
        log_record["function"] = record.funcName
        log_record["line"] = record.lineno
        
        # Add exception info if present
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)


def setup_logging(
    log_level: str | None = None,
    log_format: str | None = None,
    force: bool = False,
) -> None:
    """Configure logging for the application.
    
    Sets up logging with either JSON or console format based on configuration.
    This should be called once at application startup.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                  If None, uses settings.
        log_format: Format type ('json' or 'console'). If None, uses settings.
        force: If True, force reconfiguration even if already configured
    """
    settings = get_settings()
    
    # Get configuration from settings or parameters
    level = log_level or settings.log_level
    format_type = log_format or settings.log_format
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Get root logger
    root_logger = logging.getLogger()
    
    # Only configure if not already configured (unless force=True)
    if root_logger.handlers and not force:
        return
    
    # Remove existing handlers if forcing reconfiguration
    if force:
        root_logger.handlers.clear()
    
    root_logger.setLevel(numeric_level)
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)
    
    # Set formatter based on format type
    formatter: logging.Formatter
    if format_type.lower() == "json":
        # JSON formatter for production/machine-readable logs
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(level)s %(logger)s %(message)s"
        )
    else:
        # Console formatter for development/human-readable logs
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    
    # Silence noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name.
    
    This is a convenience wrapper around logging.getLogger that ensures
    logging is configured before returning the logger.
    
    Args:
        name: The name of the logger (typically __name__)
        
    Returns:
        A configured logger instance
    """
    # Ensure logging is set up (idempotent)
    setup_logging()
    return logging.getLogger(name)


def add_logging_context(**context: Any) -> ContextFilter:
    """Create a context filter for adding fields to log records.
    
    Example:
        logger = get_logger(__name__)
        ctx_filter = add_logging_context(request_id="abc123", user_id=42)
        logger.addFilter(ctx_filter)
        logger.info("Processing request")  # Will include request_id and user_id
        logger.removeFilter(ctx_filter)  # Clean up when done
    
    Args:
        **context: Key-value pairs to add to log records
        
    Returns:
        A ContextFilter that can be added to a logger
    """
    return ContextFilter(**context)
