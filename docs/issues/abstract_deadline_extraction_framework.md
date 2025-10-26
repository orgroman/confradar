Title: Shared Deadline Extraction and Normalization Framework

Summary
Create reusable utilities for extracting, parsing, and normalizing deadlines across scrapers, consolidating logic discovered in AI Deadlines (JS/moment.tz patterns) and extending for other sources.

Motivation
Several sources embed dates in varying formats (inline JS, free text, tables). Centralizing parsing and normalization reduces duplication, improves correctness (timezone/AoE), and simplifies tests.

Scope
- Introduce a module under `packages/confradar/src/confradar/parsers/dates.py` (extend existing) or `parsers/deadlines.py` with:
  - Regex helpers for common patterns (YYYY-MM-DD HH:MM[:SS], month/day formats)
  - JS extraction helpers (e.g., moment.tz(...) patterns with per-conference timezone vars)
  - Normalization to timezone-aware datetimes (pytz/zoneinfo), consistent output schema
  - Mapping of label aliases to standardized kinds (submission, abstract, notification, camera-ready)
- Provide simple APIs for spiders to call; keep IO-free (pure functions) for easy testing
- Add unit tests covering core parsing paths and a couple of edge cases (missing tz, AoE)
- Document usage in `docs/wiki/Scraper-Development.md`

Out of Scope
- Site-specific scraping or deep heuristics beyond utility-level helpers

Acceptance Criteria
- New parser utilities with docstrings and tests
- At least one target scraper (e.g., ACL) updated to use the utilities
- Consistent deadline kind taxonomy and datetime normalization

References
- Current date helpers: `packages/confradar/src/confradar/parsers/dates.py`
- AI Deadlines code (regex + JS parsing) for reference
- Epic: `docs/issues/epic_m2_scrapers_and_deadlines.md`
