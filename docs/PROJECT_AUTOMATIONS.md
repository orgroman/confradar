# GitHub Project Automation Examples

These automations can enhance your GitHub Project workflow. They use built-in GitHub Actions workflows.

---

## 1. Auto-Label New Issues by Milestone

Automatically add appropriate area labels when issues are assigned to specific milestones.

**File:** `.github/workflows/auto-label-by-milestone.yml`

```yaml
name: Auto-label by Milestone

on:
  issues:
    types: [milestoned]

jobs:
  auto-label:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    
    steps:
      - name: Label M1 issues
        if: github.event.milestone.title == 'M1: Requirements & Design'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: ['area:infra']
            })
      
      - name: Label M2 issues
        if: github.event.milestone.title == 'M2: Data Source Integration & Web Crawling'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: ['area:retrieval']
            })
      
      - name: Label M3 issues
        if: github.event.milestone.title == 'M3: Information Extraction Pipeline'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: ['area:extraction']
            })
```

---

## 2. Move Issues to "In Review" When PR Opens

Automatically update project status when a PR is linked to an issue.

**File:** `.github/workflows/auto-move-to-review.yml`

```yaml
name: Auto-move to In Review

on:
  pull_request:
    types: [opened, reopened]

jobs:
  move-to-review:
    runs-on: ubuntu-latest
    permissions:
      repository-projects: write
    
    steps:
      - name: Move linked issues to In Review
        uses: actions/github-script@v7
        with:
          script: |
            // Extract issue numbers from PR body
            const prBody = context.payload.pull_request.body || '';
            const issueNumbers = prBody.match(/(?:close|closes|fix|fixes|resolve|resolves)\s+#(\d+)/gi);
            
            if (!issueNumbers) return;
            
            for (const match of issueNumbers) {
              const issueNumber = match.match(/\d+/)[0];
              
              // Add comment to issue
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issueNumber,
                body: `🔄 Moved to **In Review** - PR #${context.payload.pull_request.number} opened`
              });
              
              // Note: Moving in Project v2 requires GraphQL API
              // See: https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects
            }
```

---

## 3. Weekly Sprint Report

Generate a weekly summary of completed issues.

**File:** `.github/workflows/weekly-sprint-report.yml`

```yaml
name: Weekly Sprint Report

on:
  schedule:
    - cron: '0 9 * * 1' # Every Monday at 9 AM UTC
  workflow_dispatch: # Allow manual trigger

jobs:
  generate-report:
    runs-on: ubuntu-latest
    permissions:
      issues: read
      contents: write
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Generate Report
        uses: actions/github-script@v7
        with:
          script: |
            const oneWeekAgo = new Date();
            oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
            
            // Get closed issues from last week
            const { data: issues } = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'closed',
              since: oneWeekAgo.toISOString(),
              per_page: 100
            });
            
            // Group by milestone
            const byMilestone = {};
            for (const issue of issues) {
              const milestone = issue.milestone?.title || 'No Milestone';
              if (!byMilestone[milestone]) byMilestone[milestone] = [];
              byMilestone[milestone].push(issue);
            }
            
            // Generate markdown report
            let report = `# Sprint Report - Week of ${oneWeekAgo.toISOString().split('T')[0]}\n\n`;
            report += `## Summary\n\n`;
            report += `- **Total Completed:** ${issues.length} issues\n`;
            report += `- **By Priority:**\n`;
            
            const p0 = issues.filter(i => i.labels.some(l => l.name === 'priority:P0')).length;
            const p1 = issues.filter(i => i.labels.some(l => l.name === 'priority:P1')).length;
            const p2 = issues.filter(i => i.labels.some(l => l.name === 'priority:P2')).length;
            
            report += `  - P0: ${p0}\n`;
            report += `  - P1: ${p1}\n`;
            report += `  - P2: ${p2}\n\n`;
            
            // By milestone
            report += `## Completed by Milestone\n\n`;
            for (const [milestone, milestoneIssues] of Object.entries(byMilestone)) {
              report += `### ${milestone} (${milestoneIssues.length})\n\n`;
              for (const issue of milestoneIssues) {
                report += `- #${issue.number}: ${issue.title}\n`;
              }
              report += `\n`;
            }
            
            console.log(report);
            
            // Save to file (optional)
            const fs = require('fs');
            fs.writeFileSync('sprint-report.md', report);
      
      - name: Commit Report
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add sprint-report.md || true
          git commit -m "Weekly sprint report" || true
          git push || true
```

---

## 4. Stale Issue Management

Mark issues as stale if no activity for 60 days.

**File:** `.github/workflows/stale.yml`

```yaml
name: Mark Stale Issues

on:
  schedule:
    - cron: '0 0 * * *' # Daily at midnight
  workflow_dispatch:

jobs:
  stale:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
    
    steps:
      - uses: actions/stale@v9
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          days-before-stale: 60
          days-before-close: 14
          stale-issue-message: |
            👋 This issue has been automatically marked as stale because it has not had recent activity.
            It will be closed in 14 days if no further activity occurs.
            
            If this issue is still relevant, please:
            - Add a comment explaining why it should remain open
            - Update the issue with current status
            - Add it to the current sprint if it's a priority
          stale-issue-label: 'stale'
          exempt-issue-labels: 'priority:P0,priority:P1,in-progress'
          exempt-milestones: 'M1: Requirements & Design,M2: Data Source Integration & Web Crawling,M3: Information Extraction Pipeline'
