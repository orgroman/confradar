# Dagster Orchestration

ConfRadar uses **Dagster** as its orchestration framework for scheduling, monitoring, and managing the data pipeline.

## Why Dagster?

- **Asset-based**: Models data transformations as versioned assets
- **Dependency inference**: Automatically builds DAG from function signatures
- **Web UI**: Rich interface for monitoring, debugging, and manual runs
- **Testing**: First-class support for unit and integration testing
- **Observability**: Built-in logging, metadata, and lineage tracking
- **Scheduling**: Cron-based schedules with timezone support
- **Extensibility**: Python-native with clean APIs

## Architecture Overview

```
┌─────────────────── Dagster Instance ───────────────────┐
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Scraper    │  │  Scraper    │  │  Scraper    │   │
│  │  Assets     │  │  Assets     │  │  Assets     │   │
│  │  (5 total)  │  │             │  │             │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
│         │                │                │           │
│         └────────────────┼────────────────┘           │
│                          ↓                            │
│                  ┌──────────────┐                     │
│                  │   Storage    │                     │
│                  │    Asset     │                     │
│                  └──────────────┘                     │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  crawl_job (define_asset_job)                │    │
│  │    Materializes: all assets                  │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  daily_crawl_schedule (ScheduleDefinition)   │    │
│  │    Cron: "0 2 * * *" (2 AM daily)            │    │
│  │    Job: crawl_job                             │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Assets

Assets represent materialized data products. Each asset declares its dependencies via function parameters.

### Scraper Assets

Located in `src/confradar/dagster/assets/scrapers.py`.

Each scraper asset:
1. Instantiates a Scrapy spider
2. Runs the spider via `CrawlerProcess`
3. Collects scraped items via signal dispatcher
4. Returns an `Output` with metadata

**Assets**:
- `ai_deadlines_conferences` - AI/ML conferences from ai-deadlines.com
- `acl_web_conferences` - NLP conferences from aclweb.org
- `chairing_tool_conferences` - Multi-discipline from chairing.app
- `elra_conferences` - Language resources from elra.info
- `wikicfp_conferences` - Broad coverage from wikicfp.com

**Group**: `scrapers`

**Example**:
```python
@asset(group_name="scrapers")
def ai_deadlines_conferences() -> Output[List[Dict]]:
    """Scrape AI/ML conference deadlines from ai-deadlines.com."""
    conferences = run_spider(AiDeadlinesSpider)
    return Output(
        value=conferences,
        metadata={
            "count": len(conferences),
            "source": "ai-deadlines.com",
            "preview": conferences[:3] if conferences else [],
        },
    )
```

**Metadata**:
- `count`: Number of conferences scraped
- `source`: Source website
- `preview`: First 3 conferences for quick inspection

### Storage Asset

Located in `src/confradar/dagster/assets/storage.py`.

The storage asset:
1. Receives conference lists from all scraper assets
2. Deduplicates by conference key (title + year)
3. Upserts to database using SQLAlchemy
4. Tracks all source URLs

**Asset**: `store_conferences`

**Group**: `storage`

**Dependencies**: Automatically inferred from parameters:
- `ai_deadlines_conferences`
- `acl_web_conferences`
- `chairing_tool_conferences`
- `elra_conferences`
- `wikicfp_conferences`

**Example**:
```python
@asset(group_name="storage")
def store_conferences(
    ai_deadlines_conferences: List[Dict],
    acl_web_conferences: List[Dict],
    chairing_tool_conferences: List[Dict],
    elra_conferences: List[Dict],
    wikicfp_conferences: List[Dict],
) -> Output[Dict[str, int]]:
    """Store all scraped conferences in database."""
    # Merge all sources
    all_conferences = (
        ai_deadlines_conferences
        + acl_web_conferences
        + chairing_tool_conferences
        + elra_conferences
        + wikicfp_conferences
    )
    
    # Upsert to database
    stats = save_to_db(all_conferences)
    
    return Output(
        value=stats,
        metadata={
            "total_scraped": stats["total"],
            "new_conferences": stats["created"],
            "updated_conferences": stats["updated"],
        },
    )
