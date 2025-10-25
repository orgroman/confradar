# GitHub Project Custom Fields Setup Guide

**Project:** https://github.com/users/orgroman/projects/6  
**Status:** ✅ All 61 issues assigned to @orgroman  
**Next Step:** Add custom date fields for roadmap visualization

---

## Overview

GitHub Projects v2 supports custom fields that enable:
- **Roadmap view** with timeline visualization
- **Start/End dates** for sprint planning
- **Effort estimation** for capacity planning
- **Status tracking** beyond GitHub's default states

---

## 🎯 Recommended Custom Fields

### 1. **Start Date** (Date field)
- **Purpose:** When work on the issue begins
- **Type:** Date
- **Usage:** Roadmap visualization, sprint planning
- **Example:** 2025-11-01

### 2. **Target Date** / **Due Date** (Date field)
- **Purpose:** When the issue should be completed
- **Type:** Date
- **Usage:** Roadmap timeline, deadline tracking
- **Example:** 2025-11-15

### 3. **Effort** (Single select)
- **Purpose:** Estimated time to complete
- **Type:** Single select
- **Options:**
  - 🔵 XS (< 2 hours)
  - 🟢 S (2-4 hours, ~half day)
  - 🟡 M (1-2 days)
  - 🟠 L (3-5 days, ~1 week)
  - 🔴 XL (1-2 weeks)
  - 🟣 XXL (> 2 weeks)

### 4. **Sprint** (Single select)
- **Purpose:** Which sprint/iteration the issue belongs to
- **Type:** Single select
- **Options:**
  - Sprint 1 (Nov 2025)
  - Sprint 2 (Dec 2025)
  - Sprint 3 (Jan 2026)
  - Sprint 4 (Feb 2026)
  - Backlog

### 5. **Status** (Single select) - Enhanced
- **Purpose:** More granular status than GitHub's default
- **Type:** Single select
- **Options:**
  - 📋 Backlog
  - 🔍 Refinement (needs clarification)
  - ✅ Ready (groomed, ready to start)
  - 🏗️ In Progress
  - 🔄 In Review (PR opened)
  - ✔️ Done
  - 🚫 Blocked
  - ❄️ On Hold

### 6. **Dependencies** (Text field)
- **Purpose:** Track blocking issues
- **Type:** Text
- **Format:** "Blocked by #XX" or "Depends on #YY, #ZZ"
- **Example:** "Blocked by #39, #53"

### 7. **Team** (Single select) - Optional
- **Purpose:** Which team/area owns this
- **Type:** Single select
- **Options:**
  - Backend
  - Data/ML
  - DevOps/Infra
  - Full Stack

---

## 📅 Step-by-Step: Adding Custom Fields

### Step 1: Access Project Settings

1. Go to: https://github.com/users/orgroman/projects/6
2. Click **⚙️ Settings** (three dots menu → Settings)
3. In the left sidebar, click **Custom fields**

### Step 2: Add "Start Date" Field

1. Click **+ New field**
2. Configure:
   - **Field name:** `Start Date`
   - **Field type:** Select **Date**
   - **Description (optional):** "When work on this issue begins"
3. Click **Save**

### Step 3: Add "Target Date" Field

1. Click **+ New field**
2. Configure:
   - **Field name:** `Target Date`
   - **Field type:** Select **Date**
   - **Description (optional):** "When this issue should be completed"
3. Click **Save**

### Step 4: Add "Effort" Field

1. Click **+ New field**
2. Configure:
   - **Field name:** `Effort`
   - **Field type:** Select **Single select**
   - **Options:** (add each):
     - `XS` (color: blue)
     - `S` (color: green)
     - `M` (color: yellow)
     - `L` (color: orange)
     - `XL` (color: red)
     - `XXL` (color: purple)
   - **Description:** "Estimated effort (XS=<2h, S=2-4h, M=1-2d, L=3-5d, XL=1-2w, XXL=>2w)"
3. Click **Save**

### Step 5: Add "Sprint" Field

1. Click **+ New field**
2. Configure:
   - **Field name:** `Sprint`
   - **Field type:** Select **Single select**
   - **Options:** (add each):
     - `Sprint 1 (Nov 2025)`
     - `Sprint 2 (Dec 2025)`
     - `Sprint 3 (Jan 2026)`
     - `Sprint 4 (Feb 2026)`
     - `Backlog`
3. Click **Save**

### Step 6: Add "Status" Field (Enhanced)

