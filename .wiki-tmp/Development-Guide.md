# Development Guide

This guide covers development workflows for the ConfRadar monorepo with uv and the LiteLLM proxy.

## Environment

- Python: 3.11+
- Dependency manager: uv
- Package: `packages/confradar`

```powershell
uv sync --extra dev
cd packages/confradar
uv run pytest -q
```

## LLM configuration

- API key: `CONFRADAR_SA_OPENAI` (preferred) or `OPENAI_API_KEY`
- Base URL (OpenAI-compatible): defaults to `http://localhost:4000`
- Override via: `LITELLM_BASE_URL`, `LLM_BASE_URL`, or `OPENAI_BASE_URL`
- Local proxy: `docker compose up -d` (from repo root)

## Coding standards

- Format: black
- Lint: ruff
- Tests: pytest (+ pytest-cov)

```powershell
cd packages/confradar
uv run ruff check
uv run black --check src tests
uv run pytest -q
```

## CI

GitHub Actions runs uv sync and tests on Windows and Ubuntu for pull requests.

## Notes

- Keep public APIs stable; add tests when changing behavior
- Prefer provider-agnostic LLM usage via LiteLLM (client or proxy)
- No real LLM calls in unit tests; mock LiteLLM

## Database migrations (Alembic)

We use Alembic for schema migrations.

```powershell
# Generate a new migration (autogenerate from models)
uv run alembic revision --autogenerate -m "<message>"

# Apply migrations
uv run alembic upgrade head

# Point to a different DB
$env:DATABASE_URL = "postgresql+psycopg://user:pass@localhost:5432/confradar"
uv run alembic upgrade head
```

## Dagster Development

### Running Dagster locally

```powershell
cd packages/confradar

# Start webserver (UI on port 3000)
uv run dagster-webserver

# Start daemon (for schedules)
uv run dagster-daemon run
```

### Testing Dagster assets

```powershell
# Run Dagster tests
uv run pytest tests/test_dagster.py -v

# Run with integration tests (requires network)
uv run pytest tests/test_dagster.py -v -m integration
```

### Adding new scraper assets

1. Create spider in `src/confradar/scrapers/spiders/`
2. Add asset function in `src/confradar/dagster/assets/scrapers.py`
3. Import and add to `Definitions` in `src/confradar/dagster/definitions.py`
4. Add parameter to `store_conferences` in `src/confradar/dagster/assets/storage.py`
5. Add test to verify asset exists

See [Dagster Orchestration](Dagster-Orchestration) for detailed guide.

### Materializing assets

```powershell
cd packages/confradar

# Materialize all
uv run dagster asset materialize --select '*'

# Materialize specific asset
uv run dagster asset materialize --select 'ai_deadlines_conferences'
```