---
applyTo: "**"
---

# Copilot Agent Behavior

## Task Execution
- The Copilot coding agent is allowed to create a new branch, commit code, push that branch, and open or update a pull request.
- The agent is encouraged to **self-assign or be assigned to GitHub issues** that describe well-scoped tasks.
- **Delegation to the Copilot Coding Agent must always be performed through the GitHub MCP server’s `assign_copilot_to_issue` tool**, ensuring that the assignment is visible in both the issue metadata and the MCP activity log.
- When a PR is ready and all required checks pass, the agent is encouraged to **merge** it automatically (subject to branch protection rules and merge-gate conditions below).

## Pull Request Expectations
Every PR created or updated by the agent must include:
- A clear summary of what changed and why.
- Whether any tests were added or updated.
- Whether any API behavior or ingestion behavior changed.
- Whether any UI under `web/**` was modified using Vercel v0 MCP.
- A note if this PR is addressing any automated review feedback (for example, from the Vercel review agent) and which comments were resolved.

## Safety and Scope
- The agent must not delete files that are unrelated to the described task.
- The agent must not downgrade or upgrade dependencies unless the task was explicitly about dependency management.
- The agent must not remove error handling, retry logic, or idempotency in ingestion / OCR / crawling / document storage flows.
- Large-scale ingestion / storage / pipeline changes must go in a dedicated PR, not bundled with UI or cosmetic refactors.

## Rate Limiting
- The agent is rate-limited.
- Do not spin up multiple parallel agent tasks for unrelated work.
- Queue work as separate GitHub issues and delegate them one at a time.

## Delegation Monitoring
When work is delegated to the Copilot Agent (via the **GitHub MCP server’s `assign_copilot_to_issue`** tool), we require lightweight monitoring so the repo doesn’t fill up with abandoned half-done branches.

**Agent responsibilities**
- When starting work on an issue, the agent must either:
  - link the new branch and PR back in the original issue, or
  - update the issue body with “In progress: <branch name> / <PR #>”.
- When it pushes follow-up commits in response to review (including Vercel review agent comments for frontend code), it must update the PR description with a short “Status” section describing what was addressed.
- When it considers a task “done,” it must explicitly request review on the PR and mark the parent issue as “Pending review.”
- After review approval and passing checks, the agent **should merge the PR** and close or comment on the corresponding issue.

**Human responsibilities**
- At least once per active milestone / sprint, review all open issues that are currently assigned to Copilot Agent or tagged as being handled by the agent.
  - Close any issue whose PR was merged.
  - Unassign the agent from issues where no branch or PR exists after delegation (the task was never actually executed).
  - Re-scope or rewrite vague issues so future delegation is not garbage.
- If the agent opened multiple PRs for what should have been one logical task, consolidate: leave one PR open, close the others, and update the parent issue to point to the surviving PR.

## Merge Gate
- A PR produced or updated by the agent cannot be merged if:
  - there is an unresolved open issue assigned to the agent with the same scope, or
  - the PR description does not include a clear status of what was addressed and what is still pending.

The goal here is simple: any task offloaded to the Copilot Agent must have a visible “owner,” a visible assignment through the MCP interface, and a visible end state. Nothing is allowed to just sit in limbo.
