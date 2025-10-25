# Scraper Development Guide

This guide explains how to implement new data source scrapers for ConfRadar.

## Architecture Overview

All scrapers inherit from the `Scraper` abstract base class and return `ScrapeResult` objects. This standardized interface enables:
- **Schema versioning** for handling source changes over time
- **Raw data preservation** for debugging and reprocessing
- **Metadata capture** for timestamps, error context, and monitoring
- **Dagster integration** where each scraper becomes a data asset

## The Scraper Interface

```python
from confradar.retrieval.base import Scraper, ScrapeResult

class MySourceScraper(Scraper):
    @property
    def source_name(self) -> str:
        """Unique identifier (e.g., 'aideadlines', 'wikicfp')"""
        return "mysource"
    
    @property
    def schema_version(self) -> str:
        """Current schema version (e.g., '1.0', '2.1')"""
        return "1.0"
    
    def fetch(self, **kwargs) -> Any:
        """Fetch raw data from source (JSON, HTML, PDF, etc.)"""
        # Return raw bytes, dict, or source-specific format
        pass
    
    def parse(self, raw: Any, **kwargs) -> List[Dict[str, Any]]:
        """Parse raw data into normalized conference records"""
        # For LLM-based sources, call LLM here with structured output prompts
        # Return list of dicts matching schema_version
        pass
    
    def validate(self, normalized: List[Dict[str, Any]]) -> None:
        """Validate normalized output (raises ValueError on failure)"""
        for item in normalized:
            if "key" not in item or "name" not in item:
                raise ValueError(f"Missing required fields: {item}")
```

The `scrape()` method orchestrates the pipeline: `fetch()` → `parse()` → `validate()` → wrap in `ScrapeResult`.

## Example: JSON API Scraper

See `confradar/retrieval/ai_deadlines.py` for a complete example:

```python
from confradar.retrieval.base import Scraper, ScrapeResult
import httpx

class AIDeadlinesScraper(Scraper):
    DEFAULT_API = "https://aideadlin.es/api/conferences?sub=AIML"
    
    def __init__(self, api_url: str = DEFAULT_API):
        self._api_url = api_url
    
    @property
    def source_name(self) -> str:
        return "aideadlines"
    
    @property
    def schema_version(self) -> str:
        return "1.0"
    
    def fetch(self, **kwargs) -> List[Dict]:
        api_url = kwargs.get("api_url", self._api_url)
        timeout = kwargs.get("timeout", 20.0)
        
        with httpx.Client(timeout=timeout) as client:
            resp = client.get(api_url)
            resp.raise_for_status()
            return resp.json()
    
    def parse(self, raw: List[Dict], **kwargs) -> List[Dict]:
        return [normalize_record(rec) for rec in raw]
    
    def validate(self, normalized: List[Dict]) -> None:
        for item in normalized:
            if "key" not in item or "name" not in item:
                raise ValueError(f"Missing key/name: {item}")
```

## Schema Versioning

When a source changes format:

1. **Increment schema_version** (e.g., "1.0" → "1.1" for compatible changes, "2.0" for breaking changes)
2. **Update parse() logic** to handle new format
3. **Preserve old parsing** if supporting multiple versions:

```python
def parse(self, raw: Any, **kwargs) -> List[Dict]:
    # Detect format and route to appropriate parser
    if self._is_v2_format(raw):
        return self._parse_v2(raw)
    return self._parse_v1(raw)
```

Raw data is always preserved in `ScrapeResult.raw_data` for reprocessing with updated parsers.

## LLM-Based Scrapers

For unstructured sources (PDFs, complex HTML, images), use the LLM in `parse()`:

