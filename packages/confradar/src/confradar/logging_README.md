# Logging Infrastructure

This module provides structured logging for the ConfRadar project.

## Quick Start

```python
from confradar import get_logger

logger = get_logger(__name__)
logger.info("Hello, world!")
```

## Features

- 📊 **Structured JSON** logging for production
- 🖥️ **Console** logging for development
- ⚙️ **Configurable** via environment variables
- 🏷️ **Context injection** for request tracking
- 🔗 **Dagster integration** ready
- ✨ **100% test coverage**

## Configuration

```bash
# In .env or environment
LOG_LEVEL=INFO      # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=console  # 'console' or 'json'
```

## Examples

### Basic Logging

```python
from confradar import get_logger

logger = get_logger(__name__)

logger.debug("Detailed debug info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical failure")
```

### Structured Fields

```python
logger.info(
    "Conference processed",
    extra={
        "conf_key": "icml-2025",
        "source": "ai-deadlines",
        "deadline_count": 3
    }
)
```

**JSON Output:**
```json
{
  "timestamp": "2025-11-02 14:30:45",
  "level": "INFO",
  "message": "Conference processed",
  "conf_key": "icml-2025",
  "source": "ai-deadlines",
  "deadline_count": 3
}
```

### Context Injection

```python
from confradar.logging import add_logging_context

# Add context for multiple log messages
ctx_filter = add_logging_context(request_id="abc123", user_id=42)
logger.addFilter(ctx_filter)

logger.info("Processing request")  # Includes request_id and user_id
logger.info("Request completed")   # Also includes context

logger.removeFilter(ctx_filter)  # Clean up
```

### Exception Logging

```python
try:
    process_data(data)
except Exception as e:
    logger.error("Failed to process", exc_info=True)
```

## Documentation

- 📖 [Complete Documentation](../../../docs/LOGGING.md)
- 🏗️ [Architecture](../../../wiki/Architecture.md#monitoring--observability)
- 💻 [Development Guide](../../../wiki/Development-Guide.md#logging)

## Testing

```bash
# Run logging tests
uv run pytest tests/test_logging.py -v

# Check coverage
uv run pytest tests/test_logging.py --cov=confradar.logging
```

## Module API

### Functions

- **`setup_logging(log_level=None, log_format=None, force=False)`**  
  Configure logging for the application. Called automatically by `get_logger()`.

- **`get_logger(name)`**  
  Get a configured logger instance. Use `__name__` as the name.

- **`add_logging_context(**context)`**  
  Create a context filter for adding fields to log records.

### Classes

- **`ContextFilter`**  
  Filter for adding custom context fields to log records.

- **`CustomJsonFormatter`**  
  JSON formatter with standard fields (timestamp, level, logger, module, function, line).

## Integration

### With Dagster

```python
from dagster import asset
from confradar import get_logger

logger = get_logger(__name__)

@asset
def my_asset(context):
    # Use Dagster's context logger
    context.log.info("Asset materializing")
    
    # Or use confradar logger
    logger.info("Processing data")
```

### With CLI

Logging is automatically initialized when the CLI starts. No additional setup needed.

## Best Practices

1. **Use module-level loggers**: `logger = get_logger(__name__)`
2. **Choose appropriate levels**: DEBUG < INFO < WARNING < ERROR < CRITICAL
3. **Structure your data**: Use `extra={}` for structured fields
4. **Log exceptions**: Use `exc_info=True` to include tracebacks
5. **Add context**: Use context filters for request/trace IDs

## Performance Tips

- Avoid string formatting in hot paths: `logger.debug("Item: %s", item)`
- Set higher log levels in production: `LOG_LEVEL=WARNING`
- Limit extra fields to relevant context only

## License

MIT - See LICENSE file for details
