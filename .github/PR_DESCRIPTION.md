## Summary

Completes the AI Deadlines scraper implementation with full deadline extraction and PostgreSQL database integration. This is a **P0 priority** task for M2 (Data Source Integration) that validates our complete pipeline from web scraping through database storage.

## Changes

### 🕷️ Scraper Enhancements
- **Enhanced non-Scrapy scraper** (`ai_deadlines.py`):
  - Parses JavaScript-embedded deadline data using regex
  - Extracts deadline dates from `moment.tz()` calls
  - Deduplicates conferences by key
  - Successfully extracts **187 out of 192 conferences** with deadline information

- **Updated Scrapy spider** (`spiders/ai_deadlines.py`):
  - Integrated deadline extraction into spider parse method
  - Handles both date formats: `"YYYY-MM-DD HH:MM:SS"` and `"YYYY-MM-DD HH:MM"`
  - Avoids duplicate conference entries

### 💾 Database Integration
- **Implemented DatabasePipeline** (`pipelines.py`):
  - Stores conferences in PostgreSQL
  - Creates/updates `Conference`, `Source`, and `Deadline` records
  - Handles upserts gracefully (updates existing conferences)
  - Uses transactions with automatic rollback on errors
  - Prevents duplicate deadlines via unique constraints

- **Database Session Management** (`db/base.py`):
  - Added `get_session()` function for creating database sessions
  - Added `session_scope()` context manager for transactional operations
  - Integrates with settings to get database URL

- **Schema Improvements** (`db/models.py`):
  - Fixed Conference/Source relationship bidirectional mapping
  - Added `sources` relationship to Conference model
  - Configured cascade delete-orphan for proper cleanup

### ⚙️ Configuration
- Enabled `DatabasePipeline` in Scrapy settings
- Pipeline order: Validation → Deduplication → Database

## Testing

✅ **Manual Testing Performed:**
- Deadline extraction: 187/192 conferences successfully parsed (97% success rate)
- Database integration: Created test conferences, sources, and deadlines
- End-to-end verification: Data flows from scraper to PostgreSQL

**Sample Output:**
```
NAACL 2025 (naacl25):
  Year: 2025
  Homepage: https://2025.naacl.org
  Deadline (submission): 2024-10-01T23:59:59 [UTC-12]

ICLR 2025 (iclr25):
  Year: 2025
  Homepage: https://iclr.cc/Conferences/2025/CallForPapers
  Deadline (submission): 2024-09-11T23:59:00 [UTC-12]
```

## Impact

This PR establishes the **foundation for all other scrapers** and validates our complete pipeline:

```
HTML Fetching → JavaScript Parsing → Data Extraction → PostgreSQL Storage → Dagster Orchestration
```

### Benefits:
- ✅ First working scraper with real conference data
- ✅ Validated database schema with real-world data
- ✅ Established patterns for other scrapers (ACL, WikiCFP, ELRA, etc.)
- ✅ Ready for Dagster scheduled execution

### Next Steps (Future PRs):
- Add comprehensive unit tests
- Implement change detection (track deadline updates)
- Add abstract deadline extraction (currently only submission deadlines)
- Complete remaining scrapers following this pattern

## Related Issues

Implements backlog item: "Scraper: AI Deadlines (aideadlin.es)" - P0, M2

## Checklist

- [x] Code follows project style
- [x] Database migrations tested against PostgreSQL
- [x] Manual testing completed successfully
- [x] No breaking changes to existing functionality
- [ ] Unit tests added (deferred to next PR)
- [ ] Documentation updated (deferred to next PR)

## Review Notes

**Database is required:** Make sure PostgreSQL is running via Docker Compose before testing.

**Test Commands:**
```bash
# Test scraper deadline extraction
uv run --directory packages/confradar python scripts/test_scraper_deadlines.py

# Test database integration
uv run --directory packages/confradar python scripts/test_database_integration.py

# Run full scraper (stores in database)
cd packages/confradar
uv run scrapy crawl ai_deadlines
```

---

**Ready for review!** Please let me know if you'd like any changes before merging.
