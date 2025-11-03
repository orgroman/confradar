"""Structured logging configuration for ConfRadar.

This module provides centralized logging configuration with support for:
- Structured JSON logging for production/machine-readable output
- Human-readable console logging for development
- Contextual information (timestamps, levels, module names)
- Integration with Dagster's logging system
- Sensitive data redaction
- Timezone-aware ISO 8601 timestamps
"""

from __future__ import annotations

import logging
import os
import re
import sys
from datetime import datetime, timezone
from typing import Any

from pythonjsonlogger.json import JsonFormatter

from confradar.settings import get_settings

# Package version - avoid circular import
__version__ = "0.1.0"

# Sensitive field patterns for redaction
SENSITIVE_PATTERNS = {
    "api_key",
    "token",
    "password",
    "secret",
    "apikey",
    "api-key",
    "auth",
    "authorization",
    "credential",
}


class SensitiveDataFilter(logging.Filter):
    """Filter to redact sensitive data from log records.
    
    Scans log record attributes and extra fields for sensitive patterns
    and replaces their values with '***REDACTED***'.
    """

    def __init__(self):
        """Initialize the filter with sensitive patterns."""
        super().__init__()
        # Compile patterns for efficient matching
        self.patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in SENSITIVE_PATTERNS
        ]

    def filter(self, record: logging.LogRecord) -> bool:
        """Redact sensitive fields from the log record.
        
        Args:
            record: The log record to modify
            
        Returns:
            True to allow the record to be logged
        """
        # Check all record attributes
        for attr_name in dir(record):
            if attr_name.startswith("_"):
                continue
            
            # Check if attribute name matches sensitive pattern
            if self._is_sensitive(attr_name):
                try:
                    setattr(record, attr_name, "***REDACTED***")
                except (AttributeError, TypeError):
                    # Some attributes are read-only, skip them
                    pass
        
        return True

    def _is_sensitive(self, field_name: str) -> bool:
        """Check if a field name matches sensitive patterns.
        
        Args:
            field_name: The field name to check
            
        Returns:
            True if the field name is sensitive
        """
        for pattern in self.patterns:
            if pattern.search(field_name):
                return True
        return False


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
    timestamp (ISO 8601 with UTC timezone), level, logger name, and message,
    plus any extra fields. Also includes service metadata.
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
        
        # Add ISO 8601 timestamp with UTC timezone
        log_record["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        # Add standard structured fields
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record["module"] = record.module
        log_record["function"] = record.funcName
        log_record["line"] = record.lineno
        
        # Add service metadata
        log_record["service"] = "confradar"
        log_record["version"] = __version__
        
        # Add environment from env var if present
        env = os.getenv("APP_ENV") or os.getenv("ENV") or "development"
        log_record["env"] = env
        
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
    This should be called once at application startup. Idempotent and re-entrant.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                  Case-insensitive. If None, uses settings. Invalid values
                  default to INFO with a warning.
        log_format: Format type ('json' or 'console'). Case-insensitive.
                   If None, uses settings. Invalid values default to 'console'.
        force: If True, force reconfiguration by clearing existing handlers.
              If False (default), skip setup if handlers already exist.
    """
    settings = get_settings()
    
    # Get configuration from settings or parameters
    level = log_level or settings.log_level
    format_type = log_format or settings.log_format
    
    # Validate and normalize log level (case-insensitive)
    level = level.upper()
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    
    if level not in valid_levels:
        print(
            f"WARNING: Invalid LOG_LEVEL '{level}'. Valid values: {valid_levels}. "
            f"Defaulting to INFO.",
            file=sys.stderr,
        )
        level = "INFO"
    
    numeric_level = getattr(logging, level)
    
    # Validate and normalize log format (case-insensitive)
    format_type = format_type.lower()
    valid_formats = {"console", "json"}
    
    if format_type not in valid_formats:
        print(
            f"WARNING: Invalid LOG_FORMAT '{format_type}'. Valid values: {valid_formats}. "
            f"Defaulting to 'console'.",
            file=sys.stderr,
        )
        format_type = "console"
    
    # Get root logger
    root_logger = logging.getLogger()
    
    # Idempotent guard: skip if already configured (unless force=True)
    if root_logger.handlers and not force:
        return
    
    # Remove existing handlers if forcing reconfiguration
    if force:
        root_logger.handlers.clear()
    
    root_logger.setLevel(numeric_level)
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)
    
    # Add sensitive data filter
    sensitive_filter = SensitiveDataFilter()
    handler.addFilter(sensitive_filter)
    
    # Set formatter based on format type
    formatter: logging.Formatter
    if format_type == "json":
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
