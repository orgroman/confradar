## Epic
Backend Infrastructure & Data Pipeline

## Description
Expand the test suite to achieve >80% code coverage across the codebase, ensuring reliability and maintainability.

## Current State
- Basic unit tests exist for scrapers and database models
- Coverage is below target threshold
- Integration tests are minimal
- No end-to-end pipeline tests

## Tasks

### Unit Tests
- [ ] Test all scraper spiders with mocked HTTP responses
- [ ] Test database models (Conference, Source) CRUD operations
- [ ] Test Pydantic schemas and validation logic
- [ ] Test utility functions (date parsing, URL normalization)
- [ ] Test LLM extraction functions (with mocked API calls)

### Integration Tests
- [ ] Test Scrapy pipeline end-to-end with test fixtures
- [ ] Test database transactions and rollback behavior
- [ ] Test Dagster asset dependencies and execution order
- [ ] Test Alembic migrations up and down

### End-to-End Tests
- [ ] Test complete crawl job from scrape to database storage
- [ ] Test concurrent Dagster asset materialization
- [ ] Test change detection with before/after snapshots

### Test Infrastructure
- [ ] Configure pytest with coverage reporting
- [ ] Add pytest fixtures for database sessions and test data
- [ ] Set up test database isolation (separate test DB or in-memory)
- [ ] Add CI job to run tests and fail on coverage drop
- [ ] Generate HTML coverage reports for review

## Acceptance Criteria
- [ ] Overall code coverage >80%
- [ ] All critical paths (scrapers, database, Dagster) have tests
- [ ] Tests run in <60 seconds
- [ ] CI enforces coverage threshold
- [ ] Coverage report generated and accessible

## Configuration
```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "--cov=confradar --cov-report=html --cov-report=term --cov-fail-under=80"
```

## Priority
P1 - Critical for code quality and refactoring confidence

## Estimated Effort
3-5 days

## Notes
- Focus on critical paths first (scrapers, database, extraction)
- Mock external dependencies (HTTP requests, LLM APIs)
- Use pytest fixtures for reusable test data
- Consider property-based testing (Hypothesis) for parsers