1. Click **+ New field**
2. Configure:
   - **Field name:** `Status`
   - **Field type:** Select **Single select**
   - **Options:** (add each with emoji):
     - `📋 Backlog`
     - `🔍 Refinement`
     - `✅ Ready`
     - `🏗️ In Progress`
     - `🔄 In Review`
     - `✔️ Done`
     - `🚫 Blocked`
     - `❄️ On Hold`
3. Click **Save**

### Step 7: Add "Dependencies" Field

1. Click **+ New field**
2. Configure:
   - **Field name:** `Dependencies`
   - **Field type:** Select **Text**
   - **Description:** "Format: 'Blocked by #XX' or 'Depends on #YY, #ZZ'"
3. Click **Save**

---

## 📊 Configuring Roadmap View with Dates

### Step 1: Open/Create Roadmap View

1. In your project, click the **+** next to view tabs
2. Select **New view**
3. Choose **Roadmap** layout
4. Name it: `Roadmap`

### Step 2: Configure Date Fields

1. In the Roadmap view, click **⋯** (three dots) → **Settings**
2. Under **Date fields:**
   - **Start date:** Select `Start Date` (your custom field)
   - **Target date:** Select `Target Date` (your custom field)
3. Under **Vertical grouping:**
   - Select **Milestone** (to show M1-M7 swim lanes)
4. Click **Save**

### Step 3: Adjust Timeline

- **Zoom levels:** Month / Quarter / Year
- **Markers:** Show milestone boundaries
- **Color coding:** By priority or status

---

## 🎯 Populating Fields with Realistic Dates

Now that fields are created, let's populate them based on the milestone timeline from the PRD:

### Milestone Timeline (from PRD)

| Milestone | Duration | Start Date | End Date |
|-----------|----------|------------|----------|
| M1: Requirements & Design | Month 1-2 | 2025-11-01 | 2025-12-31 |
| M2: Data Source Integration | Month 2-3 | 2025-12-01 | 2026-01-31 |
| M3: Information Extraction | Month 3-4 | 2026-01-01 | 2026-02-28 |
| M4: Clustering & Alias | Month 4-5 | 2026-02-01 | 2026-03-31 |
| M5: Agent Integration | Month 5-6 | 2026-03-01 | 2026-04-30 |
| M6: Evaluation & Iteration | Month 6 | 2026-04-01 | 2026-04-30 |
| M7: Deployment | Month 7 | 2026-05-01 | 2026-05-31 |

### Bulk Update Strategy

You can update fields in bulk:

1. **In Project Board:**
   - Select multiple issues (checkbox)
   - Click **⋯** → **Set field value**
   - Choose field (e.g., Sprint, Effort, Status)
   - Apply to all selected

2. **Individual Updates:**
   - Click on an issue card in the project
   - Edit fields in the right sidebar
   - Changes save automatically

---

## 💡 Suggested Field Values by Milestone

