# Architecture

## System Overview

ConfRadar is built as a modular pipeline with clear separation of concerns. The system uses **Dagster** for orchestration, ensuring reliable scheduling, monitoring, and data lineage tracking.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Dagster Orchestration                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Scrapers   │→ │   Storage    │→ │  Extraction  │→  ...    │
│  │   (Assets)   │  │   (Assets)   │  │   (Assets)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         Daily Schedule (2 AM)  •  Web UI  •  Monitoring         │
└─────────────────────────────────────────────────────────────────┘
           ↓                    ↓                    ↓
    ┌──────────┐         ┌──────────┐        ┌──────────┐
    │   Web    │         │ Database │        │   LLM    │
    │ Sources  │         │ (SQLite) │        │  (API)   │
    └──────────┘         └──────────┘        └──────────┘
```

## Core Components

### 1. Orchestration Layer (Dagster)

**Purpose**: Schedules, monitors, and tracks data lineage across the entire pipeline.

**Key Features**:
- **Asset-based architecture**: Each step is a materialized asset
- **Automatic dependency inference**: Assets declare dependencies via parameters
- **Web UI**: Monitor runs, view logs, materialize assets manually
- **Scheduling**: Daily cron schedule for automated scraping
- **Retry logic**: Automatic retries on transient failures

**Assets**:
- `ai_deadlines_conferences` - Scrapes AI Deadlines aggregator
- `acl_web_conferences` - Scrapes ACL anthology
- `chairing_tool_conferences` - Scrapes Chairing Tool database
- `elra_conferences` - Scrapes ELRA (European Language Resources)
- `wikicfp_conferences` - Scrapes WikiCFP
- `store_conferences` - Saves all scraped data to database

**Jobs**:
- `crawl_job` - Materializes all scraper + storage assets

**Schedules**:
- `daily_crawl_schedule` - Runs `crawl_job` daily at 2 AM (UTC)

**Configuration**:
- `workspace.yaml` - Points to ConfRadar Dagster package
- `dagster.yaml` - Instance settings (storage, scheduler, logs)

**Docker Services**:
- `dagster-daemon` - Runs schedules and sensors in background
- `dagster-webserver` - Web UI on port 3000

### 2. Data Retrieval Layer

**Purpose**: Discovers and fetches conference information from various sources.

**Technologies**:
- **Scrapy framework**: Production-grade web scraping with:
  - Concurrent requests with rate limiting
  - Automatic retries and error handling
  - Middleware for headers, cookies, user agents
  - Pipeline for data processing and validation
- **Spider templates**: One spider per source (AI Deadlines, ACL, WikiCFP, etc.)
- **Item models**: Structured data containers with validation

**Current Sources**:
1. **AI Deadlines** (ai-deadlines.com)
   - Coverage: AI/ML conferences
   - Update frequency: Community-maintained
   - Data quality: High (curated)

2. **ACL Web** (aclweb.org)
   - Coverage: NLP/CL conferences
   - Update frequency: Official
   - Data quality: High (authoritative)

3. **Chairing Tool** (chairing.app)
   - Coverage: Multi-discipline
   - Update frequency: Event organizers
   - Data quality: Medium-High

4. **ELRA** (elra.info)
   - Coverage: Language resources
   - Update frequency: Official
   - Data quality: High

5. **WikiCFP** (wikicfp.com)
   - Coverage: Broad (all fields)
   - Update frequency: Community-submitted
   - Data quality: Variable

**Scrapy Architecture**:
```
Spider → Item → Pipeline → Database
  ↓
Middleware (Headers, Retries, Rate Limiting)
```

### 3. Data Storage Layer

**Purpose**: Persists conference data with deduplication and versioning.

**Technologies**:
- **SQLAlchemy ORM**: Database abstraction
- **PostgreSQL**: Primary database (Docker Compose, production)
- **SQLite**: Legacy support for local testing only
- **Alembic**: Schema migrations

> **Note**: Migration from SQLite to PostgreSQL is in progress (P0, M1). PostgreSQL is required for production deployments due to better concurrency, transaction handling, and cloud compatibility. See [PostgreSQL Migration Issue](../issues/postgres-migration.md) for details.

**Models**:
- `Conference`: Core conference entity
  - Unique constraint on `key` (derived from title + year)
  - Fields: title, acronym, year, deadline, venue, etc.
  - Timestamps: created_at, updated_at
  
- `Source`: Source URL tracking
  - Many-to-one relationship with Conference
  - Fields: url, source_name, scraped_at
  - Enables multi-source reconciliation

**Deduplication Strategy**:
- Generate unique key from `title + year`
- Use SQLAlchemy `merge()` for upsert semantics
- Track all source URLs per conference
- Preserve original scraped data for audit

**Migrations**:
```powershell
# Create migration
uv run alembic revision --autogenerate -m "Add new field"

