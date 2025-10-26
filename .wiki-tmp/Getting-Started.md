# Getting Started

This guide helps you set up the ConfRadar development environment using uv, Docker, and Dagster.

## Prerequisites

- Docker Desktop (for LiteLLM proxy and Dagster services)
- Python 3.11+
- uv package manager

## Setup

```powershell
# Install uv (one-time)
iwr -useb https://astral.sh/uv/install.ps1 | iex

# From repo root, install dependencies (with dev extras)
uv sync --extra dev
```

## Run tests

```powershell
cd packages/confradar
uv run pytest -q
cd ../..
```

## LiteLLM proxy (recommended)

The app talks to an OpenAI-compatible endpoint via the LiteLLM proxy by default.

```powershell
# 1) Set your API key (service account preferred)
$env:CONFRADAR_SA_OPENAI = "<your-openai-key>"
# Alternative: $env:OPENAI_API_KEY = "..."

# 2) Start the proxy (listens on http://localhost:4000)
docker compose up -d litellm

# 3) (Optional) Override the base URL used by the app
$env:LITELLM_BASE_URL = "http://localhost:4000"  # default
# Or: $env:LLM_BASE_URL / $env:OPENAI_BASE_URL
```

## Dagster Orchestration

ConfRadar uses Dagster for scheduling and monitoring the scraping pipeline.

### Run Dagster locally

```powershell
# Start Dagster webserver (Web UI on port 3000)
cd packages/confradar
uv run dagster-webserver

# In another terminal, start Dagster daemon (for schedules)
cd packages/confradar
uv run dagster-daemon run
```

Access the Dagster UI at: **http://localhost:3000**

### Run Dagster with Docker

```powershell
# Start all services (LiteLLM, Dagster daemon, Dagster webserver)
docker compose up -d

# View logs
docker compose logs -f dagster-webserver
```

Access the Dagster UI at: **http://localhost:3000**

### Materialize assets manually

From the UI:
1. Navigate to **Assets**
2. Select asset(s) you want to materialize
3. Click **Materialize**

From the CLI:
```powershell
cd packages/confradar

# Materialize all assets
uv run dagster asset materialize --select '*'

# Materialize specific scraper
uv run dagster asset materialize --select 'ai_deadlines_conferences'
```

### Daily Schedule

The pipeline runs automatically at **2:00 AM UTC** every day (configured in `daily_crawl_schedule`). This requires the Dagster daemon to be running.

## Database Setup

The default database is SQLite at `data/confradar.db` (created automatically).

### Run migrations

```powershell
# Apply all migrations
uv run alembic upgrade head

# Create a new migration (after modifying models)
uv run alembic revision --autogenerate -m "Add new field"
```

### Use PostgreSQL (optional)

```powershell
# Set DATABASE_URL
$env:DATABASE_URL = "postgresql+psycopg://user:pass@localhost:5432/confradar"

# Run migrations
uv run alembic upgrade head
```

## Monorepo layout

- Root is a uv workspace aggregator
- Main Python package: `packages/confradar`
- CLI entrypoint: `confradar`

Run the CLI without installing the package globally:

```powershell
uv run confradar parse --text "Submission: Nov 15, 2025 (AoE)"
```

## Next Steps

- Review the [Architecture](Architecture) to understand system design
- Read [Dagster Orchestration](Dagster-Orchestration) for detailed Dagster guide
- Check [Scraper Development](Scraper-Development) to add new sources
- See [Development Guide](Development-Guide) for coding standards

For more details, see the repository README.