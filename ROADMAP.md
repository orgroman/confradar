# ConfRadar Roadmap

This roadmap turns the docs into actionable milestones and tracks near-term execution.

## Themes
- Retrieval and discovery (agent + crawling)
- NLP/LLM extraction to structured schema
- Change detection + versioned knowledge base
- Clustering (aliases, workshops → parent)
- Serving (Notion/Docs; optional calendar export)
- Evaluation and reliability

## Milestones

### M1: MVP core pipeline (Q4 2025)
- **Infrastructure:** Migrate from SQLite to PostgreSQL with Docker Compose support (P0)
- Retrieval: seeded crawling + basic search fallback
- Extraction: rule-first + LLM fallback to ConfRadar schema
- KB: store conference event records; last_updated
- Change detection: detect date diffs and mark updates

### M2: Clustering and alias resolution (Q4 2025)
- Alias unification for series and yearly events
- Workshop → parent event linkage by text/date/location cues

### M3: Serving and sync (Q4 2025)
- Notion database sync OR Google Doc table sync (choose one first)
- Basic formatting, sort by upcoming deadlines

### M4: Evaluation + refinements (Q1 2026)
- Metrics: precision/recall for extraction; freshness latency; clustering purity/ARI
- Improve prompts/rules to hit quality targets

### M5: Extras (Q1 2026)
- Calendar export (.ics)
- Scheduling + deployment (daily runs)

## Labels and workflow
- Backlog is curated via labels: area:*, type:*, priority:*.
- Issues are organized in GitHub Project: "ConfRadar Roadmap" with fields Status and Priority.

See `docs/roadmap/2025Q4.md` for the current quarter plan and backlog.
