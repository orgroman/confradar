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