```python
from confradar.llm.openai import OpenAIClient

class PDFConferenceScraper(Scraper):
    def __init__(self):
        self.llm = OpenAIClient()
    
    def fetch(self, pdf_url: str, **kwargs) -> bytes:
        # Download PDF
        response = httpx.get(pdf_url)
        return response.content
    
    def parse(self, raw: bytes, **kwargs) -> List[Dict]:
        # Extract text, call LLM for structured output
        text = extract_text_from_pdf(raw)
        
        prompt = f"""Extract conference information:
        - Conference name
        - Key deadlines (submission, notification, camera-ready)
        - Location and dates
        
        Text: {text}
        """
        
        response = self.llm.complete(prompt, response_format="json_object")
        return [response.content]  # Parse JSON response
```

## Vision-Based Scrapers

For image-based sources (screenshots, infographics):

```python
def parse(self, raw: bytes, **kwargs) -> List[Dict]:
    # Use vision-capable model
    response = self.llm.complete(
        prompt="Extract conference deadlines from this image",
        images=[raw],
        response_format="json_object"
    )
    return [response.content]
```

## Testing Scrapers

### Unit Tests (Mock HTTP)

```python
def test_scraper_with_mock(monkeypatch):
    class FakeResponse:
        def raise_for_status(self): pass
        def json(self): return [{"title": "Test Conf"}]
    
    class FakeClient:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def get(self, url, **kwargs): return FakeResponse()
    
    monkeypatch.setattr(httpx, "Client", FakeClient)
    
    scraper = MySourceScraper()
    result = scraper.scrape()
    assert result.source_name == "mysource"
    assert len(result.normalized) > 0
```

### Integration Tests (Real HTTP)

```python
@pytest.mark.integration
def test_scraper_real_http():
    scraper = MySourceScraper()
    result = scraper.scrape()
    
    # Verify structure
    assert result.source_name == "mysource"
    assert result.schema_version == "1.0"
    assert isinstance(result.normalized, list)
    assert result.raw_data is not None
```

Run integration tests separately: `uv run pytest -m integration`

## Dagster Integration

Each scraper becomes a Dagster asset:

```python
from dagster import asset
from confradar.retrieval.ai_deadlines import AIDeadlinesScraper

@asset
def ai_deadlines_conferences() -> List[Dict]:
    """Fetch conferences from AI Deadlines."""
    scraper = AIDeadlinesScraper()
    result = scraper.scrape()
    return result.normalized

@asset
def wikicfp_conferences() -> List[Dict]:
    """Fetch conferences from WikiCFP."""
    scraper = WikiCFPScraper()
    result = scraper.scrape()
    return result.normalized

@asset
def merged_conferences(
    ai_deadlines_conferences: List[Dict],
    wikicfp_conferences: List[Dict]
) -> None:
    """Merge and deduplicate conferences from multiple sources."""
    all_confs = ai_deadlines_conferences + wikicfp_conferences
    # Dedupe logic, write to DB
```

## Error Handling

Scrapers should raise exceptions for failures:
- **Network errors**: Let httpx raise (Dagster will retry)
- **Parsing errors**: Raise `ValueError` with details
- **Validation errors**: Raise `ValueError` in `validate()`

```python
def parse(self, raw: Any, **kwargs) -> List[Dict]:
    if not isinstance(raw, list):
        raise ValueError(f"Expected list, got {type(raw)}")
    
    try:
        return [normalize_record(rec) for rec in raw]
    except Exception as e:
        raise ValueError(f"Parse failed: {e}") from e
```

## Metadata Best Practices

Include useful metadata in your scraper:

```python
def scrape(self, **kwargs) -> ScrapeResult:
    result = super().scrape(**kwargs)
    result.metadata.update({
        "record_count": len(result.normalized),
        "source_url": self._api_url,
        "rate_limit_remaining": response.headers.get("X-RateLimit-Remaining"),
        "content_hash": hashlib.sha256(str(result.raw_data).encode()).hexdigest(),
    })
    return result
```

## Next Steps

1. **Implement your scraper** following the examples
2. **Add unit tests** with mocked HTTP
3. **Add integration test** (mark with `@pytest.mark.integration`)
4. **Document source-specific quirks** in scraper docstring
5. **Create Dagster asset** once scraper is stable

See existing scrapers in `packages/confradar/src/confradar/retrieval/` for reference.