### M1 Issues (#3, #16, #17, #39-45, #53, #59)
- **Sprint:** Sprint 1 (Nov 2025)
- **Start Date:** 2025-11-01
- **Target Date:** 2025-12-31
- **Effort:** 
  - Docs (#17, #59): S
  - Python setup (#39-45): S-M
  - LLM API (#53): M
- **Status:** Ready (P0/P1) or Backlog (P2)

### M2 Issues (#1, #7, #18, #22, #46-50, #52, #60, #61)
- **Sprint:** Sprint 2 (Dec 2025) - Sprint 3 (Jan 2026)
- **Start Date:** 2025-12-01
- **Target Date:** 2026-01-31
- **Effort:**
  - Scrapers (#46-50): M-L each
  - ORM (#60): L
  - Infrastructure (#18, #22): L-XL
- **Status:** Ready (P0/P1) or Backlog (P2)

### M3 Issues (#4, #5, #6, #20, #51, #54, #55)
- **Sprint:** Sprint 3 (Jan 2026)
- **Start Date:** 2026-01-01
- **Target Date:** 2026-02-28
- **Effort:**
  - Extraction (#4, #5): M-L
  - LangChain (#54): L
  - Prompts (#55): M
- **Status:** Backlog

### M4-M7 Issues (remaining)
- Set dates according to milestone timeline above
- Most in **Backlog** status
- Effort varies by complexity

---

## 🚀 Quick Start Checklist

Use this checklist to get your project fully configured:

- [ ] **Step 1:** Add all 7 custom fields (15 min)
  - [ ] Start Date
  - [ ] Target Date
  - [ ] Effort
  - [ ] Sprint
  - [ ] Status
  - [ ] Dependencies
  - [ ] Team (optional)

- [ ] **Step 2:** Configure Roadmap view (5 min)
  - [ ] Set Start Date field
  - [ ] Set Target Date field
  - [ ] Group by Milestone
  - [ ] Adjust zoom to Quarters

- [ ] **Step 3:** Populate high-priority issues (20 min)
  - [ ] Set Sprint for M1 issues (Sprint 1)
  - [ ] Set Start/Target dates for M1 issues
  - [ ] Set Effort estimates for P0/P1 issues
  - [ ] Set Status to "Ready" for immediate work

- [ ] **Step 4:** Bulk populate remaining issues (30 min)
  - [ ] Group select by milestone
  - [ ] Set Sprint in bulk
  - [ ] Set approximate dates
  - [ ] Set Status to "Backlog"

**Total time: ~1 hour**

---

## 📋 Example: Filling Out Issue #39 (Python Project Structure)

Here's how to fill out a complete issue:

```
Issue #39: Python project structure and pyproject.toml

✅ Already Set:
- Assignee: @orgroman
- Labels: type:task, area:infra, priority:P0
- Milestone: M1: Requirements & Design
- Description: [detailed body text]

🆕 Custom Fields to Add:
- Start Date: 2025-11-01
- Target Date: 2025-11-08 (1 week)
- Effort: M (1-2 days)
- Sprint: Sprint 1 (Nov 2025)
- Status: ✅ Ready
- Dependencies: (none - this is a blocker for others)
- Team: DevOps/Infra
```

---

## 🔄 Dependencies Setup Examples

For issues with dependencies, use this format in the Dependencies field:

**Issue #60 (SQLAlchemy ORM models):**
```
Depends on #39 (Python structure), #59 (schema docs)
```

**Issue #54 (LangChain agent):**
```
Blocked by #53 (LLM API setup)
```

**Issue #46 (AI Deadlines scraper):**
```
Depends on #61 (BeautifulSoup implementation)
```

---

## 📊 Using Fields in Views

### Roadmap View
- **Shows:** Timeline bars for each issue
- **X-axis:** Time (Start Date → Target Date)
- **Y-axis:** Grouped by Milestone
- **Color:** By Status or Priority
- **Use:** Visualize project timeline, identify overlaps

### Sprint Board View
- **Filter:** `Sprint: "Sprint 1 (Nov 2025)"`
- **Group by:** Status
- **Use:** Daily standup, current sprint work

### Effort/Capacity View
- **Group by:** Effort
- **Filter:** `Status: "Ready", "In Progress"`
- **Use:** Capacity planning, see if sprint is overloaded

---

## 🎨 Color Coding Suggestions

### By Priority (in Roadmap)
- 🔴 P0: Red
- 🟠 P1: Orange  
- 🟡 P2: Yellow
- 🟢 P3: Green

### By Status
- 📋 Backlog: Gray
- ✅ Ready: Blue
- 🏗️ In Progress: Purple
- 🔄 In Review: Orange
- ✔️ Done: Green
- 🚫 Blocked: Red

---

## 🔗 Resources

- **GitHub Docs:** [Managing custom fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields)
- **Roadmap Layout:** [Using roadmap layout](https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/customizing-the-roadmap-layout)
- **Project Automation:** See `docs/PROJECT_AUTOMATIONS.md`

---

## ⚡ Pro Tips

1. **Batch Updates:** Select 10-20 issues at once, set fields in bulk
2. **Copy from Similar Issues:** Use existing issue as template
3. **Roadmap Drag & Drop:** Drag timeline bars to adjust dates
4. **Filters:** Create saved filters like "My Sprint" or "Blocked Items"
5. **Iterations:** GitHub also supports "Iteration" field type for sprints

---

## 🎯 Next Steps

1. Add the 7 custom fields (this guide, Step-by-Step section)
2. Configure Roadmap view with Start/Target dates
3. Populate P0/P1 issues first (Sprint 1 work)
4. Gradually fill in remaining issues
5. Use Roadmap view for planning and stakeholder updates

**Estimated setup time:** 1 hour  
**Maintenance:** 5-10 min/week (update as issues progress)

---

**Last updated:** 2025-10-25  
**Status:** Ready to implement  
**All 61 issues assigned to:** @orgroman ✅
