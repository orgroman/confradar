# ConfRadar - Complete PRD Gap Analysis

**Date:** 2025-01-23  
**Analyzed Documents:**
- `docs/confradar_prd.md` (Complete PRD)
- `docs/confradar_implementation_plan.md` (Detailed Implementation Plan)
- `docs/ConfRadar.md` (Original specification)
- `backlog.csv` (38 existing issues)

## Executive Summary

After analyzing the **complete PRD** and **implementation plan**, I've identified **23 additional gaps** in the current backlog. The previous gap analysis (based only on `ConfRadar.md`) missed critical Python-specific requirements, detailed data source integrations, and specific milestone deliverables outlined in the full PRD.

### Key Findings:
- ✅ **Strong Coverage:** Infrastructure, orchestration, DevOps basics (38 existing issues)
- ⚠️ **Gaps Identified:** Python tooling, specific data source scrapers, PDF handling, detailed evaluation tasks
- 📊 **New Total:** 38 existing + 23 new = **61 total issues**

---

## Gap Analysis by Category

### 1. Python Project Setup & Tooling (7 gaps)

The PRD explicitly states "the project should be python based" with specific tech stack recommendations. Current backlog has generic "Dev workflow and CI basics" but lacks Python-specific issues.

#### Missing Issues:

1. **Python project structure and pyproject.toml**
   - **PRD Reference:** Technical Stack - "Python is recommended as the primary language"
   - **Current Coverage:** None
   - **Description:** Set up standard Python project structure with src/ layout, pyproject.toml for dependencies (Poetry or setuptools), requirements.txt, setup.py. Configure package metadata.
   - **Labels:** `type:task;area:infra;priority:P0`
   - **Milestone:** M1: Requirements & Design

2. **Python environment management (venv/conda)**
   - **PRD Reference:** Technical Stack - Python ecosystem
   - **Current Coverage:** None
   - **Description:** Document virtual environment setup. Provide scripts for creating/activating venv. Consider conda for data science dependencies. Add .python-version file.
   - **Labels:** `type:task;area:infra;priority:P1`
   - **Milestone:** M1: Requirements & Design

3. **Python code formatting (Black/Ruff)**
   - **PRD Reference:** Non-Functional Requirements - Maintainability
   - **Current Coverage:** Generic "lint/format" in issue #16
   - **Description:** Configure Black for code formatting (100 char line length). Add Ruff for fast linting. Configure in pyproject.toml. Add format/lint commands.
   - **Labels:** `type:task;area:infra;priority:P1`
   - **Milestone:** M1: Requirements & Design

4. **Type checking with mypy**
   - **PRD Reference:** Non-Functional Requirements - Maintainability (code quality)
   - **Current Coverage:** None
   - **Description:** Set up mypy for static type checking. Add type hints to critical modules (extraction, clustering). Configure mypy.ini with strict settings.
   - **Labels:** `type:task;area:infra;priority:P2`
   - **Milestone:** M1: Requirements & Design

5. **Pre-commit hooks for Python**
   - **PRD Reference:** Non-Functional Requirements - Maintainability
   - **Current Coverage:** Mentioned in issue #16 but not Python-specific
   - **Description:** Configure pre-commit with Python hooks: black, ruff, mypy, trailing-whitespace, end-of-file-fixer. Add .pre-commit-config.yaml.
   - **Labels:** `type:task;area:infra;priority:P1`
   - **Milestone:** M1: Requirements & Design

6. **Python dependency management strategy**
   - **PRD Reference:** Technical Stack - Python libraries
   - **Current Coverage:** None
   - **Description:** Choose between Poetry, pip-tools, or plain requirements.txt. Document dependency update process. Set up Dependabot for security updates.
   - **Labels:** `type:task;area:infra;priority:P1`
   - **Milestone:** M1: Requirements & Design

7. **Pytest configuration and fixtures**
   - **PRD Reference:** Technical Stack - Testing Tools, Implementation Plan M1
   - **Current Coverage:** Generic "unit test suite" in issue #32
   - **Description:** Configure pytest with pytest.ini/pyproject.toml. Set up conftest.py with shared fixtures (mock conferences, DB session). Add pytest-cov for coverage reporting. Configure coverage thresholds.
   - **Labels:** `type:task;area:infra;priority:P1`
   - **Milestone:** M1: Requirements & Design