# Apply migrations
uv run alembic upgrade head
```

### 4. Data Extraction Layer (Planned - M3)

**Purpose**: Extract structured information from unstructured text using LLMs.

**Technologies**:
- **LiteLLM**: Provider-agnostic LLM client
- **LangChain**: Orchestration and prompt management
- **Pydantic**: Output validation and structured parsing

**Extraction Tasks**:
- Date parsing (submission, notification, camera-ready)
- Venue extraction (city, country, dates)
- Event type classification (conference, workshop, symposium)
- Topic/track identification

**LLM Configuration**:
- Default: OpenAI GPT-4
- Endpoint: `http://localhost:4000` (LiteLLM proxy)
- API key: `CONFRADAR_SA_OPENAI` or `OPENAI_API_KEY`
- Fallback: Direct OpenAI API

### 5. Knowledge Organization Layer (Planned - M4-M5)

**Purpose**: Resolve aliases, cluster related events, and build conference graph.

**Components**:

**Alias Resolution**:
- Detect duplicates (e.g., "NeurIPS" = "NIPS")
- Use string similarity + LLM validation
- Maintain canonical names

**Workshop Clustering**:
- Link workshops to parent conferences
- Extract hierarchical relationships
- Group by year and edition

**Graph Database** (optional):
- Nodes: Conferences, Workshops, Venues, Organizations
- Edges: PartOf, SameAs, SuccessorOf
- Enable complex queries and recommendations

### 6. Change Detection Layer (Planned - M5)

**Purpose**: Track modifications to conference data over time.

**Features**:
- Version history for each conference
- Diff computation on updates
- Notification triggers for important changes (deadline extensions)
- Audit log for all modifications

**Implementation**:
- Store snapshots on each scrape
- Compute deltas using difflib or custom logic
- Flag significant changes (dates, venues)
- Generate alerts for subscribed users

### 7. Serving Layer (Planned - M6)

**Purpose**: Expose conference data through APIs and integrations.

**Interfaces**:

**REST API**:
- `/conferences` - List/search conferences
- `/conferences/{id}` - Get conference details
- `/conferences/{id}/history` - Version history
- `/workshops` - List workshops
- `/deadlines` - Upcoming deadlines

**Notion Integration**:
- Sync conferences to Notion database
- Update properties on changes
- Create calendar views

**Google Docs Integration**:
- Generate formatted tables
- Automatic updates via Apps Script

**Calendar Export**:
- Generate .ics files
- One event per deadline
- Include venue and links

### 8. Evaluation Layer (Planned - M7)

**Purpose**: Measure system accuracy and coverage.

**Metrics**:
- **Retrieval Coverage**: % of known conferences found
- **Extraction Accuracy**: Precision/recall on date parsing
- **Alias Resolution**: F1 score on duplicate detection
- **Change Detection**: Time to detect updates
- **End-to-End Latency**: Crawl → Serve time

**Test Sets**:
- Gold standard conference list (top-tier venues)
- Manual annotations for dates, venues
- Historical data for change detection

## Data Flow

### Daily Pipeline Run

1. **2:00 AM UTC** - Dagster schedule triggers `crawl_job`
2. **Scraping Phase** - All 5 scraper assets run in parallel:
   - Fetch HTML from each source
   - Parse with Scrapy selectors
   - Extract conference items
   - Validate with Pydantic schemas
3. **Storage Phase** - `store_conferences` asset runs:
   - Receives conference lists from all scrapers
   - Deduplicates by conference key
   - Upserts to database
   - Tracks source URLs
4. **Monitoring** - Dagster logs:
   - Number of conferences scraped per source
   - Database write statistics
   - Any errors or warnings
