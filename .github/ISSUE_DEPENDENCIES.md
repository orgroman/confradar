# Issue Dependencies and Relations

## Critical Path Analysis

### Foundation Layer (Must Complete First)

#### Schema & Infrastructure
- **#3 - Define ConfRadar event schema** (P1, area:kb)
  - Blocks: #7, #8, #20, #22
  - Must complete before any KB work

- **#39 - Project setup: uv, linting, structure** (CLOSED ✅)
  - Completed - foundation is ready

#### Core Storage
- **#7 - Knowledge base storage** (P1, area:kb)
  - Depends on: #3 (schema definition)
  - Blocks: #8, #20, #22, #36
  - Must complete before change detection

- **#22 - Database schema migrations** (P1, area:kb)
  - Depends on: #3, #7
  - Blocks: Production deployments

### Data Pipeline Layer

#### Retrieval Foundation
- **#1 - Seeded crawling for top CS conferences** (P1, area:retrieval)
  - Blocks: #4, #5, #38
  - First data source

- **#2 - Search fallback for discovery** (P2, area:retrieval)
  - Depends on: #1 (validate approach first)
  - Extends discovery beyond seeds

#### Extraction Core
- **#4 - Extraction: rule-first parser** (P1, area:extraction)
  - Depends on: #1 (needs data to parse)
  - Blocks: #5, #6
  - Core extraction logic

- **#5 - Extraction: LLM fallback for edge cases** (P1, area:extraction)
  - Depends on: #4 (rule-first must exist)
  - Depends on: #53 (LLM API setup) - CLOSED ✅
  - Handles complex cases

- **#6 - Timezone/AoE handling** (P1, area:extraction)
  - Depends on: #4 (part of date extraction)
  - Critical for deadline accuracy

### Intelligence Layer

#### Change Detection & Quality
- **#8 - Change detection for dates** (P1, area:kb)
  - Depends on: #7 (needs KB to store history)
  - Depends on: #4 (needs extraction working)
  - Blocks: #19, #31

- **#20 - Data quality validation** (P1, area:kb)
  - Depends on: #7 (needs KB)
  - Depends on: #4 (validates extracted data)
  - Blocks: Production readiness

#### Clustering & Deduplication
- **#9 - Alias normalization rules** (P2, area:clustering)
  - Depends on: #7 (needs KB)
  - Blocks: #10, #36

- **#10 - Alias clustering via embeddings** (P2, area:clustering)
  - Depends on: #9 (builds on normalization)
  - Blocks: #11, #36

- **#11 - Workshop → parent linkage** (P2, area:clustering)
  - Depends on: #10 (needs clustering)
  - Enhances deduplication

- **#36 - Data deduplication beyond clustering** (P2, area:kb)
  - Depends on: #9, #10, #11
  - Advanced deduplication logic

- **#38 - Multi-source reconciliation** (P2, area:extraction)
  - Depends on: #1, #2, #9, #10
  - Merges data from multiple sources

### Orchestration Layer

- **#18 - Dagster orchestration** (CLOSED ✅)
  - Foundation complete
  - Now enables: #19, #21

- **#19 - Pipeline monitoring and alerting** (P1, area:infra)
  - Depends on: #18 (orchestration) ✅
  - Depends on: #8 (change detection)
  - Blocks: Production ops

- **#21 - Retry logic and error handling** (P1, area:infra)
  - Depends on: #18 (orchestration) ✅
  - Blocks: Reliable operations

### Serving Layer

- **#12 - Serving: Notion adapter** (P1, area:serving)
  - Depends on: #7 (needs KB to query)
  - Depends on: #8 (show updates)
  - Primary serving interface

- **#13 - Serving: Google Docs adapter** (P2, area:serving)
  - Depends on: #7, #8
  - Alternative serving option

- **#15 - Calendar export (.ics)** (P3, area:serving)
  - Depends on: #7
  - Nice-to-have export

- **#29 - REST API for queries** (P2, area:serving)
  - Depends on: #7
  - Blocks: #30 (auth)

- **#30 - API authentication and rate limiting** (P3, area:serving)
  - Depends on: #29
  - Production API requirement

- **#31 - Email/Slack notifications** (P2, area:serving)
  - Depends on: #8 (change detection)
  - Depends on: #12 or #29 (data access)

### Infrastructure & Quality

#### Testing Suite
- **#32 - Unit test suite** (P1, area:infra)
  - Blocks: #33, #34
  - Foundation for testing

- **#33 - Integration tests for pipelines** (P1, area:infra)
  - Depends on: #32 (unit tests first)
  - Depends on: #18 (orchestration) ✅

- **#14 - Evaluation harness** (P2, area:infra)
  - Depends on: #32, #33
  - Validates extraction quality

- **#34 - Performance and load testing** (P2, area:infra)
  - Depends on: #32, #33
  - Pre-production validation

#### Code Quality
- **#41 - Python code formatting (Black/Ruff)** (P1, area:infra)
  - Blocks: #42, #43
  - Foundation for code quality

- **#42 - Type checking with mypy** (P2, area:infra)
  - Depends on: #41
  - Should pair with #43

- **#43 - Pre-commit hooks for Python** (P2, area:infra)
  - Depends on: #41, #42
  - Enforces quality