---

### 2. Specific Data Source Integrations (5 gaps)

The Implementation Plan details specific scrapers for known sources (M2-3). Current backlog only has generic "Seeded crawling" (#1).

#### Missing Issues:

8. **Scraper: AI Deadlines (aideadlin.es)**
   - **PRD Reference:** Implementation Plan M2-3 - "Develop scraper for AI Deadlines aggregator"
   - **Current Coverage:** None (generic crawling only)
   - **Description:** Implement dedicated scraper for Papers With Code's AI Deadlines site. Parse conference list, extract names, dates, links. Handle pagination/filtering.
   - **Labels:** `type:feature;area:retrieval;priority:P0`
   - **Milestone:** M2: Data Source Integration & Web Crawling

9. **Scraper: ACL Sponsored Events**
   - **PRD Reference:** Implementation Plan M2-3 - "Develop scraper for ACL Sponsored Events listing"
   - **Current Coverage:** None
   - **Description:** Parse ACL events page (https://www.aclweb.org/portal/upcoming). Extract event name, date, location, link for each ACL-sponsored conference/workshop.
   - **Labels:** `type:feature;area:retrieval;priority:P1`
   - **Milestone:** M2: Data Source Integration & Web Crawling

10. **Scraper: ChairingTool platform**
    - **PRD Reference:** Implementation Plan M2-3 - "Develop scraper or integration for ChairingTool platform conferences"
    - **Current Coverage:** None
    - **Description:** Retrieve conference info from ChairingTool (API if available, or scrape). Extract deadlines, dates. Handle authentication if needed.
    - **Labels:** `type:feature;area:retrieval;priority:P1`
    - **Milestone:** M2: Data Source Integration & Web Crawling

11. **Scraper: ELRA conference listings (LREC)**
    - **PRD Reference:** Implementation Plan M2-3 - "Develop scraper for ELRA conference listings"
    - **Current Coverage:** None
    - **Description:** Parse ELRA website for upcoming conferences like LREC. Extract conference dates and submission deadlines.
    - **Labels:** `type:feature;area:retrieval;priority:P2`
    - **Milestone:** M2: Data Source Integration & Web Crawling

12. **Scraper: WikiCFP integration**
    - **PRD Reference:** PRD - Open Questions "Should we integrate directly with WikiCFP's data?"
    - **Current Coverage:** None
    - **Description:** Implement WikiCFP scraper as fallback source. Parse CFP listings, extract categories, deadlines. Handle WikiCFP's HTML structure changes gracefully.
    - **Labels:** `type:feature;area:retrieval;priority:P2`
    - **Milestone:** M2: Data Source Integration & Web Crawling

---

### 3. PDF Handling (2 gaps)

PRD explicitly mentions PDF CFPs as a data source challenge. Current backlog doesn't address PDF parsing.

#### Missing Issues:

13. **PDF text extraction pipeline**
    - **PRD Reference:** PRD - Open Questions "PDF Handling", Technical Stack
    - **Current Coverage:** None
    - **Description:** Integrate PDF parsing library (PyMuPDF or pdfplumber). Extract text from PDF CFPs. Handle multi-column layouts and table extraction.
    - **Labels:** `type:feature;area:extraction;priority:P2`
    - **Milestone:** M3: Information Extraction Pipeline

14. **PDF download and caching**
    - **PRD Reference:** PRD - System Architecture "Retrieved content (HTML or PDF)"
    - **Current Coverage:** None
    - **Description:** Download PDF CFPs when HTML not available. Cache PDFs locally/S3 to avoid re-downloading. Track PDF URLs in database.
    - **Labels:** `type:feature;area:retrieval;priority:P2`
    - **Milestone:** M2: Data Source Integration & Web Crawling

---

### 4. LLM Integration Details (3 gaps)

PRD details LLM usage extensively (LangChain, OpenAI/Anthropic). Current backlog has generic "LLM fallback" (#5) but lacks setup/configuration issues.

#### Missing Issues:

15. **LLM API setup and configuration**
    - **PRD Reference:** PRD - Technical Stack "OpenAI API (GPT-4 or GPT-3.5)", Open Questions "LLM Choice"
    - **Current Coverage:** None
    - **Description:** Set up OpenAI/Anthropic API clients. Configure API keys via secrets management. Implement rate limiting and error handling for API calls. Add cost tracking.
    - **Labels:** `type:task;area:extraction;priority:P0`
    - **Milestone:** M1: Requirements & Design

16. **LangChain agent framework setup**
    - **PRD Reference:** PRD - Technical Stack "LangChain framework is a strong candidate"
    - **Current Coverage:** None
    - **Description:** Install and configure LangChain. Set up agent with tools (search, extraction). Implement agent memory/state management. Test basic agent workflow.
    - **Labels:** `type:feature;area:extraction;priority:P1`
    - **Milestone:** M3: Information Extraction Pipeline

17. **Extraction prompt engineering and optimization**
    - **PRD Reference:** PRD - Open Questions "define the prompting strategy", Implementation Plan M3-4
    - **Current Coverage:** Partial (mentioned in issue #5)
    - **Description:** Design and test prompts for conference field extraction. Include few-shot examples. Iterate on prompt templates. A/B test prompt variations for accuracy.
    - **Labels:** `type:task;area:extraction;priority:P1`
    - **Milestone:** M3: Information Extraction Pipeline

---

### 5. Evaluation & Metrics (3 gaps)

Implementation Plan M6 details specific evaluation tasks. Current backlog has generic "Evaluation harness" (#14) but lacks detailed sub-tasks.

#### Missing Issues:

18. **Ground truth dataset curation**
    - **PRD Reference:** Implementation Plan M6 - "Define a test set of conferences (e.g., 10 upcoming events with known ground-truth data)"
    - **Current Coverage:** None
    - **Description:** Manually curate ground truth dataset of 10-20 conferences with verified data (official deadlines, locations, dates). Document sources. Use for evaluation baseline.
    - **Labels:** `type:task;area:infra;priority:P1`
    - **Milestone:** M6: Evaluation & Iteration

19. **Extraction accuracy metrics (Precision/Recall)**
    - **PRD Reference:** PRD - Non-Functional Requirements ">90% of important dates correctly extracted", Implementation Plan M3-4
    - **Current Coverage:** Partial (mentioned in issue #14)
    - **Description:** Implement field-level precision/recall calculation. Compare extracted vs ground truth for: deadlines, locations, dates. Generate accuracy report per field.
    - **Labels:** `type:task;area:infra;priority:P1`
    - **Milestone:** M6: Evaluation & Iteration

20. **Change detection latency tracking**
    - **PRD Reference:** PRD - Non-Functional Requirements "detect and reflect change within at most 24 hours"
    - **Current Coverage:** None
    - **Description:** Track time between official deadline change and ConfRadar detection. Measure change propagation to output. Set alerting threshold for stale data.
    - **Labels:** `type:task;area:infra;priority:P2`
    - **Milestone:** M6: Evaluation & Iteration

---

### 6. Database & Schema Details (2 gaps)

Implementation Plan specifies schema details and versioning. Current backlog has generic issues but lacks specifics.

#### Missing Issues:

21. **PostgreSQL schema design documentation**
    - **PRD Reference:** PRD - Technical Stack "PostgreSQL or MySQL database", Data Schema in Assumptions
    - **Current Coverage:** Generic "Define ConfRadar event schema" (#3)
    - **Description:** Document detailed PostgreSQL schema: ConferenceSeries table, ConferenceEvent table, ChangeLog table. Define indexes, foreign keys, constraints. Add ER diagram.
    - **Labels:** `type:docs;area:kb;priority:P1`
    - **Milestone:** M1: Requirements & Design

22. **SQLAlchemy ORM models**
    - **PRD Reference:** PRD - Technical Stack "object-relational mapper (ORM) like SQLAlchemy"
    - **Current Coverage:** None
    - **Description:** Implement SQLAlchemy models for ConferenceSeries, ConferenceEvent. Add relationships, cascade deletes. Create DB session management utilities.
    - **Labels:** `type:task;area:kb;priority:P0`
    - **Milestone:** M2: Data Source Integration & Web Crawling

---

### 7. Web Scraping Details (1 gap)

PRD mentions specific libraries and techniques. Current backlog lacks implementation details.

#### Missing Issues:

23. **BeautifulSoup/Scrapy implementation**
    - **PRD Reference:** PRD - Technical Stack "BeautifulSoup for parsing HTML", "Scrapy for complex crawling"
    - **Current Coverage:** Generic crawling in issue #1
    - **Description:** Implement HTML parsers using BeautifulSoup. Consider Scrapy framework for queue management if needed. Add CSS selector tests for brittle page structures.
    - **Labels:** `type:task;area:retrieval;priority:P1`
    - **Milestone:** M2: Data Source Integration & Web Crawling

---

## Summary of New Issues

| Category | Count | Priority Breakdown |
|----------|-------|-------------------|
| Python Tooling | 7 | P0: 1, P1: 5, P2: 1 |
| Data Source Scrapers | 5 | P0: 1, P1: 2, P2: 2 |
| PDF Handling | 2 | P2: 2 |
| LLM Integration | 3 | P0: 1, P1: 2 |
| Evaluation | 3 | P1: 2, P2: 1 |
| Database | 2 | P0: 1, P1: 1 |
| Web Scraping | 1 | P1: 1 |
| **TOTAL** | **23** | **P0: 3, P1: 13, P2: 7** |

---

## Updated Issue Count

- **Previous (first gap analysis):** 17 → 38 issues
- **Current (complete PRD):** 38 → **61 issues**
- **Total new issues from complete PRD:** 23

---

## Priority Recommendations

### Critical Path (Must Have for MVP):

1. **P0 Issues (3):** Python project structure (#39), SQLAlchemy ORM (#60), LLM API setup (#53), AI Deadlines scraper (#46)
2. **High Priority (13 P1 issues):** Python tooling, specific scrapers, evaluation tasks

### Can Defer to Post-MVP:

- Conference ranking/tier data (#57)
- Manual review UI (#55)
- Advanced PDF parsing (#51-52)
- Some P3 features (API auth #31, calendar export #15)

---

## Implementation Notes

### Python-First Approach

Since the PRD explicitly mandates Python, the first sprint should:
1. Set up Python project structure (#39)
2. Configure tooling: Black, Ruff, mypy, pytest (#41-45, #47)
3. Set up SQLAlchemy models (#60)
4. Configure LLM APIs (#53)

### Data Source Priority

The Implementation Plan suggests starting with:
1. AI Deadlines (#46) - easiest, structured data
2. ACL Events (#47) - official list, reliable
3. ChairingTool (#48) - moderate complexity
4. ELRA (#49), WikiCFP (#50) - nice-to-have

### Milestone Alignment

New issues align with existing milestone structure:
- **M1:** Python tooling, docs, LLM setup (Issues #39-45, #53, #59)
- **M2:** Specific scrapers, PDF handling, ORM (Issues #46-50, #52, #60, #61)
- **M3:** Extraction pipeline, prompts, PDF parsing (Issues #51, #54, #55)
- **M6:** Evaluation tasks (Issues #56-58)

---

## Next Steps

1. **Create 23 new issues** from this analysis
2. **Update backlog.csv** to 61 total issues
3. **Run bootstrap script** to create GitHub issues #39-#61
4. **Add issues to Project #6**
5. **Update PRD_GAP_ANALYSIS.md** to reference complete analysis

---

## Appendix: PRD Coverage Map

### Well Covered:
- ✅ Orchestration (Airflow/Dagster)
- ✅ Monitoring and alerting
- ✅ Containerization and deployment
- ✅ Testing infrastructure
- ✅ API development
- ✅ Change detection
- ✅ Clustering and alias resolution

### Gaps Addressed by New Issues:
- ⚠️ Python-specific tooling → Issues #39-#45, #47
- ⚠️ Specific data sources → Issues #46-50
- ⚠️ PDF handling → Issues #51-52
- ⚠️ LLM integration details → Issues #53-55
- ⚠️ Evaluation details → Issues #56-58
- ⚠️ Database specifics → Issues #59-60
- ⚠️ Scraping implementation → Issue #61

### Still Out of Scope (Post-MVP):
- Full web UI with authentication
- Personalized recommendations
- Multi-language support
- Email list parsing
- Advanced analytics

---

**Analysis completed:** 2025-01-23  
**Analyst:** GitHub Copilot  
**Status:** Ready for issue creation
