# Complete AI Deadlines Scraper Implementation

**Issue Type:** Feature  
**Area:** retrieval  
**Priority:** P0  
**Milestone:** M2 - Data Source Integration & Web Crawling

## Summary

Complete the AI Deadlines scraper (aideadlines.org) to extract full conference information including deadlines, integrate with PostgreSQL database, and schedule via Dagster. This is the foundational scraper that will validate our complete pipeline (scraping → extraction → storage → orchestration).

## Current State

We have a basic spider skeleton at `packages/confradar/src/confradar/scrapers/spiders/ai_deadlines.py` that:
- ✅ Extracts conference names and keys
- ✅ Attempts to extract years from keys
- ✅ Tries to find homepage links
- ❌ Does NOT extract deadline information (TODOs in code)
- ❌ Not integrated with database storage
- ❌ Not scheduled via Dagster

## Acceptance Criteria

### 1. Enhanced Spider (ai_deadlines.py)
- [ ] Extract submission deadline (date + timezone)
- [ ] Extract abstract deadline if available
- [ ] Extract notification deadline if available
- [ ] Extract conference dates (start/end)
- [ ] Extract location information
- [ ] Handle pagination/filtering (NLP, CV, ML categories)
- [ ] Robust error handling for missing fields
- [ ] Structured logging for debugging

### 2. Database Integration (pipelines.py)
- [ ] Update `DatabasePipeline` to store conferences in PostgreSQL
- [ ] Create `Conference` records with unique keys
- [ ] Create `Source` records linking to aideadlines URL
- [ ] Create `Deadline` records for each deadline type
- [ ] Handle upserts (update existing conferences if changed)
- [ ] Use SQLAlchemy session management from `confradar.db.base`

### 3. Dagster Orchestration (dagster/assets/scrapers.py)
- [ ] Create `ai_deadlines_scraper` asset
- [ ] Schedule daily execution (configurable via settings)
- [ ] Track run statistics (conferences scraped, errors)
- [ ] Log output to Dagster event stream
- [ ] Handle failures gracefully (alert but don't block)

### 4. Testing (tests/)
- [ ] Unit tests for spider parsing logic
- [ ] Integration test: scrape → database (using test DB)
- [ ] Test deadline extraction accuracy (known conferences)
- [ ] Test database upsert logic (run twice, verify no duplicates)
- [ ] Mock HTTP responses for reliable testing

### 5. Documentation
- [ ] Update `docs/wiki/Scraper-Development.md` with AI Deadlines example
- [ ] Document data flow: aideadlines.org → Scrapy → Database → Dagster
- [ ] Add troubleshooting section (common HTML structure changes)
- [ ] Update `README.md` with usage examples

## Technical Design

### Spider Enhancement

The AI Deadlines site has a structured layout we can parse:

```python
# Pseudo-structure from aideadlines.org
<div class="conf-row">
    <a href="/conference?id=icml25">ICML 2025</a>
    <span class="deadline">Abstract: 2025-01-15 (AoE)</span>
    <span class="deadline">Submission: 2025-01-22 (AoE)</span>
    <span class="conf-dates">Jul 11-17, 2025</span>
    <span class="location">Vienna, Austria</span>
</div>
```

Strategy:
1. Parse conference rows using CSS selectors
2. Extract all deadline spans and classify by keywords (abstract, submission, notification)
3. Parse dates using `confradar.parsers.dates` utilities
4. Store timezone information (most are AoE for AI conferences)

### Database Pipeline

```python
class DatabasePipeline:
    def process_item(self, item: ConferenceItem, spider):
        with get_session() as session:
            # Upsert conference
            conference = session.query(Conference).filter_by(key=item.key).first()
            if not conference:
                conference = Conference(key=item.key, name=item.name, ...)
                session.add(conference)
            
            # Update source
            source = Source(conference_id=conference.id, url=item.url, ...)
            session.merge(source)
            
            # Update deadlines
            for deadline_data in item.deadlines:
                deadline = Deadline(conference_id=conference.id, ...)
                session.merge(deadline)
            
            session.commit()
```

### Dagster Asset

```python
@asset(group_name="scrapers")
def ai_deadlines_scraper(context: AssetExecutionContext) -> dict:
    """Run AI Deadlines scraper and store results in database."""
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess(get_project_settings())
    process.crawl('ai_deadlines')
    process.start()  # Blocks until complete
    
    # Return stats for monitoring
    return {
        "conferences_scraped": ...,
        "deadlines_extracted": ...,
        "errors": ...,
    }
```

## Implementation Plan

1. **Phase 1: Spider Enhancement** (Priority 1)
   - Analyze current HTML structure of aideadlines.org
   - Update CSS selectors to extract all deadline information
   - Add date parsing using existing `parsers.dates` module
   - Test manually: `uv run scrapy crawl ai_deadlines -o test.json`

2. **Phase 2: Database Integration** (Priority 2)
   - Update `DatabasePipeline` to use PostgreSQL
   - Test with Docker Compose postgres service
   - Verify data in pgAdmin

3. **Phase 3: Dagster Integration** (Priority 3)
   - Create scraper asset
   - Test via Dagster UI (http://localhost:3000)
   - Verify asset materializes successfully

4. **Phase 4: Testing & Documentation** (Priority 4)
   - Write comprehensive tests
   - Update documentation
   - Create usage examples

## Success Metrics

- ✅ Scraper extracts 50+ NLP conferences from aideadlines.org
- ✅ Deadline extraction accuracy >90% (compared to manual verification)
- ✅ Zero database errors during normal operation
- ✅ Dagster asset runs successfully on schedule
- ✅ All tests pass with >80% coverage
- ✅ Documentation complete with examples

## Dependencies

- ✅ PostgreSQL database running (Issue #75)
- ✅ SQLAlchemy models defined (conferences, sources, deadlines)
- ✅ Dagster orchestration configured
- ⚠️ Date parsing utilities may need enhancement for timezone handling

## Risk Mitigation

**Risk:** HTML structure changes on aideadlines.org  
**Mitigation:** Add fallback selectors, log warnings when structure changes, include structure validation in tests

**Risk:** Rate limiting from website  
**Mitigation:** Respect robots.txt, implement polite delays (2s between requests), add user-agent

**Risk:** Database connection failures  
**Mitigation:** Implement retry logic with exponential backoff, graceful degradation

## Notes

- This scraper is P0 because it's the most reliable source for NLP/ML conference deadlines
- Success here establishes patterns for other scrapers (ACL, WikiCFP, etc.)
- Consider adding a "last_scraped" timestamp to track freshness
- May want to add change detection (compare old vs new deadlines) in future iteration

## References

- Source website: https://aideadlines.org/?sub=NLP
- Existing spider: `packages/confradar/src/confradar/scrapers/spiders/ai_deadlines.py`
- Database models: `packages/confradar/src/confradar/db/models.py`
- Backlog item: "Scraper: AI Deadlines (aideadlin.es)" from `backlog_complete_prd.csv`
