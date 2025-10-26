Title: Complete ACL Web Scraper (ACL Sponsored Events)

GitHub Issue: https://github.com/orgroman/confradar/issues/77

Summary
Finalize the ACL Web scraper to extract conferences and key deadlines from https://www.aclweb.org/portal/acl_sponsored_events, following the AI Deadlines pattern. Persist results via DatabasePipeline and cover with tests.

Background
The spider `ACLWebSpider` exists but currently only emits basic conference metadata with empty deadlines. We need to parse dates/deadlines from the page and linked detail pages as needed, normalize, and store.

Scope
- Enhance `packages/confradar/src/confradar/scrapers/spiders/acl_web.py`:
  - Extract conference name, year, homepage (preferring external official sites)
  - Parse available deadlines: abstract due, submission due, notification, camera-ready, etc.
  - Follow event detail pages when required to fetch deadlines
  - Normalize dates (timezone, AoE handling) using shared utilities (see related issue)
- Ensure `DatabasePipeline` persists conferences/sources/deadlines without duplicates
- Add unit tests for parsing and integration tests for DB writes
- Update docs with notes about ACL-specific parsing quirks

Out of Scope
- Full historical backfill beyond what’s reachable via pagination
- Alerting/notifications (covered by change detection epic child)

Acceptance Criteria
- Spider yields ConferenceItem with populated deadlines where available
- Deadlines are normalized to UTC-aware datetimes and include timezone label when applicable
- Tests: ≥1 parser unit test (happy path + 1 edge), ≥1 integration test verifying DB persistence
- Docs updated in `docs/wiki/Scraper-Development.md` if non-obvious logic is used

References
- Spider: `packages/confradar/src/confradar/scrapers/spiders/acl_web.py`
- Pipeline: `packages/confradar/src/confradar/scrapers/pipelines.py`
- Models: `packages/confradar/src/confradar/db/models.py`
- Precedent: AI Deadlines issue – `docs/issues/complete_ai_deadlines_scraper.md`
- Epic: `docs/issues/epic_m2_scrapers_and_deadlines.md`

Notes
- ACL pages may list dates in free text; consider regex and detail-page fetches
- Be polite: respect robots and add small delays; cache in dev if needed
