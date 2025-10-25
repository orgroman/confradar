# GitHub Project Views Setup Guide

**Project:** https://github.com/users/orgroman/projects/6  
**Current State:** Single default view  
**Goal:** Create 7 organized views for sprint planning and progress tracking

---

## Recommended Views

### 1. 🎯 **Sprint Board** (Kanban by Status)

**Purpose:** Daily standup view - what's in progress, what's next

**Setup:**
1. Click "+" next to current view → "New view"
2. Name: "Sprint Board"
3. Layout: **Board**
4. Group by: **Status**
5. Add custom statuses:
   - 🆕 Backlog
   - 📋 Ready
   - 🏗️ In Progress
   - 👀 In Review
   - ✅ Done

**Filters:**
- Milestone: `is:M1, M2, M3` (current sprint only)

**Sort:** Priority (P0 → P3)

---

### 2. 🗺️ **Roadmap** (Timeline by Milestone)

**Purpose:** High-level progress visualization across all milestones

**Setup:**
1. New view → "Roadmap"
2. Layout: **Roadmap** (timeline view)
3. Group by: **Milestone**
4. Date field: Use milestone due dates

**Configuration:**
- Show: All items (no filters)
- Zoom: Quarters
- Markers: Milestone boundaries

---

### 3. 🔥 **Priority Matrix** (Table by Priority)

**Purpose:** Focus on what's most important (P0/P1 issues)

**Setup:**
1. New view → "Priority Matrix"
2. Layout: **Table**
3. Group by: **Priority**
4. Filter: `priority:P0, P1`

**Visible columns:**
- Title
- Status
- Milestone
- Labels (area:*)
- Assignees

**Sort:** 
- Primary: Priority (P0 first)
- Secondary: Milestone

---

### 4. 🏔️ **By Milestone** (Board grouped by Milestone)

**Purpose:** See all work organized by project phase

**Setup:**
1. New view → "By Milestone"
2. Layout: **Board**
3. Group by: **Milestone**
4. Columns: M1, M2, M3, M4, M5, M6, M7

**Sort:** Priority within each column

**Filters:** Status: not "Done" (hide completed)

---

### 5. 🏗️ **By Area** (Board grouped by Technical Area)

**Purpose:** Organize work by system component (for team assignment)

**Setup:**
1. New view → "By Area"
2. Layout: **Board**
3. Group by: **Labels** (select area:* labels)
4. Columns:
   - area:retrieval (crawling/scraping)
   - area:extraction (NLP/LLM)
   - area:clustering (alias resolution)
   - area:kb (database/storage)
   - area:serving (APIs/output)
   - area:infra (DevOps/tooling)

**Sort:** Priority

---

### 6. 🚀 **MVP Critical Path** (Table - P0/P1 only)

**Purpose:** Laser focus on must-have features for MVP

**Setup:**
1. New view → "MVP Critical Path"
2. Layout: **Table**
3. Filter: `priority:P0, P1` AND `milestone:M1, M2, M3, M4, M5`

**Visible columns:**
- Title
- Status
- Priority
- Milestone
- Area (labels)
- Assignees
- Dependencies (if tracked)

**Sort:** 
- Priority (P0 first)
- Then by Milestone

**Highlight:** P0 issues in red/orange

---

### 7. 📊 **Current Sprint** (Table - Active work)

**Purpose:** What's being worked on right now

**Setup:**
1. New view → "Current Sprint"
2. Layout: **Table**
3. Filter: `status:"In Progress", "In Review"`

**Visible columns:**
- Title
- Assignee
- Priority
- Milestone
- Labels (all)
- Updated (last modified)

**Sort:** Updated (most recent first)

**Use:** Daily standups - who's working on what

---

## Quick Setup Steps

### Step 1: Access Project Settings
```
1. Go to: https://github.com/users/orgroman/projects/6
2. Click Settings (gear icon in top right)
3. Under "Manage access" - ensure you have admin rights
```

### Step 2: Create Views
```
For each view above:
1. Click "+" next to the current view tab
2. Select "New view"
3. Choose layout type (Table/Board/Roadmap)
4. Name the view
5. Configure grouping/sorting/filters
6. Click "Save changes"
```

### Step 3: Configure Custom Fields (if needed)

Add these custom fields to track additional metadata:

**Effort Estimate:**
- Type: Single select
- Options: XS (< 2h), S (2-4h), M (1-2d), L (3-5d), XL (1-2w)

**Dependencies:**
- Type: Text
- Format: "Blocked by #XX" or "Depends on #YY"

**Sprint:**
- Type: Single select
- Options: Sprint 1, Sprint 2, Sprint 3, etc.

