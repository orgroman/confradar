# Instructions for Confradar

Default project rules and conventions for this repository.
---

## Documentation and Wiki
- The wiki is the source of truth.  
- Always read the wiki before suggesting or changing architecture, ingestion flows, or pipeline logic.  
- Keep the wiki up to date whenever behavior or configuration changes.

## Issues and Next Steps
- When identifying follow-ups, improvements, or missing work:
  - Create a GitHub issue, or update an existing one.  
  - Assign a priority label:  
    - `P0` – urgent / blocking  
    - `P1` – important  
    - `P2` – nice-to-have / later  
    - `P3` – low priority / backlog  
- Link related issues in pull requests.

## Pull Requests and Branch Policy
- **Never push directly to `main`.**  
- All changes must go through a pull request (PR).  
- Ensure that **all CI and PR checks pass** before merging.  
- Auto-merge is allowed **only** after every required action is green.  
- PRs must be small, focused, and linked to at least one issue when relevant.  
- Include a short summary describing purpose and impact.  
- Use `feat/`, `fix/`, or `chore/` prefixes in branch names and commit titles.

## Testing
- Always write tests:
  - **Unit tests** for individual functions and modules.  
  - **Integration tests** for multi-component flows, ingestion pipelines, or APIs.  
- Maintain or improve overall test coverage.  
- Prefer deterministic tests; isolate or mock any external I/O.  
- New features without tests are considered incomplete.


## UI and Frontend
- Reuse shared components before creating new ones.  
- Keep UI consistent with the design system or shared library.  
- Frontend logic handles presentation and local state; backend/shared utils handle correctness and filtering.
- You're highly encouaged to use vercel v0 MCP for frontend development.

---

## Summary Workflow
1. Read the wiki before making any changes.  
2. Work in a feature branch, **never in `main`**.  
3. Make the change following the style and scope rules.  
4. Add or update tests.  
5. Update the wiki if needed.  
6. Open a pull request and ensure all PR actions succeed.  
7. Auto-merge only after everything is green.  
8. Create or update related GitHub issues and tag priorities.  
9. Keep observability and ownership in mind.
