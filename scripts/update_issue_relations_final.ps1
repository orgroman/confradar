# Update GitHub Issues with Dependency Relations in Issue Body
# This script edits the issue body to add Dependencies sections

Write-Host "🔗 Updating Issue Relations (editing issue bodies)..." -ForegroundColor Cyan

# Foundation Layer
Write-Host "`n📊 Foundation Layer..." -ForegroundColor Yellow

$body = @"
Persist events with versioning metadata and last_updated timestamp.

## Dependencies
- **Depends on**: #3 (schema definition)
- **Blocks**: #8, #20, #22, #36, #12, #13, #15, #29, #37

## Priority
🔴 **CRITICAL PATH** - Core storage layer for all features
"@
gh issue edit 7 --body $body

$body = @"
Implement Alembic migrations for database schema changes.

## Dependencies
- **Depends on**: #3 (schema), #7 (KB storage)
- **Blocks**: Production deployments

## Priority
Required for production-ready database management
"@
gh issue edit 22 --body $body

# Retrieval Layer
Write-Host "`n🔍 Retrieval Layer..." -ForegroundColor Yellow

$body = @"
Implement retrieval starting with curated seeds (ACL, NeurIPS, ICML, ICLR, AAAI, EMNLP, CVPR, KDD). Schedule daily checks.

## Dependencies
- **Depends on**: None (can start immediately)
- **Blocks**: #2, #4, #38

## Priority
✅ First data source to implement - enables extraction work
"@
gh issue edit 1 --body $body

$body = @"
Add search-based discovery fallback for conferences not in seed list.

## Dependencies
- **Depends on**: #1 (validate seeded approach first)
- **Enhances**: Discovery coverage beyond known conferences

## Priority
Extends retrieval capabilities after seed crawling is proven
"@
gh issue edit 2 --body $body

# Extraction Layer
Write-Host "`n🔬 Extraction Layer..." -ForegroundColor Yellow

$body = @"
Build rule-based parser for structured date extraction from conference pages.

## Dependencies
- **Depends on**: #1 (needs data to parse)
- **Blocks**: #5, #6, #8, #20

## Priority
🔴 **CRITICAL PATH** - Core extraction logic for the pipeline
"@
gh issue edit 4 --body $body

$body = @"
Add LLM-powered extraction for complex/unstructured cases that rules cannot handle.

## Dependencies
- **Depends on**: #4 (rule-first must exist), #53 ✅ (LLM API setup)
- **Enhances**: #4 for edge cases

## Priority
Handles complex extraction scenarios after rule-based is working
"@
gh issue edit 5 --body $body

$body = @"
Handle timezone conversions and AoE (Anywhere on Earth) deadline calculations.

## Dependencies
- **Depends on**: #4 (part of date extraction pipeline)

## Priority
⚠️ Critical for deadline accuracy - prevents user confusion
"@
gh issue edit 6 --body $body

# Intelligence Layer
Write-Host "`n🧠 Intelligence Layer..." -ForegroundColor Yellow

$body = @"
Detect and track changes in conference dates by comparing new scrapes to stored data.

## Dependencies
- **Depends on**: #7 (KB for storing history), #4 (extraction working)
- **Blocks**: #19 (monitoring), #31 (notifications), #12 (Notion updates)

## Priority
🔴 **CRITICAL PATH** - Enables monitoring and serving features
"@
gh issue edit 8 --body $body

$body = @"
Implement validation rules for extracted data quality (date sanity, required fields, etc).

## Dependencies
- **Depends on**: #7 (KB), #4 (extraction)
- **Blocks**: Production readiness

## Priority
Required for reliable production data
"@
gh issue edit 20 --body $body

$body = @"
Define normalization rules for conference name aliases and acronyms.

## Dependencies
- **Depends on**: #7 (needs KB)
- **Blocks**: #10, #11, #36
- **Works with**: #38 (multi-source reconciliation)

## Priority
Foundation for deduplication and clustering
"@
gh issue edit 9 --body $body

$body = @"
Use embeddings to cluster similar conference names and detect aliases.

## Dependencies
- **Depends on**: #9 (normalization rules first)
- **Blocks**: #11, #36, #38

## Priority
Advanced alias detection beyond rules
"@
gh issue edit 10 --body $body

