# Project Views Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONFRADAR PROJECT VIEWS                       │
│           https://github.com/users/orgroman/projects/6           │
└─────────────────────────────────────────────────────────────────┘

📋 CURRENT STATE: 1 default view
🎯 RECOMMENDED: 10 specialized views

┌─────────────────────────────────────────────────────────────────┐
│ 1. 🎯 SPRINT BOARD (Kanban)                                      │
├─────────────────────────────────────────────────────────────────┤
│ Layout:  Board                                                   │
│ Group:   Status (Backlog → Ready → In Progress → Review → Done) │
│ Filter:  Current sprint (M1, M2, M3)                            │
│ Sort:    Priority (P0 → P3)                                      │
│ Use:     Daily standup, drag & drop workflow                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 2. 🗺️ ROADMAP (Timeline)                                        │
├─────────────────────────────────────────────────────────────────┤
│ Layout:  Roadmap (timeline visualization)                        │
│ Group:   Milestone (M1 → M7)                                     │
│ Filter:  None (show all)                                         │
│ Zoom:    Quarters                                                │
│ Use:     Long-term planning, stakeholder updates                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 3. 🔥 PRIORITY MATRIX (Table)                                    │
├─────────────────────────────────────────────────────────────────┤
│ Layout:  Table                                                   │
│ Group:   Priority                                                │
│ Filter:  P0, P1 only                                             │
│ Columns: Title, Status, Milestone, Area, Assignees              │
│ Use:     Focus on critical work, leadership view                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 4. 🏔️ BY MILESTONE (Board)                                      │
├─────────────────────────────────────────────────────────────────┤
│ Layout:  Board                                                   │
│ Group:   Milestone (M1 | M2 | M3 | M4 | M5 | M6 | M7)           │
│ Filter:  Status ≠ Done (hide completed)                          │
│ Sort:    Priority                                                │
│ Use:     Sprint planning, milestone tracking                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 5. 🏗️ BY AREA (Board)                                           │
├─────────────────────────────────────────────────────────────────┤
│ Layout:  Board                                                   │
│ Group:   Area labels                                             │
│ Columns: retrieval | extraction | clustering | kb | serving | infra
│ Sort:    Priority                                                │
│ Use:     Team assignment, technical coordination                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 6. 🚀 MVP CRITICAL PATH (Table)                                  │
├─────────────────────────────────────────────────────────────────┤
│ Layout:  Table                                                   │
│ Filter:  P0/P1 AND M1-M5 (MVP milestones)                        │
│ Columns: Title, Status, Priority, Milestone, Area, Dependencies │
│ Sort:    Priority → Milestone                                    │
│ Use:     MVP focus, blocking issues                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 7. 📊 CURRENT SPRINT (Table)                                     │
├─────────────────────────────────────────────────────────────────┤
│ Layout:  Table                                                   │
│ Filter:  Status: In Progress, In Review                          │
│ Columns: Title, Assignee, Priority, Milestone, Updated          │
│ Sort:    Updated (most recent)                                   │
│ Use:     Daily standup, WIP tracking                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 8. ✅ CI & QUALITY GATES (Table)                                  │
├─────────────────────────────────────────────────────────────────┤
│ Layout:  Table                                                   │
│ Filter:  label:area:infra  OR  label:type:bug label:area:infra  │
│         (optionally add: is:pr)                                  │
│ Columns: Title, Status, Priority, Labels, Assignees, Updated     │
│ Use:     Surface CI failures, coverage gates, infra work         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 9. 🧭 SCRAPERS PROGRESS (Board)                                   │
├─────────────────────────────────────────────────────────────────┤
│ Layout:  Board                                                   │
│ Group:   Component (custom field)                                │
│ Filter:  label:area:retrieval                                    │
│ Columns: AIDeadlines | ACL Web | ChairingTool | ELRA | WikiCFP   │
│ Use:     Track per-source progress                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 10. 🛠️ INFRA P0/P1 (Table)                                       │
├─────────────────────────────────────────────────────────────────┤
│ Layout:  Table                                                   │
│ Filter:  label:area:infra label:priority:P0,priority:P1          │
│ Columns: Title, Status, Priority, Assignees, Updated             │
│ Use:     Keep critical infra/testing front-and-center             │
└─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WORKFLOW GUIDE:

