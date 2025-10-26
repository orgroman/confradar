# Getting Started

This guide helps you set up the ConfRadar development environment using uv, Docker, and Dagster.

## Prerequisites

- Docker Desktop (for PostgreSQL, LiteLLM proxy, and Dagster services)
- Python 3.10+
- uv package manager

## Setup

```powershell
# Install uv (one-time)
iwr -useb https://astral.sh/uv/install.ps1 | iex

# From repo root, install dependencies (with dev extras)
uv sync --extra dev
```

## Start Services

Start all required services (PostgreSQL, LiteLLM, Dagster):

```powershell
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

Services will be available at:
- **Dagster UI**: http://localhost:3000
- **LiteLLM Proxy**: http://localhost:4000
- **PostgreSQL**: localhost:5432
- **pgAdmin**: http://localhost:5050 (email: admin@confradar.local, password: admin)

## Run tests

Tests use SQLite for fast execution (no PostgreSQL required):

```powershell
cd packages/confradar
uv run pytest -q
cd ../..
```

## Environment Configuration

Copy `.env.example` to `.env` and set your API keys:

```powershell
# Copy example env file
copy .env.example .env

# Edit .env and set your OpenAI API key
# CONFRADAR_SA_OPENAI=your-openai-api-key-here
```

## LiteLLM proxy (recommended)

The app talks to an OpenAI-compatible endpoint via the LiteLLM proxy (included in Docker Compose).

```powershell
# 1) Set your API key in .env file or environment
$env:CONFRADAR_SA_OPENAI = "<your-openai-key>"
# Alternative: $env:OPENAI_API_KEY = "..."

# 2) Proxy is automatically started by docker compose
# Listens on http://localhost:4000

# 3) (Optional) Override the base URL used by the app
$env:LITELLM_BASE_URL = "http://localhost:4000"  # default
# Or: $env:LLM_BASE_URL / $env:OPENAI_BASE_URL
```

## Database Setup

ConfRadar uses PostgreSQL for production and SQLite for testing.

### Initial Setup

Run Alembic migrations to create database tables:

```powershell
# Apply all migrations (creates tables in PostgreSQL)
uv run alembic upgrade head

# Verify tables were created
docker compose exec postgres psql -U confradar -d confradar -c "\dt"
```

### Create New Migrations

After modifying database models:

```powershell
# Generate migration
uv run alembic revision --autogenerate -m "Add new field"

# Apply migration
uv run alembic upgrade head
```

### Database Connection

Default (PostgreSQL via Docker):
```powershell
DATABASE_URL=postgresql+psycopg://confradar:confradar@localhost:5432/confradar
```

For local testing with SQLite:
```powershell
$env:DATABASE_URL = "sqlite:///test.db"
uv run alembic upgrade head
```

### Reset Database

```powershell
# Stop containers
docker compose down

# Remove PostgreSQL volume
docker volume rm confradar_postgres_data

# Restart and run migrations
docker compose up -d postgres
uv run alembic upgrade head
```

### Using pgAdmin

pgAdmin provides a web-based interface for managing PostgreSQL:

1. Open http://localhost:5050
2. Login with credentials (default: admin@confradar.local / admin)
3. Add server connection:
   - **Name**: ConfRadar Local
   - **Host**: postgres (or localhost if connecting from host)
   - **Port**: 5432
   - **Database**: confradar
   - **Username**: confradar
   - **Password**: confradar

You can now browse tables, run queries, and manage the database visually.

## Dagster Orchestration

ConfRadar uses Dagster for scheduling and monitoring the scraping pipeline.

### Using Docker (Recommended)

```powershell
# All services are already running from docker compose up -d
# Access the Dagster UI at: http://localhost:3000
```

### Run Dagster locally (Alternative)

```powershell
# Start Dagster webserver (Web UI on port 3000)
cd packages/confradar
$env:DATABASE_URL = "postgresql+psycopg://confradar:confradar@localhost:5432/confradar"
uv run dagster-webserver

# In another terminal, start Dagster daemon (for schedules)
cd packages/confradar
$env:DATABASE_URL = "postgresql+psycopg://confradar:confradar@localhost:5432/confradar"
uv run dagster-daemon run
```

Access the Dagster UI at: **http://localhost:3000**

### Run Dagster with Docker

```powershell
# Start all services (PostgreSQL, LiteLLM, Dagster daemon, Dagster webserver)
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

## Troubleshooting

### PostgreSQL Connection Issues

```powershell
# Check if PostgreSQL is running
docker compose ps postgres

# Check PostgreSQL logs
docker compose logs postgres

# Test connection
docker compose exec postgres psql -U confradar -d confradar -c "SELECT 1;"
```

### Port Conflicts

If ports 3000, 4000, or 5432 are already in use:

```powershell
# Check what's using the port
netstat -ano | findstr :5432

# Stop the conflicting service or change ports in docker-compose.yml
```

### Reset Everything

```powershell
# Stop all services
docker compose down

# Remove volumes
docker compose down -v

# Restart
docker compose up -d
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