To add custom fields:
1. Settings → Custom fields → "New field"
2. Configure as above
3. Apply to all views

---

## View Usage Guidelines

### Daily Work
- **Start day:** Check "Current Sprint" view
- **Pick next task:** Use "Priority Matrix" or "Sprint Board"
- **Update status:** Drag issues across "Sprint Board"

### Sprint Planning
- **Review:** "By Milestone" view
- **Prioritize:** "Priority Matrix" view
- **Assign:** "By Area" view (group by technical expertise)

### Stakeholder Updates
- **Progress:** "Roadmap" view
- **Critical issues:** "MVP Critical Path" view

### Team Coordination
- **Backend team:** Filter "By Area" to area:retrieval, area:extraction, area:kb
- **DevOps team:** Filter to area:infra
- **ML team:** Filter to area:extraction, area:clustering

---

## Filters Cheat Sheet

### Common Filters

**By Priority:**
```
label:priority:P0
label:priority:P0,priority:P1
```

**By Milestone:**
```
milestone:"M1: Requirements & Design"
milestone:M1,M2,M3
```

**By Area:**
```
label:area:retrieval
label:area:extraction,area:clustering
```

**By Type:**
```
label:type:feature
label:type:bug
label:type:task,type:feature
```

**By Status:**
```
status:"In Progress"
status:"Backlog","Ready"
-status:Done (everything except Done)
```

**Complex Filters:**
```
label:priority:P0,priority:P1 milestone:M1,M2 -status:Done
(High priority, early milestones, not done)

label:area:infra status:"Backlog","Ready"
(Infrastructure work ready to start)
```

---

## Saved Views Quick Reference

| View | Best For | Layout | Key Filter |
|------|----------|--------|------------|
| Sprint Board | Daily work | Board | Current sprint milestones |
| Roadmap | Timeline | Roadmap | All issues |
| Priority Matrix | Focus | Table | P0, P1 only |
| By Milestone | Planning | Board | Group by milestone |
| By Area | Assignment | Board | Group by area labels |
| MVP Critical Path | Leadership | Table | P0/P1, M1-M5 |
| Current Sprint | Standup | Table | In Progress/Review |

---

## Automation Suggestions

Consider adding GitHub Actions workflows for:

### Auto-label by milestone
When issue assigned to M1, auto-add priority:P1 if not set

### Auto-close stale issues
If issue in "Backlog" for >90 days with no activity, label as stale

### Auto-move to "In Review"
When PR linked to issue is opened, move to "In Review" status

### Sprint report
Weekly: Generate report of completed issues per sprint

(These require GitHub Actions - can provide examples if needed)

---

## Tips & Tricks

### Keyboard Shortcuts
- `C` - Create new issue
- `?` - Show shortcuts
- `E` - Edit issue inline
- `/` - Focus search

### Bulk Operations
1. Select multiple issues (checkbox)
2. Click "..." menu
3. Bulk update: labels, milestone, status, assignee

### Permalink Views
Each view has a unique URL - bookmark your most-used views:
- Sprint Board: `.../projects/6?view=2`
- Priority Matrix: `.../projects/6?view=3`

### Mobile Access
GitHub Mobile app supports Projects v2 - views sync automatically

---

## Next Steps

1. **Create views** following the guide above (15-20 min)
2. **Add custom fields** if needed (5 min)
3. **Share with team** - send bookmarks to specific views
4. **Set default view** - Settings → Default view (recommend "Sprint Board")
5. **Archive old issues** - Move completed M1 issues to Done

---

## Example: Creating "Sprint Board" (Step-by-Step)

1. Go to https://github.com/users/orgroman/projects/6
2. Click "+" next to "View 1" tab (top left)
3. Click "New view"
4. In the modal:
   - Name: `Sprint Board`
   - Layout: Select **Board** radio button
   - Click "Create"
5. View is created. Now configure:
   - Click "Group by" dropdown → Select **Status**
   - Click "Filter" → Type: `milestone:M1,M2,M3`
   - Click "Sort" → Select **Priority** (High to Low)
6. Click "Save changes" (top right)
7. View is ready! ✅

Repeat for other 6 views using the configurations above.

---

## Questions?

If you need help with:
- **Automations** - I can create GitHub Actions workflows
- **Custom fields** - I can suggest additional tracking fields
- **Integrations** - Connect to Slack, Discord, or email notifications
- **Reports** - Generate sprint reports or burndown charts

Just let me know!

---

**Last updated:** 2025-01-23  
**Project:** ConfRadar  
**Status:** Ready to implement