Morning Routine:
  1. Open "Current Sprint" → See what's active
  2. Check "Priority Matrix" → Pick next P0/P1 task
  3. Update "Sprint Board" → Move issue to In Progress

Sprint Planning:
  1. Review "By Milestone" → See upcoming work
  2. Filter "Priority Matrix" → Identify P0/P1 for next sprint
  3. Use "By Area" → Assign by team/expertise

Stakeholder Update:
  1. Show "Roadmap" → Timeline progress
  2. Show "MVP Critical Path" → Blockers and critical issues

Team Coordination:
  1. "By Area" view → See work per component
  2. Filter by assignee → Check individual workload

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ISSUE BREAKDOWN BY VIEW:

Sprint Board (M1-M3):
  ├─ Backlog: ~30 issues
  ├─ Ready: ~5 issues  
  ├─ In Progress: ~3 issues
  └─ Done: ~0 issues (fresh project)

Priority Matrix (P0/P1):
  ├─ P0: 3 issues (#39, #53, #60 + scrapers)
  └─ P1: 13 issues (tooling, scrapers, eval)

By Milestone:
  ├─ M1 (Requirements): 11 issues
  ├─ M2 (Data Sources): 8 issues
  ├─ M3 (Extraction): 3 issues
  ├─ M4 (Clustering): 3 issues (from original)
  ├─ M5 (Integration): 5 issues (from original)
  ├─ M6 (Evaluation): 6 issues
  └─ M7 (Deployment): 7 issues

By Area:
  ├─ area:retrieval: 12 issues (crawling/scraping)
  ├─ area:extraction: 10 issues (NLP/LLM)
  ├─ area:clustering: 3 issues (alias resolution)
  ├─ area:kb: 8 issues (database/storage)
  ├─ area:serving: 5 issues (APIs/output)
  └─ area:infra: 23 issues (DevOps/tooling)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SETUP TIME ESTIMATE:

✓ Create 7 views: ~15 minutes
✓ Configure filters/sorts: ~5 minutes
✓ Test views: ~5 minutes
─────────────────────────────
TOTAL: ~25 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEYBOARD SHORTCUTS:

  C        Create new issue
  E        Edit issue inline
  /        Focus search
  ?        Show all shortcuts
  Cmd+K    Command palette

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT STEPS:

1. Follow setup guide: docs/PROJECT_VIEWS_SETUP.md
2. Create 10 views (20-25 min)
3. Set "Sprint Board" as default
4. Bookmark frequently used views
5. Share view URLs with team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Quick Filter Cheatsheet

```bash
# By Priority
label:priority:P0
label:priority:P0,priority:P1

# By Milestone  
milestone:"M1: Requirements & Design"
milestone:M1,M2,M3

# By Area
label:area:retrieval
label:area:extraction,area:clustering

# By Status
status:"In Progress"
-status:Done

# Complex (AND conditions)
label:priority:P0,priority:P1 milestone:M1,M2 -status:Done
```

## View URLs (after creation)

Once you create the views, bookmark these:

- Sprint Board: `https://github.com/users/orgroman/projects/6?view=2`
- Roadmap: `https://github.com/users/orgroman/projects/6?view=3`
- Priority Matrix: `https://github.com/users/orgroman/projects/6?view=4`
- By Milestone: `https://github.com/users/orgroman/projects/6?view=5`
- By Area: `https://github.com/users/orgroman/projects/6?view=6`
- MVP Critical: `https://github.com/users/orgroman/projects/6?view=7`
- Current Sprint: `https://github.com/users/orgroman/projects/6?view=8`
 - CI & Quality Gates: `https://github.com/users/orgroman/projects/6?view=9`
 - Scrapers Progress: `https://github.com/users/orgroman/projects/6?view=10`
 - Infra P0/P1: `https://github.com/users/orgroman/projects/6?view=11`

---

**Reference:** `docs/PROJECT_VIEWS_SETUP.md` (detailed guide)
