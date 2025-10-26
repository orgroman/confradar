Title: Complete ChairingTool Scraper

GitHub Issue: https://github.com/orgroman/confradar/issues/78

Summary
Finalize the ChairingTool scraper to extract conferences and deadlines from https://chairingtool.com/conferences, following the AI Deadlines pattern and persisting to the database.

Background
`ChairingToolSpider` exists and yields basic conference metadata with empty deadlines. Deadlines may require following links to each conference page and parsing structured fields or free text.

Scope
- Enhance `packages/confradar/src/confradar/scrapers/spiders/chairing_tool.py`:
  - Extract name, year, official homepage (external if available)
  - Parse key deadlines (abstract, submission, notification, camera-ready)
  - Follow detail pages when needed; handle pagination
  - Normalize dates/timezones (AoE, local tz) via shared utilities
- Ensure DB persistence via `DatabasePipeline` without duplicates
- Add parser unit tests and DB integration tests
- Document any site-specific parsing rules

Out of Scope
- Alerts delivery; UI (future)

Acceptance Criteria
- Spider yields deadlines where present; normalized and timezone-aware
- Tests cover happy path and one edge case (e.g., missing timezone)
- Docs updated as needed

References
- Spider: `packages/confradar/src/confradar/scrapers/spiders/chairing_tool.py`
- Pipeline: `packages/confradar/src/confradar/scrapers/pipelines.py`
- Models: `packages/confradar/src/confradar/db/models.py`
- Precedent: `docs/issues/complete_ai_deadlines_scraper.md`
- Epic: `docs/issues/epic_m2_scrapers_and_deadlines.md`

Notes
- Respect robots and rate limits; consider caching during development