```

---

## 5. Priority Assignment for New Issues

Automatically assign P2 priority to new issues without priority label.

**File:** `.github/workflows/default-priority.yml`

```yaml
name: Default Priority

on:
  issues:
    types: [opened]

jobs:
  assign-priority:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    
    steps:
      - name: Check if priority exists
        id: check
        uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;
            const hasPriority = issue.labels.some(label => 
              label.name.startsWith('priority:')
            );
            return hasPriority;
      
      - name: Add default P2 priority
        if: steps.check.outputs.result == 'false'
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: ['priority:P2']
            });
            
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '🏷️ Automatically assigned **priority:P2**. Adjust if needed.'
            });
```

---

## 6. Dependency Checker

Warn when closing issues that are dependencies for other issues.

**File:** `.github/workflows/check-dependencies.yml`

```yaml
name: Check Dependencies

on:
  issues:
    types: [closed]

jobs:
  check-deps:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    
    steps:
      - name: Check for dependent issues
        uses: actions/github-script@v7
        with:
          script: |
            const closedIssueNumber = context.issue.number;
            
            // Search for issues that depend on this one
            const { data: allIssues } = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open',
              per_page: 100
            });
            
            const dependents = allIssues.filter(issue => {
              const body = issue.body || '';
              return body.includes(`Depends on #${closedIssueNumber}`) ||
                     body.includes(`Blocked by #${closedIssueNumber}`);
            });
            
            if (dependents.length > 0) {
              let comment = `✅ Issue closed. The following issues were depending on this:\n\n`;
              for (const dep of dependents) {
                comment += `- #${dep.number}: ${dep.title}\n`;
              }
              comment += `\n⚠️ These issues may now be unblocked!`;
              
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: closedIssueNumber,
                body: comment
              });
            }
```

---

## 7. New Issue Welcome Message

Add helpful context to new issues based on labels.

**File:** `.github/workflows/issue-welcome.yml`

```yaml
name: Issue Welcome

on:
  issues:
    types: [labeled]

jobs:
  welcome:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    
    steps:
      - name: Welcome message for bugs
        if: github.event.label.name == 'type:bug'
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `🐛 **Bug Report Guidelines**
              
              Thanks for reporting this bug! To help us fix it quickly, please ensure:
              
              - [ ] Steps to reproduce are clear
              - [ ] Expected vs actual behavior is documented
              - [ ] Environment details provided (Python version, OS)
              - [ ] Relevant logs/screenshots attached
              
              See: [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.yml)`
            });
      
      - name: Welcome message for features
        if: github.event.label.name == 'type:feature'
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `✨ **Feature Request Guidelines**
              
              Thanks for the suggestion! Before implementation:
              
              - [ ] Check if it aligns with MVP scope
              - [ ] Consider impact on existing architecture
              - [ ] Estimate effort (XS/S/M/L/XL)
              - [ ] Identify dependencies on other issues
              
              See: [PRD](docs/confradar_prd.md) for scope guidance`
            });
```

---

## Installation Instructions

1. **Create workflow files:**
   ```bash
   mkdir -p .github/workflows
   # Copy desired workflows from above
   ```

2. **Enable GitHub Actions:**
   - Go to Settings → Actions → General
   - Enable "Allow all actions and reusable workflows"

3. **Test workflows:**
   - Create a test issue to trigger automations
   - Check Actions tab for workflow runs

4. **Customize:**
   - Adjust schedules (cron expressions)
   - Modify labels and milestones to match your project
   - Add Slack/Discord notifications if needed

---

## Advanced: GraphQL for Projects v2

Projects v2 requires GraphQL API. Example to update issue status:

```javascript
const query = `
  mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: String!) {
    updateProjectV2ItemFieldValue(
      input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: { singleSelectOptionId: $value }
      }
    ) {
      projectV2Item {
        id
      }
    }
  }
`;

// Get IDs using gh CLI or GraphQL explorer
const variables = {
  projectId: "PVT_...",  // Project ID
  itemId: "PVTI_...",    // Issue ID in project
  fieldId: "PVTF_...",   // Status field ID
  value: "PVTSSOV_..."   // "In Review" option ID
};
```

See: https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects

---

## Slack/Discord Integration (Optional)

**Slack notification on issue closure:**

```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "✅ Issue #${{ github.event.issue.number }} closed: ${{ github.event.issue.title }}"
      }
```

**Discord webhook:**

```yaml
- name: Notify Discord
  run: |
    curl -H "Content-Type: application/json" \
         -d '{"content": "✅ Issue #${{ github.event.issue.number }} closed"}' \
         ${{ secrets.DISCORD_WEBHOOK }}
```

---

## Next Steps

1. Choose 2-3 automations to start with
2. Create workflow files in `.github/workflows/`
3. Test on a non-critical issue
4. Iterate based on team feedback
5. Add more automations as needed

---

**See also:**
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Projects v2 API](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project)
- [Workflow Examples](https://github.com/actions/starter-workflows)
