@echo off
REM Update all GitHub issues with dependency relations
echo Updating issue relations...

gh issue edit 7 --body "Persist events with versioning metadata and last_updated timestamp.## Dependencies- **Depends on**: #3 (schema definition)- **Blocks**: #8, #20, #22, #36, #12, #13, #15, #29, #37## Priority- Core storage layer for all features"

gh issue edit 22 --body "Implement Alembic migrations for database schema changes.## Dependencies- **Depends on**: #3 (schema), #7 (KB storage)- **Blocks**: Production deployments"

gh issue edit 2 --body "Add search-based discovery fallback for conferences not in seed list.## Dependencies- **Depends on**: #1 (validate seeded approach first)- **Enhances**: Discovery coverage"

gh issue edit 4 --body "Build rule-based parser for structured date extraction from conference pages.## Dependencies- **Depends on**: #1 (needs data to parse)- **Blocks**: #5, #6, #8, #20## Priority- Core extraction logic"

gh issue edit 5 --body "Add LLM-powered extraction for complex cases.## Dependencies- **Depends on**: #4 (rule-first must exist), #53 (LLM API setup)- **Enhances**: #4 for edge cases"

gh issue edit 6 --body "Handle timezone conversions and AoE deadline calculations.## Dependencies- **Depends on**: #4 (part of date extraction)## Priority- Critical for deadline accuracy"

gh issue edit 8 --body "Detect and track changes in conference dates.## Dependencies- **Depends on**: #7 (KB for history), #4 (extraction)- **Blocks**: #19, #31, #12## Priority- Enables monitoring and serving features"

gh issue edit 20 --body "Implement validation rules for extracted data quality.## Dependencies- **Depends on**: #7 (KB), #4 (extraction)- **Blocks**: Production readiness"

gh issue edit 9 --body "Define normalization rules for conference name aliases and acronyms.## Dependencies- **Depends on**: #7 (needs KB)- **Blocks**: #10, #11, #36- **Works with**: #38"

gh issue edit 10 --body "Use embeddings to cluster similar conference names.## Dependencies- **Depends on**: #9 (normalization rules first)- **Blocks**: #11, #36, #38"

gh issue edit 11 --body "Link workshops to their parent conference events automatically.## Dependencies- **Depends on**: #10 (clustering capability)- **Enhances**: Data organization"

gh issue edit 36 --body "Advanced deduplication strategies.## Dependencies- **Depends on**: #9, #10, #11 (clustering)- **Enhances**: Data quality"

gh issue edit 38 --body "Reconcile conference data from multiple sources.## Dependencies- **Depends on**: #1, #2 (retrieval), #9, #10 (clustering)- **Integrates**: Multiple data sources"

gh issue edit 19 --body "Add monitoring and alerting for pipeline health.## Dependencies- **Depends on**: #18 (Dagster), #8 (change detection), #24 (logging)- **Blocks**: Production operations## Priority- Required for production reliability"

gh issue edit 21 --body "Implement retry logic and error handling.## Dependencies- **Depends on**: #18 (Dagster orchestration)- **Blocks**: Reliable operations"

gh issue edit 12 --body "Build adapter to sync conference data to Notion database.## Dependencies- **Depends on**: #7 (KB), #8 (change detection)- **Blocks**: #31 (notifications)## Priority- Primary user-facing interface for MVP"

gh issue edit 13 --body "Build adapter to sync conference data to Google Docs.## Dependencies- **Depends on**: #7 (KB), #8 (change detection)- **Alternative to**: #12"

gh issue edit 15 --body "Generate iCalendar files for conference deadlines.## Dependencies- **Depends on**: #7 (KB)"

gh issue edit 29 --body "Build REST API for querying conference data.## Dependencies- **Depends on**: #7 (KB)- **Blocks**: #30- **Alternative to**: #12"

gh issue edit 30 --body "Add authentication and rate limiting to REST API.## Dependencies- **Depends on**: #29 (API must exist first)## Priority- Security for public API"

gh issue edit 31 --body "Send email/Slack notifications when deadlines change.## Dependencies- **Depends on**: #8 (change detection), #12 or #29 (data access)- **Enhances**: User experience"

gh issue edit 32 --body "Build comprehensive unit test suite.## Dependencies- **Depends on**: None (can start immediately)- **Blocks**: #33, #14, #34## Priority- Foundation for quality assurance"

gh issue edit 33 --body "Build integration tests for end-to-end pipeline.## Dependencies- **Depends on**: #32 (unit tests first), #18 (orchestration)- **Blocks**: Production deployment"

gh issue edit 14 --body "Build evaluation harness to measure extraction accuracy.## Dependencies- **Depends on**: #32, #33 (test infrastructure)- **Validates**: #4, #5"

gh issue edit 34 --body "Conduct performance and load testing.## Dependencies- **Depends on**: #32, #33## Priority- Pre-production validation"

gh issue edit 41 --body "Set up Python code formatting with Black/Ruff.## Dependencies- **Depends on**: None (can start immediately)- **Blocks**: #42, #43, #16## Priority- Foundation for code quality"

gh issue edit 42 --body "Add mypy type checking.## Dependencies- **Depends on**: #41- **Works with**: #43"

gh issue edit 43 --body "Set up pre-commit hooks.## Dependencies- **Depends on**: #41, #42- **Enforces**: Code quality standards"

gh issue edit 23 --body "Implement secrets management for API keys and credentials.## Dependencies- **Depends on**: None (can start immediately)- **Blocks**: #27, #28## Priority- Required for secure production deployment"

gh issue edit 24 --body "Set up structured logging infrastructure.## Dependencies- **Depends on**: None (can start immediately)- **Blocks**: #19, #25, #26## Priority- Foundation for observability"

gh issue edit 25 --body "Add metrics collection and observability tooling.## Dependencies- **Depends on**: #24- **Works with**: #19"

gh issue edit 26 --body "Integrate Sentry for error tracking.## Dependencies- **Depends on**: #24- **Enhances**: Production error visibility"

gh issue edit 27 --body "Complete containerization with Docker.## Dependencies- **Depends on**: #23- **Blocks**: #28## Priority- Partially complete (Dagster done)"

gh issue edit 28 --body "Set up automated cloud deployment pipeline.## Dependencies- **Depends on**: #23, #27- **Blocks**: Production launch"

gh issue edit 40 --body "Refine Python environment management with uv.## Status- Using uv from #39"

gh issue edit 16 --body "Document development workflow and CI/CD basics.## Dependencies- **Depends on**: #41, #43## Priority- Developer onboarding"

gh issue edit 17 --body "Maintain comprehensive setup and architecture documentation.## Status- Wiki exists and is maintained"

gh issue edit 37 --body "Add conference ranking/tier data.## Dependencies- **Depends on**: #7 (KB)## Priority- P3 enhancement"

gh issue edit 35 --body "Build manual review UI for quality control.## Dependencies- **Depends on**: #7 (KB), #20## Priority- P3 quality control tool"

echo Done! All issues updated.
