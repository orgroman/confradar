# Development Guide

This guide covers development workflows for the ConfRadar monorepo with uv and the LiteLLM proxy.

## Environment

- Python: 3.10+
- Dependency manager: uv
- Database: PostgreSQL (Docker) or SQLite (tests only)
- Package: `packages/confradar`

```powershell
uv sync --extra dev
cd packages/confradar
uv run pytest -q
```

## Database Development

### Connection Strings

Production (default):
```powershell
DATABASE_URL=postgresql+psycopg://confradar:confradar@localhost:5432/confradar
```

Testing (SQLite):
```powershell
$env:DATABASE_URL = "sqlite:///test.db"
```

Docker internal (for containers):
```powershell
DATABASE_URL=postgresql+psycopg://confradar:confradar@postgres:5432/confradar
```

### Working with PostgreSQL

```powershell
# Start PostgreSQL
docker compose up -d postgres

# Connect via psql
docker compose exec postgres psql -U confradar -d confradar

# Common queries
docker compose exec postgres psql -U confradar -d confradar -c "\dt"  # List tables
docker compose exec postgres psql -U confradar -d confradar -c "\d conferences"  # Describe table
docker compose exec postgres psql -U confradar -d confradar -c "SELECT COUNT(*) FROM conferences;"
```

### Backup and Restore

```powershell
# Backup database
docker compose exec postgres pg_dump -U confradar confradar > backup.sql

# Restore database
docker compose exec -T postgres psql -U confradar -d confradar < backup.sql
```

## LLM configuration

- API key: `CONFRADAR_SA_OPENAI` (preferred) or `OPENAI_API_KEY`
- Base URL (OpenAI-compatible): defaults to `http://localhost:4000`
- Override via: `LITELLM_BASE_URL`, `LLM_BASE_URL`, or `OPENAI_BASE_URL`
- Local proxy: `docker compose up -d` (from repo root)

## Coding standards

- Format: black
- Lint: ruff
- Type check: mypy
- Tests: pytest (+ pytest-cov)

```powershell
cd packages/confradar

# Lint code
uv run ruff check src tests

# Auto-fix linting issues
uv run ruff check --fix src tests

# Check formatting
uv run black --check src tests

# Auto-format code
uv run black src tests

# Type checking
uv run mypy src --ignore-missing-imports

# Run tests
uv run pytest -q
```

### Code Quality Status

Current known issues (tracked in #86):
- 99 ruff linting errors (mostly deprecated type hints)
- 17 files need black formatting
- Some mypy type hints can be improved

These will be systematically fixed, after which the code quality CI checks will be made mandatory.

## CI/CD

### Main CI (Tests)
- **Triggers**: Push to main, PRs to main
- **Runs on**: Ubuntu (Python 3.11)
- **Tests**: All unit tests (skips integration + database tests)
- **Required**: Must pass for PR merge

### Coverage CI
- **Triggers**: PRs to main
- **Minimum coverage**: 45% (fails below)
- **Thresholds**:
  - 🟢 Green: 60%+
  - 🟡 Orange: 45-60%
  - 🔴 Red: <45%
- **Reports**: HTML coverage report available as downloadable artifact

### Code Quality CI
- **Triggers**: PRs to main
- **Checks**:
  - **Ruff**: Linting (import order, deprecated types, unused imports, etc.)
  - **Black**: Code formatting verification
  - **Mypy**: Static type checking
- **Status**: Currently in reporting mode (`continue-on-error: true`)
- **Note**: All checks will be made mandatory after #86 (code quality improvements) is merged

### Security CI
- **Triggers**: PRs to main + weekly schedule (Sundays)
- **Checks**:
  - **Bandit**: Security vulnerability scanning in code
  - **Safety**: Dependency vulnerability checks
  - **detect-secrets**: Secret scanning to prevent credential leaks
- **Status**: Reporting mode (won't fail PRs, provides visibility)

### Dependency Review CI
- **Triggers**: PRs that modify `pyproject.toml` or `uv.lock`
- **Action**: Reviews dependency changes for known vulnerabilities
- **Behavior**: Fails on moderate+ severity vulnerabilities
- **Status**: Active and enforced

### Running tests locally

```powershell
cd packages/confradar

# Quick test run
uv run pytest -q

# With coverage
uv run pytest --cov=src/confradar --cov-report=term-missing

# Specific test file
uv run pytest tests/test_acl_web_scraper.py -v

# Skip slow tests
uv run pytest --ignore=tests/test_integration_scrapers.py
```

### Known CI Issues
- **#83**: Integration tests fail due to Scrapy reactor issue (skipped in CI)
- **#84**: Database tests need PostgreSQL service (skipped in CI)
- **#86**: Code quality improvements needed (ruff/black/mypy issues)

Once #84 is resolved, coverage threshold can be raised to 50%+.
Once #86 is resolved, code quality checks will become mandatory.

## Branch Protection

Main branch is protected:
- ✅ Requires "Tests (uv) (3.11)" check to pass
- ✅ Cannot merge PRs with failing tests
- ✅ Ensures code quality and prevents regressions

## Notes

- Keep public APIs stable; add tests when changing behavior
- Prefer provider-agnostic LLM usage via LiteLLM (client or proxy)
- No real LLM calls in unit tests; mock LiteLLM

## Database migrations (Alembic)

We use Alembic for schema migrations. Migrations run against PostgreSQL by default.

```powershell
# Generate a new migration (autogenerate from models)
uv run alembic revision --autogenerate -m "<message>"

# Apply migrations
uv run alembic upgrade head

# Downgrade one revision
uv run alembic downgrade -1

# View migration history
uv run alembic history

# Test migration with SQLite
$env:DATABASE_URL = "sqlite:///test.db"
uv run alembic upgrade head
```

### Migration Best Practices

- Always review autogenerated migrations before committing
- Test migrations on a copy of production data when possible
- Keep migrations small and focused
- Include both upgrade and downgrade logic
- Never edit applied migrations (create new ones instead)

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