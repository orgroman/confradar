# Roadmap

For the canonical roadmap and quarterly plan, see the repo documents:

- Main roadmap: https://github.com/orgroman/confradar/blob/main/ROADMAP.md
- Quarterly plan (2025 Q4): https://github.com/orgroman/confradar/blob/main/docs/roadmap/2025Q4.md

This Wiki mirrors highlights from the repo. Update the links above for the authoritative source.

## Current Focus (2025 Q4)

### Frontend Web Application (New Initiative - Oct 2025)

**Goal**: Build a modern web interface for browsing conference information.

**Timeline**: 5 milestones from Dec 2025 to Apr 2026

**Status**: Phase 1 (Infrastructure) in progress with GitHub Copilot coding agent

**Milestones**:
- **FE-1** (Dec 2025): Infrastructure & Setup - Framework, components, state, routing, build tools
- **FE-2** (Jan 2026): List View & Display - Conference cards, pagination, sorting
- **FE-3** (Jan 2026): Search & Filtering - Real-time search, date/location/field filters
- **FE-4** (Feb 2026): Detail View & Timezone - Detail pages, AoE toggle, timezone conversion
- **FE-5** (Mar-Apr 2026): Calendar Export & Settings - ICS export, user preferences

**Active Work**:
- 40 issues created across 9 epics (see [epic #86](https://github.com/orgroman/confradar/issues/86))
- 5 PRs in progress by Copilot: #127-#131 (infrastructure setup)
- Priorities: P0 (parent epic), P1 (infrastructure, core features), P2 (enhancements)

See [Frontend PRD](../confradar_web_prd.md) for complete specifications.

### Backend Data Pipeline (Ongoing)

**Status**: Core pipeline operational with 5 scrapers + Dagster orchestration

**Next Priorities**:
1. **P0**: PostgreSQL migration (move from SQLite to PostgreSQL for production)
2. **P1**: Expand test coverage to >80%
3. **P1**: Add pipeline monitoring and alerting
4. **M6**: Build REST API to serve frontend application

See [Backend Issues](https://github.com/orgroman/confradar/issues) for tracking.
