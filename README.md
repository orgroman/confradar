# ConfRadar

[![Frontend CI](https://github.com/orgroman/confradar/actions/workflows/frontend.yml/badge.svg)](https://github.com/orgroman/confradar/actions/workflows/frontend.yml)
[![Deploy to Vercel](https://github.com/orgroman/confradar/actions/workflows/deploy-vercel.yml/badge.svg)](https://github.com/orgroman/confradar/actions/workflows/deploy-vercel.yml)

AI-powered agent that tracks academic conference deadlines by crawling CFP pages, extracting key dates with LLMs, detecting changes, and publishing to collaborative surfaces (Notion/Google Docs). Built in Python with LangChain; supports alias resolution, clustering of workshops, change history, and calendar export.

## Quick Links

- Project Board: https://github.com/users/orgroman/projects/6
- Wiki: https://github.com/orgroman/confradar/wiki
- Backlog (CSV): [`backlog.csv`](backlog.csv)
- Roadmap: [`ROADMAP.md`](ROADMAP.md) · Quarterly plan: [`docs/roadmap/2025Q4.md`](docs/roadmap/2025Q4.md)
- PRD (complete): [`docs/confradar_prd.md`](docs/confradar_prd.md)
- Implementation Plan: [`docs/confradar_implementation_plan.md`](docs/confradar_implementation_plan.md)
- Gap Analysis (complete): [`docs/PRD_GAP_ANALYSIS_COMPLETE.md`](docs/PRD_GAP_ANALYSIS_COMPLETE.md) · Summary: [`docs/COMPLETE_GAP_ANALYSIS_SUMMARY.md`](docs/COMPLETE_GAP_ANALYSIS_SUMMARY.md)
- Project Views setup: [`docs/PROJECT_VIEWS_SETUP.md`](docs/PROJECT_VIEWS_SETUP.md) · Quick ref: [`docs/PROJECT_VIEWS_QUICK_REF.md`](docs/PROJECT_VIEWS_QUICK_REF.md)
- Custom fields (Roadmap dates): [`docs/CUSTOM_FIELDS_SETUP.md`](docs/CUSTOM_FIELDS_SETUP.md)
- Project automations: [`docs/PROJECT_AUTOMATIONS.md`](docs/PROJECT_AUTOMATIONS.md)

## Status

- Issues: 61 (P0–P3), organized across 7 milestones (M1–M7)
- All issues assigned to @orgroman and set to Status = Todo in the project
- MVP scope prioritized in M1–M3 (seed crawling, extraction, KB)

## Getting Started (Dev)

We use uv for Python dependency management and fast workflows. You can still use pip, but uv is preferred.

### Prerequisites

- **Docker Desktop** (for PostgreSQL and services)
- **Python 3.10+**
- **uv** package manager

On Windows PowerShell:

```powershell
# Install uv (one-time)
iwr -useb https://astral.sh/uv/install.ps1 | iex

# Create venv and install deps (project + dev extras)
uv sync --extra dev
```

### Start Services

Start PostgreSQL, LiteLLM proxy, and Dagster services:

```powershell
# Start all services
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs -f postgres
```

### Database Setup

Run Alembic migrations to create database tables:

```powershell
# From repo root
uv run alembic upgrade head

# Generate new migration (after model changes)
uv run alembic revision --autogenerate -m "change message"
```

### Run Tests

```powershell
# From package directory
cd packages/confradar
uv run pytest -q
cd ../..
```

### CLI Usage

```powershell
uv run confradar parse --text "Submission: Nov 15, 2025 (AoE)"
uv run confradar fetch https://www.example.org/cfp
```

### Database Configuration

Default connection uses PostgreSQL via Docker Compose:
```powershell
# Default (PostgreSQL in Docker)
DATABASE_URL=postgresql+psycopg://confradar:confradar@localhost:5432/confradar

# For local testing with SQLite (optional)
$env:DATABASE_URL = "sqlite:///test.db"
uv run alembic upgrade head
```

See `.env.example` for all configuration options.

Notes:
- Monorepo structure will evolve (apps/, packages/, infra/). Current library lives under `src/confradar/` with tests in `tests/`.
- See P0/P1 issues for initial setup: project structure, SQLAlchemy ORM, LLM API config.
- Orchestration will use Airflow/Dagster; Docker and IaC tracked in infra issues.

Repo scripts and ops:

- Bootstrap GitHub artifacts: [`scripts/bootstrap_github.ps1`](scripts/bootstrap_github.ps1)
- Update milestones in bulk: [`scripts/update_milestones.ps1`](scripts/update_milestones.ps1)

## LiteLLM proxy (recommended)

Run a local LiteLLM proxy so the app can talk to an OpenAI-compatible endpoint without hard-coding a vendor. The proxy listens on http://localhost:4000 and is included in the Docker Compose setup.

1. Set your API key (service account preferred):

```powershell
$env:CONFRADAR_SA_OPENAI = "<your-openai-key>"
# Alternatively: $env:OPENAI_API_KEY = "..."
```

2. LiteLLM proxy starts automatically with Docker Compose:

```powershell
docker compose up -d
```

3. The app by default points to the proxy at http://localhost:4000. To override, set one of:

```powershell
$env:LITELLM_BASE_URL = "http://localhost:4000"  # default
# or
$env:LLM_BASE_URL = "https://api.openai.com/v1"
# or
$env:OPENAI_BASE_URL = "https://api.openai.com/v1"
```

### Accessing Services

- **Dagster UI**: http://localhost:3000
- **LiteLLM Proxy**: http://localhost:4000
- **PostgreSQL**: localhost:5432 (username: confradar, password: confradar)
- **pgAdmin**: http://localhost:5050 (email: admin@confradar.local, password: admin)

## Contributing

Please file issues on the Project Board and use the label taxonomy (type:*, area:*, priority:Px).

## Acknowledgements

This project aggregates public conference information; please respect robots.txt and source terms. PRs welcome for new sources and extraction rules.