$body = @"
Link workshops to their parent conference events automatically.

## Dependencies
- **Depends on**: #10 (clustering capability)
- **Enhances**: Data organization and deduplication

## Priority
Improves data structure and user experience
"@
gh issue edit 11 --body $body

$body = @"
Advanced deduplication strategies beyond basic clustering.

## Dependencies
- **Depends on**: #9, #10, #11 (clustering infrastructure)
- **Enhances**: Data quality

## Priority
Polish after basic clustering is working
"@
gh issue edit 36 --body $body

$body = @"
Reconcile conference data from multiple sources (WikiCFP, official sites, etc).

## Dependencies
- **Depends on**: #1, #2 (retrieval), #9, #10 (clustering)
- **Integrates**: Multiple data sources

## Priority
Enhances coverage and accuracy
"@
gh issue edit 38 --body $body

# Orchestration
Write-Host "`n⚙️ Orchestration Layer..." -ForegroundColor Yellow

$body = @"
Add monitoring and alerting for pipeline health and data freshness.

## Dependencies
- **Depends on**: #18 ✅ (Dagster orchestration), #8 (change detection), #24 (logging)
- **Blocks**: Production operations

## Priority
🔴 **CRITICAL PATH** - Required for production reliability
"@
gh issue edit 19 --body $body

$body = @"
Implement retry logic and comprehensive error handling for scrapers and extraction.

## Dependencies
- **Depends on**: #18 ✅ (Dagster orchestration)
- **Blocks**: Reliable production operations

## Priority
Required for resilient pipeline execution
"@
gh issue edit 21 --body $body

# Serving Layer
Write-Host "`n📤 Serving Layer..." -ForegroundColor Yellow

$body = @"
Build adapter to sync conference data to Notion database.

## Dependencies
- **Depends on**: #7 (KB to query), #8 (change detection for updates)
- **Blocks**: #31 (notifications)

## Priority
🎯 Primary user-facing interface for MVP
"@
gh issue edit 12 --body $body

$body = @"
Build adapter to sync conference data to Google Docs.

## Dependencies
- **Depends on**: #7 (KB), #8 (change detection)
- **Alternative to**: #12 (Notion adapter)

## Priority
Alternative serving option to Notion
"@
gh issue edit 13 --body $body

$body = @"
Generate iCalendar (.ics) files for conference deadlines and dates.

## Dependencies
- **Depends on**: #7 (KB)

## Priority
Nice-to-have export format for calendar apps
"@
gh issue edit 15 --body $body

$body = @"
Build REST API for querying conference data.

## Dependencies
- **Depends on**: #7 (KB)
- **Blocks**: #30 (API auth)
- **Alternative to**: #12 (Notion adapter)

## Priority
Programmatic access to data
"@
gh issue edit 29 --body $body

$body = @"
Add authentication and rate limiting to REST API.

## Dependencies
- **Depends on**: #29 (API must exist first)
- **Required for**: Production API deployment

## Priority
Security for public API
"@
gh issue edit 30 --body $body

$body = @"
Send email/Slack notifications when conference deadlines change.

## Dependencies
- **Depends on**: #8 (change detection), #12 or #29 (data access)
- **Enhances**: User experience with proactive alerts

## Priority
Valuable user feature after core serving is working
"@
gh issue edit 31 --body $body

# Testing
Write-Host "`n🧪 Testing..." -ForegroundColor Yellow

$body = @"
Build comprehensive unit test suite for all core modules.

## Dependencies
- **Depends on**: None (can start immediately)
- **Blocks**: #33, #14, #34

## Priority
🔴 Foundation for quality assurance - start early
"@
gh issue edit 32 --body $body

$body = @"
Build integration tests for end-to-end pipeline execution.

## Dependencies
- **Depends on**: #32 (unit tests first), #18 ✅ (orchestration)
- **Blocks**: Production deployment confidence

## Priority
Required before production launch
"@
gh issue edit 33 --body $body

$body = @"
Build evaluation harness to measure extraction accuracy.

## Dependencies
- **Depends on**: #32, #33 (test infrastructure)
- **Validates**: #4, #5 (extraction quality)

## Priority
Quality metrics for extraction pipeline
"@
gh issue edit 14 --body $body

$body = @"
Conduct performance and load testing for production readiness.

