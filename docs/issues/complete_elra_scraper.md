Title: Complete ELRA Scraper

GitHub Issue: https://github.com/orgroman/confradar/issues/79

Summary
Finalize the ELRA scraper to extract conferences/workshops and deadlines from https://www.elra.info/elra-events/, persisting via DatabasePipeline with tests and documentation.

Background
`ELRASpider` exists and emits basic conference metadata with empty deadlines. ELRA event pages vary in structure; deadlines may be embedded in article content or linked pages.

Scope
- Enhance `packages/confradar/src/confradar/scrapers/spiders/elra.py`:
  - Extract name, year, official homepage
  - Parse deadlines from content or follow links to official sites
  - Normalize dates/timezones via shared utilities (AoE/local tz)
- Ensure persistence via `DatabasePipeline` with deduplication
- Add parser unit tests and DB integration tests
- Document parsing strategies and caveats

Out of Scope
- Alerts delivery or UI visualization (future)

Acceptance Criteria
- Spider yields ConferenceItem(s) with populated, normalized deadlines where available
- Tests cover happy path and one edge case
- Docs updated if special parsing logic is used

References
- Spider: `packages/confradar/src/confradar/scrapers/spiders/elra.py`
- Pipeline: `packages/confradar/src/confradar/scrapers/pipelines.py`
- Models: `packages/confradar/src/confradar/db/models.py`
- Precedent: `docs/issues/complete_ai_deadlines_scraper.md`
- Epic: `docs/issues/epic_m2_scrapers_and_deadlines.md`
