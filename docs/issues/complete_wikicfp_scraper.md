Title: Complete WikiCFP Scraper

Summary
Finalize the WikiCFP scraper to extract conferences and deadlines from http://www.wikicfp.com/cfp/, persisting via DatabasePipeline with tests and docs.

Background
`WikiCFPSpider` exists and currently emits metadata with empty deadlines. WikiCFP lists often include deadline columns and links to official CFP pages which may have more accurate dates.

Scope
- Enhance `packages/confradar/src/confradar/scrapers/spiders/wikicfp.py`:
  - Extract name, year, and official homepage (prefer non-wikicfp external links)
  - Parse deadline(s) from the listing row and/or detail pages
  - Handle pagination and optional category filtering
  - Normalize dates/timezones via shared utilities
- Ensure DB persistence and deduplication via `DatabasePipeline`
- Add parser unit tests and DB integration tests
- Document parsing rules and limitations

Out of Scope
- Alerts delivery or UI (future)

Acceptance Criteria
- Spider yields deadlines where present; normalized and timezone-aware
- Tests cover happy path + edge case
- Docs updated as needed

References
- Spider: `packages/confradar/src/confradar/scrapers/spiders/wikicfp.py`
- Pipeline: `packages/confradar/src/confradar/scrapers/pipelines.py`
- Models: `packages/confradar/src/confradar/db/models.py`
- Precedent: `docs/issues/complete_ai_deadlines_scraper.md`
- Epic: `docs/issues/epic_m2_scrapers_and_deadlines.md`
