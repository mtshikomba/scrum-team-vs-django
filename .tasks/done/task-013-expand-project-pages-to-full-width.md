# Ticket: Expand Project Pages to Full Width

## User Story

As a client, I want the projects index and project detail pages to use the available workspace width so that these pages feel consistent with the rest of the client workspace and are easier to scan.

## Context

The project index (`/projects/`) and project detail page (`/projects/6/`) share the `detail-panel` layout. That panel is capped at 760px even though the surrounding `page-shell` supports a wider workspace. The resulting narrow column leaves excessive unused space on desktop and makes project pages inconsistent with the client landing page and other wide task-oriented views.

## Scope

- Update the shared project-page layout so the projects index and project detail content uses the available `page-shell` width on desktop.
- Preserve the existing visual hierarchy, spacing language, controls, project cards, task table, and empty states.
- Keep the layout responsive at mobile widths, including readable project cards, action controls, and task rows without horizontal overflow.
- Cover both the populated projects state and the no-projects state, plus a project detail page with and without tasks.
- Add or update focused template/style tests as appropriate to prevent regression of the intended layout hooks and page rendering.
- Validate the rendered pages in a browser at desktop and mobile viewport widths.

## Acceptance Criteria

- [x] `/projects/` uses the available content width of the shared page shell on desktop instead of being constrained to a narrow 760px column.
- [x] `/projects/6/` uses the same full-width project layout treatment as `/projects/`, with its task content able to use the available desktop width.
- [x] The project pages remain visually consistent with the client workspace, including header alignment, page padding, typography, controls, cards, task table, and empty states.
- [x] Project cards use the available width without awkward stretching, and the grid remains readable at intermediate viewport widths.
- [x] At mobile widths, project pages remain usable with a single-column project grid, readable action controls, and no horizontal page overflow.
- [x] Existing project navigation and actions continue to work: back links, new project, new task, edit project, delete project, and project/task links.
- [x] Populated and empty project states render correctly after the layout change; project detail pages with and without tasks remain understandable.
- [x] Browser validation passes at a desktop viewport and a mobile viewport, including a visual check for excess unused width, clipping, overlap, and horizontal overflow.
- [x] Django tests and project quality checks pass, including `python manage.py test`, `python manage.py check`, Black, Flake8, and migration checks.
- [x] No models, migrations, authorization rules, or project/task data contracts are changed.

## Out of Scope

- Redesigning the project or task visual language.
- Adding project filtering, sorting, pagination, or new project/task actions.
- Changing project ownership, authorization, routing, models, forms, or database migrations.
- Changing unrelated authentication, profile, landing-page, or task-detail layouts.

## Implementation Notes

- Start from the shared `.detail-panel` and related responsive rules in `core/static/core/landing.css`.
- Keep the existing `.page-shell` as the alignment and maximum-width boundary unless a small template adjustment is required for consistency.
- Inspect both `core/templates/core/project_list.html` and `core/templates/core/project_detail.html` before editing.
- Use branch `task-013/expand-project-pages-to-full-width`.
- Pull request title: `[task-013] Expand project pages to full width`.
- Run `@ux-developer` specification and browser validation before `@tech-lead` review.

## UX Specification

### Primary Flow

1. A signed-in client opens **Projects** from the workspace.
2. The client scans project cards across the available desktop content width and selects a project.
3. The client reviews the project summary and task table, then uses the existing actions to create, edit, or delete project work.
4. The client uses the back link to return to the project list or workspace.

### Layout and Responsive Behavior

- Align both project pages with the full inner width of `.page-shell`; do not introduce a second desktop container narrower than the shell.
- Keep the current topbar, page padding, typography, card styling, action hierarchy, and task-table treatment unchanged except where width requires reflow.
- Keep project cards in a balanced multi-column grid on desktop and intermediate widths; collapse to one column at the existing mobile breakpoint.
- Allow project-detail actions to wrap cleanly when the available width is reduced.
- Preserve readable task-row columns on desktop and the existing two-column mobile task-row structure.
- Ensure no content, controls, status labels, or due dates clip or create horizontal page overflow.

### Required States

- Project list with multiple projects.
- Project list with no projects and its existing create-project call to action.
- Project detail with a description and multiple tasks.
- Project detail without a description.
- Project detail with no tasks and its existing create-task call to action.

### Accessibility and Interaction

- Preserve semantic headings and the existing page landmarks (`header`, `main`, and task `section`).
- Keep all project, task, navigation, and action controls keyboard reachable in a logical order.
- Preserve visible focus indicators and ensure focused links/buttons remain within the viewport after responsive reflow.
- Keep link and button labels descriptive without relying on visual position or color.
- Maintain sufficient text contrast for muted metadata, statuses, priorities, and action controls.
- Verify long project names, task titles, and descriptions wrap or truncate without overlapping adjacent content.

### Browser Validation Handoff

- Desktop: validate at 1440px wide and confirm both project pages align with the page shell, use the available width, and have no unexplained empty side region.
- Intermediate: validate around 900px wide and confirm the card grid, detail actions, and task rows remain balanced and readable.
- Mobile: validate at 390px wide and confirm one-column cards, wrapped actions, readable task content, visible focus, and no horizontal overflow.
- Test populated and empty states listed above; record any clipping, overlap, unexpected scrollbars, or broken navigation before technical review.

## Approval

Status: Completed and merged in PR #12.
