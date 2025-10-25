# Project Overview

## Introduction

Researchers and academics often struggle to keep track of rapidly approaching conference submission deadlines and details. Conference information (e.g., Call for Papers dates, venues, etc.) is spread across many websites, mailing lists, and portals, making it time-consuming to manually monitor.

Existing community-driven trackers (such as WikiCFP or field-specific deadline aggregators) cover only a small portion of events and are not always up-to-date. In fact, conference data is highly dynamic – dates and deadlines frequently change (extensions, venue updates, etc.).

**ConfRadar** addresses this need by leveraging an AI-driven agent to continuously gather conference information, extract key dates, detect changes over time, and present the latest data in a convenient format (e.g., Google Docs or Notion pages).

## The Problem

### Pain Points for Researchers

1. **Information Scatter**: Conference CFPs are published on:
   - Official conference websites (varying layouts)
   - Community sites like WikiCFP (incomplete coverage)
   - Mailing lists (hard to search)
   - Social media (ephemeral)
   - Association portals (ACM, IEEE, etc.)

2. **Frequent Changes**: Deadlines are extended, venues change, or events are moved online with little notice

3. **Duplicate Tracking**: Same conference appears under multiple names (e.g., "NeurIPS" vs "NIPS" vs "Conference on Neural Information Processing Systems")

4. **Workshop Discovery**: Workshop CFPs are often separate from main conference announcements

5. **Manual Maintenance**: Keeping a personal deadline tracker requires constant vigilance and manual updates

### Current Solutions (and their limitations)

- **WikiCFP**: Community-maintained but incomplete; relies on manual submissions
- **AI Deadlines**: Curated list for AI/ML conferences only; updated via pull requests
- **Personal spreadsheets**: Completely manual; out of date quickly
- **Email alerts**: Passive; requires someone to post updates

## The Solution: ConfRadar

ConfRadar automates the entire pipeline from discovery to presentation:

### 1. Automated Discovery
- Crawls known conference websites on a schedule
- Searches for new events using intelligent queries
- Follows links from community aggregators

### 2. Intelligent Extraction
- Uses LLMs to parse diverse page layouts
- Extracts structured data: deadlines, locations, dates
- Handles time zones and date format variations

### 3. Smart Organization
- Resolves aliases and duplicate entries
- Links workshops to parent conferences
- Clusters related events

### 4. Change Tracking
- Detects when deadlines are extended
- Highlights updates and modifications
- Maintains version history

### 5. Seamless Integration
- Syncs to Notion databases
- Updates Google Docs tables
- Exports to calendar formats (.ics)

## Core Contributions

1. **Automated Conference Tracking System**: An end-to-end system that automatically retrieves and aggregates conference information from disparate sources in real time

2. **NLP-Based Information Extraction**: Robust extraction pipelines using LLMs to parse unstructured CFP announcements into structured records

3. **Temporal Change Detection**: Mechanism for monitoring changes to conference data over time, highlighting updates to users

4. **Alias Resolution & Clustering**: Methods to automatically cluster and link related events (workshops to conferences, aliases to series)

5. **User-Friendly Integration**: Synchronization with collaborative platforms (Notion, Google Docs) that researchers use daily

## Use Cases

### For Individual Researchers
- Never miss a submission deadline
- Track conferences in your specific field
- Automatic calendar integration
- Historical view of deadline changes

### For Research Groups
- Shared Notion workspace with all relevant conferences
- Collaborative planning around deadlines
- Workshop discovery for accepted papers

### For Conference Organizers
- Monitor competing conference dates
- Track trends in deadline timing
- Analyze extension patterns

## Technology Stack

- **Agent Framework**: LangChain for orchestration
- **LLMs**: For parsing and extraction
- **Web Scraping**: BeautifulSoup, Playwright for dynamic pages
- **Knowledge Base**: Graph database or structured store
- **Integrations**: Notion API, Google Docs API
- **Scheduling**: Cron or cloud functions for periodic runs

## Project Timeline

**Duration**: 6-7 months (MSc project)

See the [Roadmap](Roadmap) page for detailed milestones.

## Project Management

- Project Board: https://github.com/users/orgroman/projects/6
- Backlog (CSV): https://github.com/orgroman/confradar/blob/main/backlog.csv
- Roadmap docs: https://github.com/orgroman/confradar/blob/main/ROADMAP.md · Quarterly: https://github.com/orgroman/confradar/blob/main/docs/roadmap/2025Q4.md
- PRD: https://github.com/orgroman/confradar/blob/main/docs/confradar_prd.md
- Implementation Plan: https://github.com/orgroman/confradar/blob/main/docs/confradar_implementation_plan.md
- Gap Analysis (complete): https://github.com/orgroman/confradar/blob/main/docs/PRD_GAP_ANALYSIS_COMPLETE.md
- Views & fields setup: https://github.com/orgroman/confradar/blob/main/docs/PROJECT_VIEWS_SETUP.md · https://github.com/orgroman/confradar/blob/main/docs/CUSTOM_FIELDS_SETUP.md

## Success Metrics

- **Coverage**: % of major conferences tracked (target: 90%+ of top-tier CS conferences)
- **Accuracy**: Precision/recall of extracted deadlines (target: >95%)
- **Freshness**: Time lag for detecting updates (target: <24 hours)
- **User Satisfaction**: Researchers report reduced time spent tracking deadlines

## Related Work

- **WikiCFP**: Manual conference listing
- **AI Deadlines**: GitHub-maintained deadline tracker
- **Conference Crawlers**: Academic papers on metadata extraction
- **Persistent Identifiers for Conferences**: Research on standardizing conference identifiers

## Next Steps

1. Review the [Architecture](Architecture) to understand the system design
2. Explore the [Data Schema](Data-Schema) for the conference data model
3. Check the [Roadmap](Roadmap) for current development status
4. See [Getting Started](Getting-Started) for setup instructions (coming soon)
