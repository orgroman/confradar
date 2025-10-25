from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class ScrapeResult:
    """Result from a scraper execution.
    
    Attributes:
        source_name: Identifier for the source (e.g., 'aideadlines', 'wikicfp')
        schema_version: Version string for normalized data schema (e.g., '1.0')
        scraped_at: UTC timestamp when data was retrieved
        raw_data: Original response (JSON/HTML/etc.) for debugging and reprocessing
        normalized: List of normalized conference items (schema-versioned)
        metadata: Optional fields (e.g., record count, API rate limits, error context)
    """

    source_name: str
    schema_version: str
    scraped_at: datetime
    raw_data: Any
    normalized: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)


class Scraper(ABC):
    """Abstract base for all scrapers.
    
    Each source (AI Deadlines, WikiCFP, PDFs, etc.) implements this interface.
    Supports:
    - Dagster integration (each scraper = asset returning ScrapeResult)
    - LLM-based extraction (override parse with LLM calls)
    - Schema evolution (raw data preserved; normalized output versioned)
    - Robust error handling (network, parsing, schema drift)
    
    Typical flow:
        1. fetch() -> raw bytes/JSON/HTML
        2. parse(raw) -> normalized list of dicts
        3. validate(normalized) -> check required fields
        4. Return ScrapeResult with raw + normalized + metadata
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Unique identifier for this source."""
        pass

    @property
    @abstractmethod
    def schema_version(self) -> str:
        """Current schema version for normalized output."""
        pass

    @abstractmethod
    def fetch(self, **kwargs: Any) -> Any:
        """Fetch raw data from the source.
        
        Returns raw bytes, JSON, HTML, or any source-specific format.
        Raises exceptions on network/auth failures (let Airflow handle retries).
        """
        pass

    @abstractmethod
    def parse(self, raw: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        """Parse raw data into normalized conference records.
        
        For LLM-based sources, this calls the LLM with structured output prompts.
        For JSON APIs, this maps fields to the schema.
        Returns list of dicts matching schema_version.
        """
        pass

    def validate(self, normalized: List[Dict[str, Any]]) -> None:
        """Validate normalized output against schema expectations.
        
        Override to add source-specific validation.
        Raises ValueError if schema is violated.
        """
        for item in normalized:
            if not isinstance(item, dict):
                raise ValueError(f"Expected dict, got {type(item)}")
            if "key" not in item or "name" not in item:
                raise ValueError(f"Missing required fields: {item}")

    def scrape(self, **kwargs: Any) -> ScrapeResult:
        """Execute full scrape pipeline: fetch -> parse -> validate -> wrap result.
        
        This is the main entry point for Dagster assets.
        """
        scraped_at = datetime.now(timezone.utc)
        raw = self.fetch(**kwargs)
        normalized = self.parse(raw, **kwargs)
        self.validate(normalized)
        
        return ScrapeResult(
            source_name=self.source_name,
            schema_version=self.schema_version,
            scraped_at=scraped_at,
            raw_data=raw,
            normalized=normalized,
            metadata={"count": len(normalized)},
        )