```

## Jobs

Jobs define which assets to materialize together.

**Job**: `crawl_job`

**Definition**:
```python
crawl_job = define_asset_job(
    name="crawl_job",
    description="Daily conference crawling pipeline - scrape all sources and store in database",
)
```

**Behavior**: Materializes all assets in dependency order:
1. Run all 5 scraper assets in parallel
2. Wait for all scrapers to complete
3. Run storage asset with scraper outputs

## Schedules

Schedules trigger jobs on a cron schedule.

**Schedule**: `daily_crawl_schedule`

**Definition**:
```python
daily_crawl_schedule = ScheduleDefinition(
    name="daily_crawl_schedule",
    job=crawl_job,
    cron_schedule="0 2 * * *",  # 2 AM UTC daily
    description="Run daily conference crawl pipeline",
)
```

**Execution**: Runs every day at 2:00 AM UTC.

## Configuration Files

### workspace.yaml

Tells Dagster where to find code locations.

**Location**: `packages/confradar/workspace.yaml`

```yaml
load_from:
  - python_package:
      package_name: confradar.dagster
      attribute: defs
```

### dagster.yaml

Instance configuration (storage, scheduler, logs).

**Location**: `packages/confradar/dagster.yaml`

```yaml
storage:
  postgres:
    postgres_db:
      username:
        env: POSTGRES_USER
      password:
        env: POSTGRES_PASSWORD
      hostname:
        env: POSTGRES_HOSTNAME
      db_name:
        env: POSTGRES_DB
      port: 5432

run_coordinator:
  module: dagster.core.run_coordinator
  class: QueuedRunCoordinator

run_launcher:
  module: dagster.core.launcher
  class: DefaultRunLauncher

scheduler:
  module: dagster.core.scheduler
  class: DagsterDaemonScheduler

compute_logs:
  module: dagster.core.storage.local_compute_log_manager
  class: LocalComputeLogManager
  config:
    base_dir: /opt/dagster/dagster_home/logs

run_retries:
  enabled: true
  max_retries: 3

retention:
  schedule:
    purge_after_days: 90

telemetry:
  enabled: false
```

## Running Dagster

### Local Development

**Start webserver**:
```powershell
cd packages/confradar
uv run dagster-webserver
```

Access UI at: http://localhost:3000

**Start daemon** (for schedules):
```powershell
uv run dagster-daemon run
```

### Docker

**Start services**:
```powershell
docker-compose up dagster-daemon dagster-webserver
```

**Services**:
- `dagster-daemon`: Runs schedules and sensors
- `dagster-webserver`: Web UI on port 3000

**Dockerfile**: `Dockerfile.dagster`
- Base: Python 3.11-slim
- Package manager: uv
- Sets `DAGSTER_HOME=/opt/dagster/dagster_home`
- Copies workspace.yaml and dagster.yaml

## Materializing Assets

### Via UI

1. Open http://localhost:3000
2. Navigate to **Assets**
3. Select asset(s)
4. Click **Materialize**

### Via CLI

**All assets**:
```powershell
cd packages/confradar
uv run dagster asset materialize --select '*'
```

**Specific asset**:
```powershell
uv run dagster asset materialize --select 'ai_deadlines_conferences'
```

**Downstream assets**:
```powershell
uv run dagster asset materialize --select 'ai_deadlines_conferences+'
```

**Upstream and downstream**:
```powershell
uv run dagster asset materialize --select '+store_conferences+'
```

## Monitoring

### Asset Lineage

View the asset graph in the UI:
- **Assets** tab → **Lineage**
- Shows dependencies and data flow
- Click nodes to see details

### Run History

View past runs:
- **Runs** tab
- Filter by status (success, failed, in progress)
- Click run to see logs and timing

### Logs

Each asset produces logs:
- Standard output/error
- Dagster context logs
- Custom metadata

View in UI:
- **Runs** tab → Select run → Click asset

### Metadata

Assets attach metadata to outputs:
- Conference count
- Source name
- Preview of data
- Timing information

View in UI:
- **Assets** tab → Select asset → **Metadata** tab

## Testing

### Unit Tests

Located in `tests/test_dagster.py`.

Tests verify:
- Definitions load without errors
- All expected assets exist
- Job is defined
- Schedule exists with correct cron

**Run tests**:
```powershell
cd packages/confradar
uv run pytest tests/test_dagster.py -v
```

### Integration Tests

Mark tests with `@pytest.mark.integration`:
```python
@pytest.mark.integration
def test_materialize_scrapers():
    """Test scraper assets can be materialized."""
    # ... test code
