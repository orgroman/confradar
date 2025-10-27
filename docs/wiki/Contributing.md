# Contributing

Thanks for your interest in improving ConfRadar!

- Issues: https://github.com/orgroman/confradar/issues
- Project board: https://github.com/users/orgroman/projects/6
- Roadmap: https://github.com/orgroman/confradar/blob/main/ROADMAP.md

## Dev setup

```powershell
iwr -useb https://astral.sh/uv/install.ps1 | iex
uv sync --extra dev
cd packages/confradar
uv run pytest -q
```

## CI Requirements

All pull requests are checked by multiple CI workflows:

### Required Checks (Must Pass)
- **Tests**: All unit tests must pass (Ubuntu CI)
- **Coverage**: Minimum 55% code coverage required (raised from 45% after #84 and #86)
  - Current baseline: 57%
  - Orange zone: 55-60% (warning)
  - Green zone: 60%+ (good)
- **Ruff**: Code linting must pass (no deprecated types, proper imports, no unused vars)
- **Black**: Code formatting must pass (all files properly formatted)

### Quality Checks (Reporting Mode)
The following checks currently run in reporting mode (won't block PRs):
- **Mypy**: Static type checking (will be enforced after type coverage improves)
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checks
- **detect-secrets**: Secret scanning

### Dependency Review (Enforced)
- **Dependency Review**: Fails if new dependencies have moderate+ severity vulnerabilities
- Only runs when `pyproject.toml` or `uv.lock` are modified

### Local Pre-commit Checks

Before submitting a PR, run:
```powershell
cd packages/confradar

# Run tests with coverage
uv run pytest --cov=src/confradar --cov-report=term-missing

# Check code quality
uv run ruff check src tests
uv run black --check src tests
uv run mypy src --ignore-missing-imports
```

Note: Integration tests (#83) are skipped in CI due to Scrapy reactor limitations and network dependencies. Database tests now run with PostgreSQL service (#84 resolved).

## Docs and Wiki

- Edit docs under `docs/wiki/` in the main repo. They auto-sync to the GitHub Wiki on push to `main`.
- Home page is `docs/wiki/Home.md`.

## PRs

- Keep changes focused and covered by tests when public behavior changes.
- Update docs when you add features or change UX/APIs.
