---
applyTo: "web/**"
---

# Frontend / UI Rules (web/**)

These rules apply to all code, components, pages, and client logic under `web/`.

## UI Consistency
- Reuse shared components before creating new components.
- Keep UI consistent with the shared design system or component library.
- Do not invent new global styles, spacing tokens, or typography scale without updating the shared design system.
- Frontend code should handle presentation and local state.
- Validation, filtering, and business rules belong in backend/shared utilities.

## Styling and Components
- Do not inline random spacing, color, or typography tokens if an existing utility / class / component already expresses that choice.
- If you copy an existing component just to tweak it, promote the shared logic into a reusable component instead of leaving two near-duplicates to drift.
- Any component intended for reuse across pages must live in the shared components directory and include a short comment at the top describing intended usage.

## API Usage from Frontend
- Do not call backend services directly with hardcoded URLs in components.
- All network calls from `web/**` must go through the approved client / API wrapper layer.
- If you introduce a new backend route, document:
  - route path
  - required params
  - response shape  
  in the wiki, and link that in the PR.

## Vercel v0 MCP Usage
Use Vercel v0 MCP for frontend work in these cases:
1. Generating or modifying significant UI structure (multi-page layouts, dashboards, complex modals, tables with pagination, etc.).
2. End-to-end scaffolding that touches both the frontend (under `web/`) and an API/backend endpoint.
3. Work that affects shared UI conventions or cross-page patterns (navigation, layout shells, shared forms).
4. Time-sensitive or highly visual changes where rapid preview / iteration speed matters.
5. Prototyping new user interactions or flows that will go through design feedback.

Outside those cases, local edits or standard Copilot suggestions are acceptable.

## Pull Requests for `web/**`
Every UI change PR must include:
- What changed in the user-facing UI.
- Whether shared components or layout primitives were touched.
- Whether Vercel v0 MCP was involved in generating the structure.
- Linked issue and priority (`P0`, `P1`, etc.).

## Testing for Frontend
- New components require basic render coverage or snapshot coverage.
- Interactive flows (forms, table actions, pagination) require an integration-style test or e2e-style test stub.
- If the frontend calls a backend route, mock that route in tests instead of hitting live services.

## Ownership Notes
- Any new reusable component added under `web/` must either:
  - be documented in the shared component library / story, or
  - be explicitly marked as "local-only" to this feature in code comments.
- If a change under `web/` introduces or modifies an API contract, update the wiki section for that API and include request/response shape.

## Automated Review Feedback
- There is an automated Vercel review agent running on frontend pull requests. It may leave review comments with required changes, suggestions, or consistency notes.
- The GitHub Copilot Agent is expected to address those comments directly:
  - Apply fixes requested by the Vercel review agent (naming, props shape, missing cleanup, incorrect hook usage, layout violations, etc.).
  - Push follow-up commits to the same feature branch and update the same pull request. Do not open a new PR unless the comment explicitly asks for a larger refactor.
  - Mark each addressed Vercel comment as resolved in the PR after applying the change.
- If the Vercel review agent flags a structural/design-system issue (for example: “this layout duplicates an existing component,” “this spacing is inconsistent with the shared tokens”), Copilot Agent must refactor toward the shared component / token instead of adding yet another custom variant.
- If a Vercel review comment implies a backend/API contract change, Copilot Agent must:
  - update the relevant API wrapper/client code under `web/**`
  - and update the documented request/response shape in the wiki
  before the PR is considered mergeable.
- A pull request under `web/**` is not considered ready to merge until:
  - Vercel review agent comments are resolved,
  - Copilot Agent has applied those fixes or explicitly documented why a comment was intentionally not applied,
  - all normal merge requirements in the global instructions file are met (tests, CI green, linked issue, etc.).

