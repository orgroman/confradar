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

### Required Checks
- **Tests**: All unit tests must pass (Ubuntu CI)
- **Coverage**: Minimum 45% code coverage required
  - Current baseline: ~48%
  - Orange zone: 45-60% (warning)
  - Green zone: 60%+ (good)

### Quality Checks (Reporting Mode)
The following checks currently run in reporting mode (won't block PRs):
- **Ruff**: Code linting (import order, deprecated types, unused imports)
- **Black**: Code formatting verification
- **Mypy**: Static type checking
- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checks
- **detect-secrets**: Secret scanning

These will become mandatory after #86 (code quality improvements) is merged.

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

Note: Integration tests (#83) and database tests (#84) are currently skipped in CI due to known issues.

## Docs and Wiki

- Edit docs under `docs/wiki/` in the main repo. They auto-sync to the GitHub Wiki on push to `main`.
- Home page is `docs/wiki/Home.md`.

## PRs

- Keep changes focused and covered by tests when public behavior changes.
- Update docs when you add features or change UX/APIs.
