# Logging Infrastructure

This document describes the structured logging infrastructure in ConfRadar.

## Overview

ConfRadar uses structured logging to provide consistent, machine-readable logs across the application. The logging system supports both human-readable console output for development and JSON-formatted output for production environments.

## Features

- **Structured JSON Logging**: Machine-readable logs with consistent field names
- **Console Logging**: Human-readable logs for development
- **Contextual Information**: Automatic inclusion of timestamps, levels, module names, functions, and line numbers
- **Context Injection**: Add custom fields (request IDs, user IDs, etc.) to log records
- **Configurable**: Control log level and format via environment variables
- **Integration**: Works seamlessly with Dagster's logging system

## Configuration

Logging is configured via environment variables in `.env` or system environment:

```bash
# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Log format: 'console' (human-readable) or 'json' (structured)
LOG_FORMAT=console
```

### Console Format (Development)

```
2025-11-02 14:30:45 - confradar.scrapers.ai_deadlines - INFO - Scraping AI Deadlines
2025-11-02 14:30:46 - confradar.scrapers.ai_deadlines - WARNING - Failed to parse date: invalid format
```

### JSON Format (Production)

```json
{
  "timestamp": "2025-11-02 14:30:45",
  "level": "INFO",
  "logger": "confradar.scrapers.ai_deadlines",
  "module": "ai_deadlines",
  "function": "parse",
  "line": 42,
  "message": "Scraping AI Deadlines"
}
```

## Usage

### Basic Usage

```python
from confradar import get_logger

logger = get_logger(__name__)

# Log messages at different levels
logger.debug("Detailed debugging information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical failure")
```

### Logging with Extra Fields

```python
logger.info(
    "User action",
    extra={
        "user_id": 123,
        "action": "login",
        "ip_address": "192.168.1.1"
    }
)
```

In JSON format, this produces:

```json
{
  "timestamp": "2025-11-02 14:30:45",
  "level": "INFO",
  "message": "User action",
  "user_id": 123,
  "action": "login",
  "ip_address": "192.168.1.1"
}
```

### Logging with Context

Use context filters to add fields to multiple log messages:

```python
from confradar.logging import add_logging_context, get_logger

logger = get_logger(__name__)

# Add context for request processing
ctx_filter = add_logging_context(request_id="abc123", trace_id="xyz789")
logger.addFilter(ctx_filter)

logger.info("Processing request")  # Includes request_id and trace_id
logger.info("Request completed")   # Also includes request_id and trace_id

# Remove context when done
logger.removeFilter(ctx_filter)
```

### Logging Exceptions

```python
try:
    # Some code that might raise an exception
    process_conference(conf_data)
except Exception as e:
    logger.error("Failed to process conference", exc_info=True)
```

The `exc_info=True` parameter includes the full exception traceback in the log output.

## Integration with Dagster

The logging system integrates with Dagster's built-in logging:

```python
from dagster import asset
from confradar.logging import get_logger

logger = get_logger(__name__)

@asset
def my_asset(context):
    # Use Dagster's context logger for asset logs
    context.log.info("Asset materializing")
    
    # Or use the confradar logger for application logs
    logger.info("Processing data")
    
    return result
```

## Architecture

### Logging Module Structure

```
src/confradar/logging.py
├── setup_logging()        # Configure logging (called at startup)
├── get_logger()          # Get a configured logger instance
├── add_logging_context() # Create context filter for extra fields
├── ContextFilter         # Filter for adding context to log records
└── CustomJsonFormatter   # JSON formatter with standard fields
```

### Initialization

Logging is automatically initialized when you call `get_logger()`. You can also manually initialize it:

```python
from confradar.logging import setup_logging

# Initialize with defaults from settings
setup_logging()

# Or override settings
setup_logging(log_level="DEBUG", log_format="json")
```

The CLI automatically initializes logging at startup.

## Best Practices

### 1. Use Module-Level Loggers

```python
from confradar.logging import get_logger

logger = get_logger(__name__)  # Use __name__ for module-scoped loggers
```

