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

All pull requests must pass:
- **Tests**: All unit tests must pass (Ubuntu CI)
- **Coverage**: Minimum 45% code coverage required
  - Current baseline: ~48%
  - Orange zone: 45-60% (warning)
  - Green zone: 60%+ (good)

Note: Integration tests (#83) and database tests (#84) are currently skipped in CI due to known issues.

## Docs and Wiki

- Edit docs under `docs/wiki/` in the main repo. They auto-sync to the GitHub Wiki on push to `main`.
- Home page is `docs/wiki/Home.md`.

## PRs

- Keep changes focused and covered by tests when public behavior changes.
- Update docs when you add features or change UX/APIs.
