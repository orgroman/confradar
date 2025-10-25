# ConfRadar Wiki

Welcome to the **ConfRadar** documentation wiki! ConfRadar is an intelligent agent that automatically tracks academic conference deadlines by crawling CFP pages, extracting key dates with LLMs, detecting changes over time, and syncing to Notion or Google Docs.

## Quick Links

- [Project Overview](Overview)
- [Architecture](Architecture)
- [Getting Started](Getting-Started)
- [Development Guide](Development-Guide)
- [Scraper Development](Scraper-Development)
- [Dagster Orchestration](Dagster-Orchestration.md)
- [Data Schema](Data-Schema)
- [Roadmap](Roadmap)
- [Contributing](Contributing)

### Project Management

- Project Board: https://github.com/users/orgroman/projects/6
- Backlog (CSV): https://github.com/orgroman/confradar/blob/main/backlog.csv
- Project Views setup: https://github.com/orgroman/confradar/blob/main/docs/PROJECT_VIEWS_SETUP.md
- Project Views quick ref: https://github.com/orgroman/confradar/blob/main/docs/PROJECT_VIEWS_QUICK_REF.md
- Custom fields (Start/Target Date, etc.): https://github.com/orgroman/confradar/blob/main/docs/CUSTOM_FIELDS_SETUP.md
- Project automations: https://github.com/orgroman/confradar/blob/main/docs/PROJECT_AUTOMATIONS.md

### Primary Docs

- Roadmap document: https://github.com/orgroman/confradar/blob/main/ROADMAP.md
- Quarterly plan (2025 Q4): https://github.com/orgroman/confradar/blob/main/docs/roadmap/2025Q4.md
- Product Requirements (PRD): https://github.com/orgroman/confradar/blob/main/docs/confradar_prd.md
- Implementation Plan: https://github.com/orgroman/confradar/blob/main/docs/confradar_implementation_plan.md
- Gap Analysis (complete): https://github.com/orgroman/confradar/blob/main/docs/PRD_GAP_ANALYSIS_COMPLETE.md
- Gap Analysis summary: https://github.com/orgroman/confradar/blob/main/docs/COMPLETE_GAP_ANALYSIS_SUMMARY.md

## What is ConfRadar?

ConfRadar solves a common problem for researchers: **staying on top of academic conference deadlines**. Conference information is scattered across countless websites, mailing lists, and portals, making it time-consuming to manually monitor. Deadlines frequently change (extensions, venue updates), and missing one can mean lost opportunities.

### Key Features

- **🔍 Automated Discovery**: Crawls conference websites and CFP aggregators
- **🤖 LLM-Powered Extraction**: Uses NLP to extract dates, venues, and details
- **📊 Change Detection**: Monitors and alerts when deadlines are extended or updated
- **🔗 Alias Resolution**: Recognizes that "NeurIPS" and "NIPS" are the same conference
- **🎯 Workshop Clustering**: Links workshops to their parent conferences
- **📝 Smart Sync**: Updates your Notion database or Google Doc automatically
- **📅 Calendar Export**: Generates .ics files for your calendar app

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Dagster Orchestration                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Scrapers   │→ │   Storage    │→ │  Extraction  │→  ...    │
│  │   (Assets)   │  │   (Assets)   │  │   (Assets)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         Daily Schedule (2 AM)  •  Web UI  •  Monitoring         │
└─────────────────────────────────────────────────────────────────┘
           ↓                    ↓                    ↓
    ┌──────────┐         ┌──────────┐        ┌──────────┐
    │   Web    │         │ Database │        │   LLM    │
    │ Sources  │         │ (SQLite) │        │  (API)   │
    └──────────┘         └──────────┘        └──────────┘
```

## Project Status

**Current Phase**: M2 - Data Source Integration & Web Crawling

**Recently Completed**:
- ✅ Scrapy framework with 5 production spiders (AI Deadlines, ACL Web, Chairing Tool, ELRA, WikiCFP)
- ✅ Dagster orchestration pipeline with daily scheduling
- ✅ Database models with SQLAlchemy and Alembic migrations
- ✅ Docker Compose setup with LiteLLM proxy and Dagster services

**Active Development**:
- M3: LLM-based information extraction
- Data quality checks and monitoring
- Notion/Google Docs integration planning

See the [Roadmap](Roadmap) for detailed milestones and the [GitHub Project](https://github.com/users/orgroman/projects/6) for active tasks.

## Quick Start

On Windows PowerShell using uv:

```powershell
# Install uv (one-time)
iwr -useb https://astral.sh/uv/install.ps1 | iex

# Install deps (project + dev extras)
uv sync --extra dev

# Run tests (from package directory)
cd packages/confradar
uv run pytest -q
cd ../..

# Try the CLI
uv run confradar parse --text "Submission: Nov 15, 2025 (AoE)"
```

### LiteLLM proxy (recommended)

Run a local LiteLLM proxy so ConfRadar talks to an OpenAI-compatible endpoint without vendor lock-in.

```powershell
# Set your key
$env:CONFRADAR_SA_OPENAI = "<your-openai-key>"

# Start proxy from repo root (http://localhost:4000)
docker compose up -d

# Optional: override base URL
$env:LITELLM_BASE_URL = "http://localhost:4000"  # default
```

See the repository [`README`](https://github.com/orgroman/confradar#readme) for more details.

## Documentation Structure

- **[Overview](Overview)** - High-level concepts and motivation
- **[Architecture](Architecture)** - System design and components
- **[Data Schema](Data-Schema)** - Conference event data structure
- **[Retrieval](Retrieval)** - Web crawling and discovery
- **[Extraction](Extraction)** - NLP and LLM-based parsing
- **[Clustering](Clustering)** - Alias resolution and grouping
- **[Serving](Serving)** - Integration with Notion, Docs, and calendars
- **[Evaluation](Evaluation)** - Metrics and testing approach
- **[Development Guide](Development-Guide)** - Contributing and workflow

## Contact & Contributions

- **Repository**: [orgroman/confradar](https://github.com/orgroman/confradar)
- **Issues**: [GitHub Issues](https://github.com/orgroman/confradar/issues)
- **Discussions**: [GitHub Discussions](https://github.com/orgroman/confradar/discussions)

For contribution guidelines, see [Contributing](Contributing).