5. **Completion** - Results visible in Dagster UI

### Manual Asset Materialization

Developers can trigger assets manually:

```powershell
# Materialize all assets
uv run dagster asset materialize --select '*'

# Materialize specific scraper
uv run dagster asset materialize --select 'ai_deadlines_conferences'

# Materialize storage only (uses cached scraper outputs)
uv run dagster asset materialize --select 'store_conferences'
```

### Web UI Access

```powershell
# Local development
uv run dagster-webserver
# Access at http://localhost:3000

# Docker
docker-compose up dagster-webserver
# Access at http://localhost:3000
```

## Deployment Architecture

### Local Development

```
Developer Machine
  ├── SQLite database (data/confradar.db)
  ├── LiteLLM proxy (Docker, port 4000)
  ├── Dagster webserver (Python, port 3000)
  └── Dagster daemon (Python, background)
```

### Production (Planned)

```
Cloud Infrastructure
  ├── PostgreSQL (managed DB)
  ├── Dagster Cloud or self-hosted
  ├── LiteLLM proxy (container)
  ├── Redis (caching)
  └── Object storage (logs, artifacts)
```

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Orchestration** | Dagster 1.8+ |
| **Web Scraping** | Scrapy 2.11+ |
| **Database** | SQLAlchemy, SQLite/PostgreSQL |
| **Migrations** | Alembic |
| **LLM Access** | LiteLLM, OpenAI |
| **Validation** | Pydantic |
| **Testing** | pytest, pytest-cov |
| **Containers** | Docker, docker-compose |
| **Package Management** | uv (Python) |
| **CI/CD** | GitHub Actions |

## Configuration Management

All configuration via environment variables:

```powershell
# Database
$env:DATABASE_URL = "sqlite:///data/confradar.db"  # or postgresql://...

# LLM
$env:CONFRADAR_SA_OPENAI = "sk-..."  # preferred
$env:OPENAI_API_KEY = "sk-..."      # fallback
$env:LITELLM_BASE_URL = "http://localhost:4000"

# Dagster
$env:DAGSTER_HOME = "/opt/dagster/dagster_home"
```

Settings loaded via Pydantic:
- `src/confradar/settings.py`
- Validates types and provides defaults
- Accessible via `get_settings()`

## Monitoring & Observability

### Dagster UI (Current)

- **Asset Lineage**: Visual graph of dependencies
- **Run History**: Success/failure rates, duration
- **Logs**: Per-asset execution logs with filtering
- **Metadata**: Custom metadata on each asset (e.g., conference count)

### Future Enhancements

- **Prometheus Metrics**: Scrape success rate, latency, DB growth
- **Error Alerting**: Email/Slack on pipeline failures
- **Data Quality Checks**: Dagster asset checks for anomalies
- **Cost Tracking**: LLM API usage and cost per run

## Security Considerations

- **API Keys**: Stored in environment variables, never committed
- **Database**: Use read-only users for serving layer
- **Web Scraping**: Respect robots.txt, rate limits
- **LLM**: Sanitize inputs to avoid prompt injection
- **Docker**: Run containers as non-root users

## Scalability

### Current Limitations

- Single-threaded Scrapy per source
- SQLite limits concurrent writes
- No caching layer

### Future Improvements

- **Horizontal Scaling**: Multiple Dagster workers
- **Database**: PostgreSQL with connection pooling
- **Caching**: Redis for API responses
- **CDN**: Static assets and calendar exports
- **Queue**: Celery for async tasks

## Testing Strategy

### Unit Tests
- Test individual spiders in isolation
- Mock HTTP responses with fixtures
- Validate Pydantic models

### Integration Tests
- Test full Dagster pipeline with test DB
- Verify asset dependencies resolve
- Check database writes

### End-to-End Tests
- Run against live (test) sources
- Verify LLM extraction on real data
- Test Notion/Docs sync

## Next Steps

1. **M3 - Extraction**: Implement LLM-based date/venue extraction
2. **M4 - Clustering**: Build alias resolution and workshop clustering
3. **M5 - Change Detection**: Add versioning and diff computation
4. **M6 - Serving**: Create REST API and integrations
5. **M7 - Evaluation**: Build test sets and metrics

See [Roadmap](Roadmap) for detailed timeline.
