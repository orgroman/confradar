Title: Epic – Complete M2 Scrapers and Deadline Handling

GitHub Epic: https://github.com/orgroman/confradar/issues/81

Summary
Track and coordinate the completion of remaining M2 scrapers and shared deadline handling improvements. This epic groups the work to bring ACL Web, ChairingTool, ELRA, and WikiCFP scrapers to parity with AI Deadlines (including deadline extraction and DB persistence), plus core improvements like shared extraction utilities and change detection.

Motivation
We now have a solid pattern from AI Deadlines: robust extraction (including JS-parsed dates), DB pipeline integration, and tests/docs. Applying this pattern to the remaining sources will quickly expand coverage. Centralizing date parsing and adding change detection will improve quality and maintainability.

Scope
- Complete and productionize the following scrapers:
  - ACL Web (aclweb.org) – `confradar.scrapers.spiders.acl_web.ACLWebSpider`
  - ChairingTool (chairingtool.com) – `confradar.scrapers.spiders.chairing_tool.ChairingToolSpider`
  - ELRA (elra.info) – `confradar.scrapers.spiders.elra.ELRASpider`
  - WikiCFP (wikicfp.com) – `confradar.scrapers.spiders.wikicfp.WikiCFPSpider`
- Extract and persist key deadlines (CFP, abstract, submission, notification, camera-ready, etc.)
- Build shared deadline extraction utilities for reuse (regex/JS parsing, normalization, AoE/timezone handling)
- Add change detection for deadlines to detect updates and avoid duplicate rows
- Tests and docs matching the AI Deadlines precedent

Out of Scope
- UI/visualization of changes (future)
- Notifications/alerts delivery channels (email/Slack) beyond basic detection (future)

Acceptance Criteria
- Each target scraper yields ConferenceItem(s) with populated deadlines when available
- DatabasePipeline persists conferences, sources, and deadlines without duplicates
- Unit tests (parser) and integration tests (DB pipeline) for each scraper; all tests green
- Shared utilities extracted (date parsing, normalization, AoE/timezone) with coverage
- Change detection implemented with clear behavior (update vs. insert, dedup, audit trail)
- Updated docs: Getting-Started, Scraper-Development, and source-specific notes

Related Work
- AI Deadlines (completed): `docs/issues/complete_ai_deadlines_scraper.md`

Child Issues
- [ ] orgroman/confradar#77 – ACL Web scraper (spec: docs/issues/complete_acl_web_scraper.md)
- [ ] orgroman/confradar#78 – ChairingTool scraper (spec: docs/issues/complete_chairing_tool_scraper.md)
- [ ] orgroman/confradar#79 – ELRA scraper (spec: docs/issues/complete_elra_scraper.md)
- [ ] orgroman/confradar#80 – WikiCFP scraper (spec: docs/issues/complete_wikicfp_scraper.md)
- [ ] orgroman/confradar#6 – Timezone/AoE handling (context: docs/issues/abstract_deadline_extraction_framework.md)
- [ ] orgroman/confradar#4 – Extraction: rule-first parser (context: docs/issues/abstract_deadline_extraction_framework.md)
- [ ] orgroman/confradar#8 – Change detection for dates (context: docs/issues/implement_deadline_change_detection.md)

References
- Code paths
  - Scrapy spiders: `packages/confradar/src/confradar/scrapers/spiders/`
  - DB models: `packages/confradar/src/confradar/db/models.py`
  - Pipeline: `packages/confradar/src/confradar/scrapers/pipelines.py`
  - Dagster assets: `packages/confradar/src/confradar/dagster/assets/`
