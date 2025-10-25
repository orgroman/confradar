# ConfRadar Wiki

Welcome to the **ConfRadar** documentation wiki! ConfRadar is an intelligent agent that automatically tracks academic conference deadlines by crawling CFP pages, extracting key dates with LLMs, detecting changes over time, and syncing to Notion or Google Docs.

## Quick Links

- [Project Overview](Overview)
- [Architecture](Architecture)
- [Getting Started](Getting-Started)
- [Development Guide](Development-Guide)
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
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Web       │────▶│  LLM Agent   │────▶│  Knowledge  │
│   Sources   │     │  (LangChain) │     │    Base     │
└─────────────┘     └──────────────┘     └─────────────┘
                            │                     │
                            │                     │
                            ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │  Clustering  │     │   Change    │
                    │   & Aliases  │     │  Detection  │
                    └──────────────┘     └─────────────┘
                            │                     │
                            └──────────┬──────────┘
                                       │
                                       ▼
                            ┌──────────────────┐
                            │  Serving Layer   │
                            │  (Notion/Docs)   │
                            └──────────────────┘
```

## Project Status

**Current Phase**: Requirements & Design (M1)

- Issues: 61 items across milestones M1–M7
- Status: All items set to "Todo" and assigned to @orgroman

See the [Roadmap](Roadmap) for detailed milestones and the [GitHub Project](https://github.com/users/orgroman/projects/6) for active tasks.

## Quick Start

Setup and environment instructions will be documented as implementation progresses. For immediate context, see the repository [`README`](https://github.com/orgroman/confradar#readme) and the planning docs linked above.

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
