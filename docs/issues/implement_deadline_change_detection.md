Title: Implement Deadline Change Detection

Summary
Detect and record changes to conference deadlines between crawls to avoid duplicates and enable downstream notifications/analytics.

Motivation
Deadlines change frequently (extensions, corrections). We need to track when a deadline changes and update records accordingly while maintaining history or at least an audit trail.

Scope
- Define change semantics for Deadline rows in the DB:
  - If same (conference_id, kind) and due_date changes → update existing record and log a change event; or insert new version and mark the prior as superseded
  - If identical already exists → no-op
- Implement logic in `DatabasePipeline` (or a dedicated service) to:
  - Check for existing deadlines for (conference, kind)
  - Detect changes (date/time/timezone) and apply chosen strategy
  - Option A (simpler): update the existing row and add a `updated_at` timestamp + optional `prev_due_date` field
  - Option B (audit-friendly): introduce a `deadline_versions` table with FK to `deadline`
- Add minimal tests verifying detection of a changed due_date and correct persistence behavior
- Document the chosen approach and how it interacts with unique constraints

Out of Scope
- User-facing notifications (email/Slack)
- UI visualization

Acceptance Criteria
- On re-crawl with a changed due_date for the same conference/kind, the system reflects the change once (no duplicates) and preserves an audit signal (timestamp or version row)
- Tests demonstrate change detection and idempotency
- Docs updated accordingly

References
- Pipeline: `packages/confradar/src/confradar/scrapers/pipelines.py`
- Models: `packages/confradar/src/confradar/db/models.py`
- Epic: `docs/issues/epic_m2_scrapers_and_deadlines.md`
