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

# Create venv and install deps (project + dev group)
uv sync --all-groups

# Run tests
uv run pytest

# Run CLI (examples)
uv run confradar parse --text "Submission: Nov 15, 2025 (AoE)"
uv run confradar fetch https://www.example.org/cfp
```

Notes:
- Monorepo structure will evolve (apps/, packages/, infra/). Current library lives under `src/confradar/` with tests in `tests/`.
- See P0/P1 issues for initial setup: project structure, SQLAlchemy ORM, LLM API config.
- Orchestration will use Airflow/Dagster; Docker and IaC tracked in infra issues.

Repo scripts and ops:

- Bootstrap GitHub artifacts: [`scripts/bootstrap_github.ps1`](scripts/bootstrap_github.ps1)
- Update milestones in bulk: [`scripts/update_milestones.ps1`](scripts/update_milestones.ps1)

## Contributing

Please file issues on the Project Board and use the label taxonomy (type:*, area:*, priority:Px).

## Acknowledgements

This project aggregates public conference information; please respect robots.txt and source terms. PRs welcome for new sources and extraction rules.
