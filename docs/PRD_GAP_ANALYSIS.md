# PRD Coverage Analysis & Gap Remediation

**Date**: October 25, 2025  
**Status**: ✅ Complete

## Executive Summary

Conducted comprehensive gap analysis between the Product Requirements Document (PRD) in `docs/ConfRadar.md` and the GitHub project backlog. **Identified 21 critical missing issues** primarily in infrastructure, orchestration, and DevOps areas. All gaps have been addressed with new issues created and added to the project.

---

## Analysis Methodology

1. **Reviewed PRD documentation** (`ConfRadar.md`)
2. **Audited existing backlog** (17 initial issues)
3. **Cross-referenced with project milestones** (M1-M7)
4. **Identified feature/technical debt gaps**
5. **Created 21 additional issues** (total now: **38 issues**)

---

## Gap Analysis Results

### ✅ Well-Covered Areas (Original 17 Issues)

| Area | Issues | Status |
|------|--------|--------|
| Retrieval/Crawling | #1, #2 | ✅ Complete |
| NLP Extraction | #4, #5, #6 | ✅ Complete |
| Knowledge Base | #3, #7 | ✅ Complete |
| Clustering & Aliases | #9, #10, #11 | ✅ Complete |
| Change Detection | #8 | ✅ Complete |
| Serving (Notion/Docs) | #12, #13, #15 | ✅ Complete |
| Evaluation | #14 | ✅ Complete |
| Dev Basics | #16, #17 | ✅ Complete |

### ❌ Critical Gaps Identified (Now Addressed)

#### 1. **Orchestration & Pipeline Management** 🔴 Critical
**Gap**: PRD mentions "scheduling" and "agent runs periodically" but NO orchestration tooling specified.

**Remediation** (3 issues):
- #18: **Airflow/Dagster pipeline setup** (P0) → M2
- #19: **Pipeline monitoring and alerting** (P1) → M5  
- #21: **Retry logic and error handling** (P1) → M2

**Note**: User specified **Airflow or Dagster** for data orchestration - now formalized.

---

#### 2. **Data Quality & Validation** 🟠 High Priority
**Gap**: Extraction produces structured data but no validation layer.

**Remediation** (3 issues):
- #20: **Data quality validation** (P1) → M3
- #36: **Data deduplication beyond clustering** (P2) → M4
- #38: **Multi-source reconciliation** (P2) → M3

---

#### 3. **Infrastructure & DevOps** 🟠 High Priority
**Gap**: Deployment mentioned but infrastructure as code, secrets, containers not specified.

**Remediation** (6 issues):
- #22: **Database schema migrations** (P1) → M2
- #23: **Secrets management** (P1) → M1
- #27: **Containerization (Docker)** (P1) → M1
- #28: **Cloud deployment automation** (P1) → M7
- #24: **Logging infrastructure** (P1) → M5
- #26: **Error tracking (Sentry)** (P2) → M5

---

#### 4. **Observability & Monitoring** 🟡 Medium Priority
**Gap**: Evaluation metrics exist but no runtime monitoring/dashboards.

**Remediation** (2 issues):
- #25: **Metrics and observability** (P2) → M6
- #19: **Pipeline monitoring** (covered above)

---

#### 5. **Testing** 🟠 High Priority
**Gap**: PRD mentions "validation" but no test infrastructure.

**Remediation** (3 issues):
- #32: **Unit test suite** (P1) → M1
- #33: **Integration tests for pipelines** (P1) → M5
- #34: **Performance and load testing** (P2) → M6

---

#### 6. **API & Programmatic Access** 🟡 Medium Priority
**Gap**: Serving focuses on Notion/Docs but no API for programmatic access.

**Remediation** (2 issues):
- #29: **REST API for queries** (P2) → M7
- #30: **API authentication and rate limiting** (P3) → M7

---

#### 7. **User Engagement Features** 🟢 Nice-to-Have
**Gap**: PRD mentions notifications implicitly via "change detection" but not explicitly.

**Remediation** (2 issues):
- #31: **Email/Slack notifications** (P2) → M7
- #35: **Manual review UI/workflow** (P3) → M7

---

#### 8. **Enrichment Data** 🟢 Nice-to-Have
**Gap**: Conference tier/ranking not in schema but useful.

**Remediation** (1 issue):
- #37: **Conference ranking/tier data** (P3) → M2

---

## Updated Statistics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total Issues** | 17 | 38 | +21 (+123%) |
| **P0 Issues** | 0 | 1 | +1 |
| **P1 Issues** | 8 | 18 | +10 |
| **P2 Issues** | 8 | 15 | +7 |
| **P3 Issues** | 1 | 4 | +3 |

### Issues by Milestone

| Milestone | Before | After | Change |
|-----------|--------|-------|--------|
| M1: Requirements & Design | 3 | 6 | +3 |
| M2: Data Source Integration | 3 | 8 | +5 |
| M3: Information Extraction | 3 | 5 | +2 |
| M4: Clustering & Alias Resolution | 3 | 4 | +1 |
| M5: Agent Integration & Orchestration | 1 | 5 | +4 |
| M6: Evaluation & Iteration | 1 | 3 | +2 |
| M7: Deployment & User-Facing | 3 | 7 | +4 |

### Issues by Area

| Area | Count | % of Total |
|------|-------|------------|
| area:infra | 15 | 39% |
| area:kb | 6 | 16% |
| area:extraction | 5 | 13% |
| area:retrieval | 3 | 8% |
| area:serving | 5 | 13% |
| area:clustering | 4 | 11% |