```

**Run integration tests**:
```powershell
uv run pytest tests/test_dagster.py -v -m integration
```

### Mocking

Use Dagster's built-in testing utilities:
```python
from dagster import materialize

# Materialize single asset
result = materialize([my_asset])
assert result.success

# Materialize with dependencies
result = materialize([scraper_asset, storage_asset])
assert result.success
```

## Debugging

### View Asset Outputs

In the UI:
- **Assets** tab → Select asset → **Materializations**
- Shows metadata from most recent run

### Check Logs

- **Runs** tab → Select run → Click asset
- View stdout, stderr, and Dagster logs
- Filter by log level (DEBUG, INFO, WARNING, ERROR)

### Local Execution

Run assets directly in Python:
```python
from confradar.dagster.assets.scrapers import ai_deadlines_conferences

# Run asset function
result = ai_deadlines_conferences()
print(result.value)  # List of conferences
print(result.metadata)  # Count, source, preview
```

## Common Issues

### Schedule Not Running

**Symptom**: Daily schedule doesn't trigger.

**Solution**: Ensure daemon is running:
```powershell
uv run dagster-daemon run
```

Or in Docker:
```powershell
docker-compose up dagster-daemon
```

### Asset Materialization Fails

**Symptom**: Asset shows as failed in UI.

**Solution**:
1. Check logs for error message
2. Verify dependencies (e.g., database connection)
3. Test asset function directly in Python
4. Check for network issues (scrapers)

### Database Connection Error

**Symptom**: Storage asset fails with database error.

**Solution**:
1. Verify `DATABASE_URL` environment variable
2. Ensure database exists and is accessible
3. Run migrations: `uv run alembic upgrade head`

### LLM API Error (Future)

**Symptom**: Extraction assets fail with API error.

**Solution**:
1. Check `CONFRADAR_SA_OPENAI` or `OPENAI_API_KEY`
2. Verify LiteLLM proxy is running (if using)
3. Check API quota and rate limits

## Best Practices

### Asset Design

- **Idempotent**: Assets should produce same output for same input
- **Stateless**: Don't rely on global state or side effects
- **Metadata**: Include rich metadata for debugging
- **Error Handling**: Catch and log errors gracefully

### Scheduling

- **Off-peak**: Schedule heavy jobs during low-traffic hours
- **Retry**: Enable retries for transient failures
- **Backfills**: Use Dagster backfills for historical data

### Testing

- **Unit**: Test asset logic in isolation
- **Integration**: Test asset dependencies
- **End-to-end**: Test full pipeline with real data

### Monitoring

- **Alerts**: Set up notifications for failures
- **Metrics**: Track success rate, duration, data volume
- **Logs**: Include contextual information in logs

## Future Enhancements

### Data Quality Checks

Add Dagster asset checks:
```python
from dagster import asset_check, AssetCheckResult

@asset_check(asset=ai_deadlines_conferences)
def check_conference_count(conferences):
    """Verify we scraped a reasonable number of conferences."""
    count = len(conferences)
    return AssetCheckResult(
        passed=count > 10,
        description=f"Scraped {count} conferences",
    )
```

### Partitioned Assets

Partition by date for incremental processing:
```python
@asset(partitions_def=DailyPartitionsDefinition(start_date="2024-01-01"))
def daily_conferences(context):
    """Scrape conferences for a specific date."""
    date = context.partition_key
    # ... scrape for date
```

### Multi-Asset Operations

Materialize multiple scrapers as one asset:
```python
@multi_asset(
    outs={
        "ai_deadlines": AssetOut(),
        "acl_web": AssetOut(),
    }
)
def scrape_all_sources():
    """Scrape all sources in one operation."""
    # ... scrape logic
    return ai_deadlines_data, acl_web_data
```

## Resources

- **Dagster Documentation**: https://docs.dagster.io/
- **Dagster University**: https://dagster.io/university
- **ConfRadar Dagster Code**: `packages/confradar/src/confradar/dagster/`
- **Tests**: `packages/confradar/tests/test_dagster.py`

## Next Steps

1. Monitor daily runs for a week
2. Add data quality checks
3. Implement extraction assets (M3)
4. Add partitioning for incremental updates
5. Set up alerting for failures
