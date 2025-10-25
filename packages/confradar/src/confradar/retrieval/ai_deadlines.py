from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, List

import httpx


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


def fetch_ai_deadlines(api_url: str = DEFAULT_API, *, timeout: float = 20.0) -> list[ConferenceItem]:
    """Fetch and normalize AI Deadlines data.

    This expects an Open API returning JSON list of conferences. Tests mock httpx to avoid
    real network calls. The schema is normalized to ConferenceItem/DeadlineItem.
    """
    with httpx.Client(timeout=timeout) as client:
        resp = client.get(api_url)
        resp.raise_for_status()
        data = resp.json()

    return [normalize_record(rec) for rec in data]


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