### 2. Choose Appropriate Log Levels

- **DEBUG**: Detailed information for debugging (verbose)
- **INFO**: General informational messages (default)
- **WARNING**: Warning messages for potentially problematic situations
- **ERROR**: Error messages for failures that don't stop execution
- **CRITICAL**: Critical errors that may cause application failure

### 3. Structure Your Log Messages

```python
# Good: Clear, actionable messages
logger.info("Scraped 42 conferences from AI Deadlines")
logger.warning("Missing deadline for conference", extra={"conf_key": "icml-2025"})

# Avoid: Vague messages
logger.info("Done")
logger.warning("Problem")
```

### 4. Use Extra Fields for Structured Data

```python
# Good: Use extra fields for structured data
logger.info(
    "Conference saved to database",
    extra={
        "conf_key": "icml-2025",
        "source": "ai-deadlines",
        "deadline_count": 3
    }
)

# Avoid: Embedding data in message strings
logger.info(f"Saved conf_key=icml-2025 from source=ai-deadlines with 3 deadlines")
```

### 5. Log Exceptions with Context

```python
try:
    result = process_data(data)
except ValueError as e:
    logger.error(
        "Data validation failed",
        exc_info=True,
        extra={
            "data_type": type(data).__name__,
            "data_size": len(data)
        }
    )
    raise
```

## Performance Considerations

### 1. Avoid String Formatting in Hot Paths

```python
# Good: Lazy evaluation
logger.debug("Processing item: %s", item)

# Avoid: Eager evaluation (formats even if DEBUG is disabled)
logger.debug(f"Processing item: {item}")
```

### 2. Use Appropriate Log Levels

Set `LOG_LEVEL=WARNING` or `LOG_LEVEL=ERROR` in production to reduce log volume.

### 3. Limit Extra Fields

Each extra field adds overhead. Include only relevant contextual information.

## Testing

The logging infrastructure includes comprehensive tests:

```bash
# Run logging tests
uv run pytest tests/test_logging.py -v

# Test specific functionality
uv run pytest tests/test_logging.py::TestLoggingSetup -v
```

## Migration Guide

### Migrating Existing Code

Replace standard library logging with structured logging:

```python
# Old
import logging
logger = logging.getLogger(__name__)

# New
from confradar.logging import get_logger
logger = get_logger(__name__)
```

The API is mostly compatible, so existing `logger.info()`, `logger.error()`, etc. calls work without changes.

### Scrapy Spider Logging

Scrapy spiders already have a `self.logger` attribute. You can continue using it:

```python
class MySpider(scrapy.Spider):
    def parse(self, response):
        self.logger.info(f"Parsing {response.url}")
        # Spider's logger works as before
```

## Troubleshooting

### No Logs Appearing

1. Check log level: Ensure `LOG_LEVEL` allows your messages
2. Verify logging is initialized: Call `setup_logging()` early
3. Check handlers: Ensure root logger has handlers

### Duplicate Logs

This can happen if logging is initialized multiple times. Use `force=False` (default) or call `setup_logging()` only once at application startup.

### JSON Logs in Development

If you see JSON logs during development, check your `LOG_FORMAT` setting:

```bash
export LOG_FORMAT=console
```

## Future Enhancements

Planned improvements to the logging infrastructure:

1. **Log Aggregation**: Integration with centralized logging (ELK, CloudWatch, etc.)
2. **Metrics Export**: Convert log events to metrics for monitoring
3. **Sampling**: Reduce log volume in high-throughput scenarios
4. **Sensitive Data Filtering**: Automatically redact sensitive information
5. **Correlation IDs**: Automatic trace ID generation for request tracking
6. **Alert Integration**: Trigger alerts on specific log patterns

## References

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [python-json-logger](https://github.com/madzak/python-json-logger)
- [Dagster Logging](https://docs.dagster.io/concepts/logging)
- [Structured Logging Best Practices](https://www.structlog.org/)