**Key Insight**: Infrastructure now represents 39% of issues (was ~12%), reflecting production-readiness focus.

---

## Priority Distribution (Re-balanced)

```
P0 (Critical):     █ 3%
P1 (High):       ████████████████████ 47%
P2 (Medium):     ████████████████ 39%
P3 (Low):        ████ 11%
```

---

## Airflow/Dagster Integration Plan

Per user requirement: **"data orchestration, mining, transformations will be with Airflow or Dagster"**

### Recommended DAG Structure

#### **DAG 1: Daily Crawl & Extract**
```
seed_conferences → fetch_pages → extract_dates → store_events
     ↓
search_new_cfps → fetch_pages → extract_dates → store_events
```

#### **DAG 2: Weekly Clustering & Reconciliation**
```
compute_aliases → cluster_events → link_workshops → reconcile_conflicts
```

#### **DAG 3: Hourly Change Detection**
```
re_fetch_upcoming → compare_deltas → log_changes → trigger_notifications
```

#### **DAG 4: Daily Serving Sync**
```
query_updated_events → format_output → sync_notion → sync_docs → export_calendar
```

### Issue Mapping to DAGs

| Issue | DAG | Task |
|-------|-----|------|
| #18 | Setup | Define all 4 DAGs with schedules |
| #1, #2 | DAG 1 | Crawl tasks |
| #4, #5, #6 | DAG 1 | Extract tasks |
| #7, #22 | DAG 1 | Storage tasks |
| #9, #10, #11 | DAG 2 | Clustering tasks |
| #8 | DAG 3 | Change detection |
| #12, #13, #15 | DAG 4 | Serving sync |

---

## Key Architectural Decisions

### 1. Orchestration: Airflow vs Dagster

**Recommendation**: **Airflow** for initial MVP, **Dagster** for v2+

**Rationale**:
- Airflow: mature, widely adopted, cloud-managed (MWAA, Cloud Composer)
- Dagster: better for data quality, type-safe, modern UI, but less mature

### 2. Deployment Strategy

**Phases**:
1. **MVP (M1-M3)**: Local Airflow + Docker Compose
2. **Beta (M4-M6)**: AWS MWAA (Managed Workflows for Apache Airflow)
3. **Production (M7)**: MWAA + RDS + Lambda for API

### 3. Database Choice

**Recommendation**: **PostgreSQL 14+** with JSONB

**Rationale**:
- Mature, reliable, well-supported
- JSONB for flexible metadata (topics, tracks)
- Native full-text search for conference names
- Easy RDS deployment

---

## Risks & Mitigation

| Risk | Mitigation | Issue |
|------|------------|-------|
| Airflow learning curve | Start with simple DAGs, add complexity | #18 |
| Pipeline monitoring gaps | Implement early in M5 | #19, #25 |
| Data quality issues | Validate at every stage | #20 |
| Secret leaks | Never commit secrets; use managed services | #23 |
| Deployment complexity | Use IaC (Terraform); test in staging | #28 |

---

## Next Steps

### Immediate (Week 1-2)
1. ✅ **Complete gap analysis** ← Done
2. **Finalize Airflow vs Dagster choice** (#18)
3. **Set up Docker dev environment** (#27)
4. **Design database schema** (#3, #22)

### Short-Term (M1-M2)
1. **Implement seed crawler** (#1)
2. **Set up Airflow DAGs** (#18)
3. **Build extraction pipeline** (#4, #5)
4. **Add data validation** (#20)

### Medium-Term (M3-M5)
1. **Clustering implementation** (#9, #10, #11)
2. **Change detection** (#8)
3. **Pipeline monitoring** (#19, #25)
4. **Integration tests** (#33)

### Long-Term (M6-M7)
1. **Evaluation metrics** (#14, #34)
2. **Production deployment** (#28)
3. **API and notifications** (#29, #31)
4. **User-facing features** (#35)

---

## Resources & Dependencies

### External Services Required
- **OpenAI/Anthropic API** (LLM extraction) - $100-500/month est.
- **Notion API** (free for personal workspace)
- **Google Docs API** (free)
- **AWS Services**:
  - MWAA (Airflow): ~$300/month
  - RDS (Postgres): ~$50/month
  - Lambda (API): ~$10/month
  - S3 (logs): ~$5/month
- **Optional**: Sentry (free tier), Grafana Cloud (free tier)

### Development Tools
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 14+
- Airflow 2.7+ or Dagster 1.5+
- pytest, black, ruff

---

## Conclusion

✅ **Gap analysis complete**  
✅ **21 new issues created** (total: 38)  
✅ **All issues added to GitHub Project**  
✅ **Airflow/Dagster integration planned**  
✅ **Infrastructure coverage significantly improved**

The backlog now comprehensively covers:
- ✅ Core features (retrieval, extraction, clustering, serving)
- ✅ **NEW**: Orchestration (Airflow/Dagster DAGs)
- ✅ **NEW**: Infrastructure & DevOps
- ✅ **NEW**: Testing & Quality Assurance
- ✅ **NEW**: Monitoring & Observability
- ✅ **NEW**: Production deployment

**Status**: Ready to begin M1 implementation with full confidence in scope coverage.

---

**Related Artifacts**:
- Backlog CSV: `backlog.csv` (38 issues)
- GitHub Project: https://github.com/users/orgroman/projects/6
- Issues: #1-#38
- Wiki: https://github.com/orgroman/confradar/wiki
