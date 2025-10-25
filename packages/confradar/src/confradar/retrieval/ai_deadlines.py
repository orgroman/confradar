from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import httpx

from confradar.retrieval.base import Scraper, ScrapeResult


@dataclass
class DeadlineItem:
    kind: str
    due_at: datetime
    timezone: str | None = None


@dataclass
class ConferenceItem:
    key: str
    name: str
    year: int | None
    homepage: str | None
    deadlines: List[DeadlineItem]


DEFAULT_API = "https://aideadlin.es/api/conferences?sub=AIML"


class AIDeadlinesScraper(Scraper):
    """Scraper for aideadlin.es JSON API.
    
    Schema v1.0: Returns list of conference dicts with key, name, year, 
    homepage, and deadlines list.
    """

    def __init__(self, api_url: str = DEFAULT_API):
        self._api_url = api_url

    @property
    def source_name(self) -> str:
        return "aideadlines"

    @property
    def schema_version(self) -> str:
        return "1.0"

    def fetch(self, **kwargs: Any) -> List[Dict[str, Any]]:
        """Fetch JSON from aideadlin.es API."""
        api_url = kwargs.get("api_url", self._api_url)
        timeout = kwargs.get("timeout", 20.0)
        
        with httpx.Client(timeout=timeout) as client:
            resp = client.get(api_url)
            resp.raise_for_status()
            return resp.json()

    def parse(self, raw: List[Dict[str, Any]], **kwargs: Any) -> List[Dict[str, Any]]:
        """Parse raw JSON into normalized ConferenceItem records."""
        normalized = []
        for rec in raw:
            conf_item = normalize_record(rec)
            # Convert dataclass to dict with datetime serialization
            conf_dict = asdict(conf_item)
            # Convert datetime objects to ISO strings for JSON compatibility
            for dl in conf_dict.get("deadlines", []):
                if isinstance(dl.get("due_at"), datetime):
                    dl["due_at"] = dl["due_at"].isoformat()
            normalized.append(conf_dict)
        return normalized

    def validate(self, normalized: List[Dict[str, Any]]) -> None:
        """Validate normalized output has required fields."""
        for item in normalized:
            if not isinstance(item, dict):
                raise ValueError(f"Expected dict, got {type(item)}")
            if "key" not in item or "name" not in item:
                raise ValueError(f"Missing key/name: {item}")
            if "deadlines" not in item or not isinstance(item["deadlines"], list):
                raise ValueError(f"Invalid deadlines field: {item}")


def fetch_ai_deadlines(api_url: str = DEFAULT_API, *, timeout: float = 20.0) -> list[ConferenceItem]:
    """Fetch and normalize AI Deadlines data (legacy function).
    
    This function maintains backward compatibility with existing code.
    For new code, prefer using AIDeadlinesScraper class directly.
    
    This expects an Open API returning JSON list of conferences. Tests mock httpx to avoid
    real network calls. The schema is normalized to ConferenceItem/DeadlineItem.
    """
    scraper = AIDeadlinesScraper(api_url=api_url)
    result = scraper.scrape(timeout=timeout)
    # Convert dicts back to dataclasses for backward compatibility
    conferences = []
    for item in result.normalized:
        deadlines = [
            DeadlineItem(
                kind=dl["kind"],
                due_at=datetime.fromisoformat(dl["due_at"]) if isinstance(dl["due_at"], str) else dl["due_at"],
                timezone=dl.get("timezone")
            )
            for dl in item["deadlines"]
        ]
        conferences.append(ConferenceItem(
            key=item["key"],
            name=item["name"],
            year=item.get("year"),
            homepage=item.get("homepage"),
            deadlines=deadlines
        ))
    return conferences


def normalize_record(rec: dict[str, Any]) -> ConferenceItem:
    name = rec.get("title") or rec.get("name") or "Unknown"
    key = (rec.get("acronym") or name).lower().replace(" ", "")
    year = None
    for cand in (rec.get("year"), rec.get("date")):
        if isinstance(cand, int):
            year = cand
            break
        if isinstance(cand, str) and cand.isdigit():
            year = int(cand)
            break
    homepage = rec.get("link") or rec.get("homepage")

    deadlines: list[DeadlineItem] = []
    # The API tends to include multiple deadline fields; we map known keys where present
    mapping: list[tuple[str, str]] = [
        ("deadline", "submission"),
        ("abstract_deadline", "abstract"),
        ("notification_due", "notification"),
        ("camera_ready_due", "camera_ready"),
    ]
    for src_key, kind in mapping:
        raw = rec.get(src_key)
        if not raw:
            continue
        dt = _parse_datetime(raw)
        if dt is None:
            continue
        deadlines.append(DeadlineItem(kind=kind, due_at=dt, timezone=_tz_of(raw)))

    return ConferenceItem(key=key, name=name, year=year, homepage=homepage, deadlines=deadlines)


def _parse_datetime(value: str | Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    # Common formats: 2025-05-15 23:59:59 AoE, 2025-05-15 23:59:59 UTC, ISO
    v = value.strip()
    # Try ISO first
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(v, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            pass
    # Fallback: strip trailing token (e.g., AoE) and parse
    parts = v.split()
    try_vals: Iterable[str] = [" ".join(parts[:-1]), v]
    for cand in try_vals:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(cand, fmt).replace(tzinfo=timezone.utc)
                return dt
            except Exception:
                continue
    return None


def _tz_of(value: str | Any) -> str | None:
    if not isinstance(value, str):
        return None
    tail = value.strip().split()[-1]
    if tail.upper() in {"AOE", "UTC", "PST", "PDT", "CET", "CEST"}:
        return tail.upper()
    return None
