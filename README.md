# ConfRadar

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

On Windows PowerShell:

```powershell
# Install uv (one-time)
iwr -useb https://astral.sh/uv/install.ps1 | iex

# Create venv and install deps (project + dev extras)
uv sync --extra dev

# Run tests (from package directory)
cd packages/confradar
uv run pytest -q
cd ../..

uv run confradar parse --text "Submission: Nov 15, 2025 (AoE)"
uv run confradar fetch https://www.example.org/cfp

### Database migrations (Alembic)

Generate and apply migrations using Alembic. Default DB URL is `sqlite:///confradar.db`.

```powershell
# From repo root
uv run alembic revision --autogenerate -m "change message"
uv run alembic upgrade head

# Override DB URL (e.g., PostgreSQL)
$env:DATABASE_URL = "postgresql+psycopg://user:pass@localhost:5432/confradar"
uv run alembic upgrade head
```
```

Notes:
- Monorepo structure will evolve (apps/, packages/, infra/). Current library lives under `src/confradar/` with tests in `tests/`.
- See P0/P1 issues for initial setup: project structure, SQLAlchemy ORM, LLM API config.
- Orchestration will use Airflow/Dagster; Docker and IaC tracked in infra issues.

Repo scripts and ops:

- Bootstrap GitHub artifacts: [`scripts/bootstrap_github.ps1`](scripts/bootstrap_github.ps1)
- Update milestones in bulk: [`scripts/update_milestones.ps1`](scripts/update_milestones.ps1)

## LiteLLM proxy (recommended)

Run a local LiteLLM proxy so the app can talk to an OpenAI-compatible endpoint without hard-coding a vendor. The proxy listens on http://localhost:4000.

1. Set your API key (service account preferred):

```powershell
$env:CONFRADAR_SA_OPENAI = "<your-openai-key>"
# Alternatively: $env:OPENAI_API_KEY = "..."
```

2. Start the proxy with Docker Compose from the repo root:

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

## Contributing

Please file issues on the Project Board and use the label taxonomy (type:*, area:*, priority:Px).

## Acknowledgements

This project aggregates public conference information; please respect robots.txt and source terms. PRs welcome for new sources and extraction rules.
