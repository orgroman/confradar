from __future__ import annotations

import re
from datetime import datetime

import dateparser

MONTHS = (
    "jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|"
    "sep|sept|september|oct|october|nov|november|dec|december"
)

# Simple regex capturing common date expressions (e.g., Nov 15, 2025; 2025-11-15; 15 Nov 2025)
_DATE_PATTERN = (
    f"\\b((?:{MONTHS})\\.?\\s+\\d{{1,2}}(?:,\\s*\\d{{4}})?|"
    f"\\d{{1,2}}\\s+(?:{MONTHS})\\s+\\d{{4}}|"
    "\\d{4}-\\d{1,2}-\\d{1,2})\\b"
)
DATE_REGEX = re.compile(_DATE_PATTERN, re.IGNORECASE)


def extract_dates_from_text(text: str) -> list[datetime]:
    """Extract date-like values from text and parse to datetimes.

    Heuristic, non-exhaustive. Intended as a smoke test until the full extraction pipeline (rules+LLM) lands.
    """
    candidates: set[str] = set(m.group(0) for m in DATE_REGEX.finditer(text))
    results: list[datetime] = []
    for token in sorted(candidates):
        dt = dateparser.parse(
            token,
            settings={
                "PREFER_DAY_OF_MONTH": "first",
                "PREFER_DATES_FROM": "future",
                "RELATIVE_BASE": datetime.utcnow(),
            },
        )
        if isinstance(dt, datetime):
            results.append(dt)
    # De-duplicate by date (Y-m-d) while preserving order
    seen: set[str] = set()
    unique: list[datetime] = []
    for dt in sorted(results):
        key = dt.date().isoformat()
        if key not in seen:
            seen.add(key)
            unique.append(dt)
    return unique