#### Environment & Deployment
- **#40 - Python environment management** (P1, area:infra)
  - Using uv (from #39) ✅
  - May need refinement

- **#27 - Containerization (Docker)** (P1, area:infra)
  - Partially done (Dagster) ✅
  - Depends on: #23 (secrets)
  - Blocks: #28

- **#23 - Secrets management** (P1, area:infra)
  - Blocks: #27, #28
  - Critical for production

- **#28 - Cloud deployment automation** (P1, area:infra)
  - Depends on: #27, #23
  - Blocks: Production launch

#### Observability
- **#24 - Logging infrastructure** (P1, area:infra)
  - Blocks: #25, #26, #19
  - Foundation for monitoring

- **#25 - Metrics and observability** (P2, area:infra)
  - Depends on: #24
  - Works with #19

- **#26 - Error tracking (Sentry integration)** (P2, area:infra)
  - Depends on: #24
  - Production error tracking

### Documentation & Process

- **#16 - Dev workflow and CI basics** (P2, area:infra)
  - Depends on: #41, #43
  - Blocks: Team efficiency

- **#17 - Docs: Setup & architecture** (P2, docs, area:infra)
  - Ongoing - Wiki exists ✅
  - Should document decisions as we go

### Future Enhancements

- **#37 - Conference ranking/tier data** (P3, area:kb)
  - Depends on: #7
  - Enhancement feature

- **#35 - Manual review UI/workflow** (P3, area:infra)
  - Depends on: #7, #20
  - Quality control tool

## Recommended Issue Updates

### Add "blocked-by" Labels
Create the following relationships in GitHub:

```bash
# Foundation blockers
gh issue edit 7 --add-label "blocked-by:3"
gh issue edit 8 --add-label "blocked-by:7"
gh issue edit 20 --add-label "blocked-by:7"
gh issue edit 22 --add-label "blocked-by:3,7"

# Extraction chain
gh issue edit 4 --add-label "blocked-by:1"
gh issue edit 5 --add-label "blocked-by:4"
gh issue edit 6 --add-label "blocked-by:4"

# Clustering chain
gh issue edit 10 --add-label "blocked-by:9"
gh issue edit 11 --add-label "blocked-by:10"
gh issue edit 36 --add-label "blocked-by:9,10,11"

# Orchestration dependencies
gh issue edit 19 --add-label "blocked-by:8"
gh issue edit 33 --add-label "blocked-by:32"

# Serving dependencies
gh issue edit 12 --add-label "blocked-by:7,8"
gh issue edit 13 --add-label "blocked-by:7,8"
gh issue edit 31 --add-label "blocked-by:8,12"

# Infrastructure
gh issue edit 42 --add-label "blocked-by:41"
gh issue edit 43 --add-label "blocked-by:41,42"
gh issue edit 27 --add-label "blocked-by:23"
gh issue edit 28 --add-label "blocked-by:23,27"
gh issue edit 25 --add-label "blocked-by:24"
gh issue edit 26 --add-label "blocked-by:24"
```

### Create Sub-Issues
Consider breaking down these large issues:

- **#3 (Schema)** → Sub-issues:
  - Core event schema fields
  - Series relationship model
  - Workshop linkage schema
  - Change history schema

- **#7 (KB Storage)** → Sub-issues:
  - Database selection & setup
  - Core tables implementation
  - Version history mechanism
  - Query interface

- **#12 (Notion Adapter)** → Sub-issues:
  - Notion API integration
  - Data sync logic
  - Update notification formatting
  - Error handling & rate limiting

### Priority Adjustments Recommended

**Increase to P0 (Critical - Immediate):**
- #3 - Define schema (blocks everything)
- #7 - KB storage (blocks core features)
- #4 - Extraction parser (core functionality)

**Keep at P1 (High):**
- #1, #5, #6, #8, #12, #19, #20, #21, #23, #24, #27, #28, #32, #33, #40, #41

**Consider lowering to P3:**
- #16 - Dev workflow (nice-to-have, can document as we go)
- #40 - Environment (already using uv, refinement can wait)

## Next 5 Issues to Focus On

1. **#3 - Define ConfRadar event schema** - MUST DO FIRST
2. **#7 - Knowledge base storage** - Second critical path
3. **#1 - Seeded crawling** - Start data collection
4. **#4 - Extraction: rule-first parser** - Parse collected data
5. **#41 - Python code formatting** - Set quality standards

## Sprint Grouping Suggestion

### Sprint 1: Foundation (Current)
- [x] #39 - Project setup ✅
- [x] #18 - Dagster orchestration ✅
- [x] #53 - LLM API setup ✅
- [ ] #3 - Define schema
- [ ] #7 - KB storage
- [ ] #22 - Migrations

### Sprint 2: Data Pipeline
- [ ] #1 - Seeded crawling
- [ ] #4 - Rule-first parser
- [ ] #6 - Timezone handling
- [ ] #5 - LLM fallback

### Sprint 3: Intelligence
- [ ] #8 - Change detection
- [ ] #9 - Alias normalization
- [ ] #10 - Alias clustering
- [ ] #20 - Data quality

### Sprint 4: Production Ready
- [ ] #19 - Monitoring/alerting
- [ ] #21 - Retry logic
- [ ] #24 - Logging
- [ ] #32 - Unit tests
- [ ] #33 - Integration tests

### Sprint 5: Serving
- [ ] #12 - Notion adapter
- [ ] #31 - Notifications
- [ ] #29 - REST API