## Dependencies
- **Depends on**: #32, #33 (test infrastructure)
- **Required for**: Production launch

## Priority
Pre-production validation
"@
gh issue edit 34 --body $body

# Code Quality
Write-Host "`n✨ Code Quality..." -ForegroundColor Yellow

$body = @"
Set up Python code formatting with Black/Ruff.

## Dependencies
- **Depends on**: None (can start immediately)
- **Blocks**: #42, #43, #16

## Priority
🔴 Foundation for code quality standards
"@
gh issue edit 41 --body $body

$body = @"
Add mypy type checking to the codebase.

## Dependencies
- **Depends on**: #41 (formatting first)
- **Works with**: #43 (pre-commit)

## Priority
Type safety for maintainability
"@
gh issue edit 42 --body $body

$body = @"
Set up pre-commit hooks for automated code quality checks.

## Dependencies
- **Depends on**: #41, #42 (formatting and type checking)
- **Enforces**: Code quality standards automatically

## Priority
Automated quality enforcement
"@
gh issue edit 43 --body $body

# Infrastructure
Write-Host "`n🏗️ Infrastructure..." -ForegroundColor Yellow

$body = @"
Implement secrets management for API keys and credentials.

## Dependencies
- **Depends on**: None (can start immediately)
- **Blocks**: #27, #28

## Priority
🔴 **CRITICAL PATH** - Required for secure production deployment
"@
gh issue edit 23 --body $body

$body = @"
Set up structured logging infrastructure across all components.

## Dependencies
- **Depends on**: None (can start immediately)
- **Blocks**: #19, #25, #26

## Priority
🔴 **CRITICAL PATH** - Foundation for observability
"@
gh issue edit 24 --body $body

$body = @"
Add metrics collection and observability tooling.

## Dependencies
- **Depends on**: #24 (logging infrastructure)
- **Works with**: #19 (monitoring)

## Priority
Production observability
"@
gh issue edit 25 --body $body

$body = @"
Integrate Sentry for error tracking and alerting.

## Dependencies
- **Depends on**: #24 (logging)
- **Enhances**: Production error visibility

## Priority
Production error tracking and debugging
"@
gh issue edit 26 --body $body

$body = @"
Complete containerization of all components with Docker.

## Dependencies
- **Depends on**: #23 (secrets management)
- **Blocks**: #28 (cloud deployment)

## Priority
⚠️ Partially complete (Dagster containerized) - finish remaining components
"@
gh issue edit 27 --body $body

$body = @"
Set up automated cloud deployment pipeline.

## Dependencies
- **Depends on**: #23 (secrets), #27 (containerization)
- **Blocks**: Production launch

## Priority
Automated deployment for production
"@
gh issue edit 28 --body $body

$body = @"
Refine Python environment management with uv.

## Dependencies
- **Status**: ✅ Using uv (from #39)

## Priority
Refinement based on team feedback if needed
"@
gh issue edit 40 --body $body

# Documentation
Write-Host "`n📚 Documentation..." -ForegroundColor Yellow

$body = @"
Document development workflow and CI/CD basics.

## Dependencies
- **Depends on**: #41, #43 (code quality setup)
- **Status**: Ongoing - document as we implement

## Priority
Developer onboarding and process documentation
"@
gh issue edit 16 --body $body

$body = @"
Maintain comprehensive setup and architecture documentation.

## Dependencies
- **Status**: ✅ Wiki exists and is maintained

## Priority
Keep updated with architectural decisions as we build
"@
gh issue edit 17 --body $body

# Future Enhancements
Write-Host "`n🚀 Future Enhancements..." -ForegroundColor Yellow

$body = @"
Add conference ranking/tier data (A*, core rankings, etc).

## Dependencies
- **Depends on**: #7 (KB)

## Priority
P3 - Nice-to-have data enrichment
"@
gh issue edit 37 --body $body

$body = @"
Build manual review UI for quality control and data correction.

## Dependencies
- **Depends on**: #7 (KB), #20 (quality validation)

## Priority
P3 - Quality control tool for future
"@
gh issue edit 35 --body $body

Write-Host "`n✅ All issue relations updated in issue bodies!" -ForegroundColor Green
Write-Host "`nView any issue on GitHub to see the Dependencies section" -ForegroundColor Cyan
