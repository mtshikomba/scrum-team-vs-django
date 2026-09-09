# Ticket: Add Top Navigation to Action Pages

## User Story

As a client, I want the top navigation to remain visible and consistent while I create, edit, or delete projects and tasks so that I can always identify the workspace, sign out, and orient myself without relying on browser navigation.

## Context

The project and task list/detail pages render the shared `topbar` with the Client tasks brand and sign-out control. The related create, edit, and delete pages instead render centered `auth-page` panels without that navigation. This makes action flows visually inconsistent and removes the persistent workspace navigation exactly when a client is making a change.

## Scope

- Add the shared top navigation to project create, project edit, project delete confirmation, task create, task edit, and task delete confirmation pages.
- Preserve the existing action-page content, forms, confirmation copy, cancel/back links, CSRF protection, validation behavior, and destructive-action styling.
- Use the same Client tasks brand link and sign-out control as the project and task list/detail pages.
- Keep the action-page panel readable and centered within the existing page shell at desktop and mobile widths.
- Ensure navigation and action controls remain keyboard reachable, visually consistent, and free of overlap or horizontal overflow.
- Decide and document whether profile and password-change pages should also adopt the same navigation in this ticket; do not change their behavior without explicitly including them in the implementation scope.
- Add focused rendering/template tests for navigation presence across all included action-page states.
- Validate the updated flows in a browser at desktop and mobile widths.

## Acceptance Criteria

- [x] Project create and edit pages render the shared top navigation with the Client tasks brand and sign-out control.
- [x] Project delete confirmation renders the shared top navigation while preserving the keep-project and delete actions.
- [x] Task create and edit pages render the shared top navigation with the Client tasks brand and sign-out control.
- [x] Task delete confirmation renders the shared top navigation while preserving the cancel and delete actions.
- [x] Navigation markup, labels, destinations, sign-out method, and visual treatment match the existing project/task list and detail pages.
- [x] Existing forms, validation errors, CSRF protection, cancel/back links, confirmation messaging, authorization boundaries, and redirects continue to work.
- [x] Action-page layouts remain centered and readable on desktop and mobile, with no clipping, overlap, or horizontal page overflow.
- [x] Keyboard navigation reaches the brand link, sign-out control, form controls, cancel links, and submit buttons in a logical order with visible focus.
- [x] Focused tests cover each included create, edit, and delete page family and confirm that unauthorized users cannot use the pages.
- [x] Browser validation passes at desktop and mobile widths for populated forms, validation-error state where applicable, and delete confirmation state.
- [x] No models, migrations, project/task data contracts, or unrelated landing/detail-page behavior are changed.

## Out of Scope

- Redesigning the topbar, brand, sign-out behavior, or action-page form styling beyond the layout integration required for consistent navigation.
- Adding new project or task actions, filters, sorting, or workflow behavior.
- Changing authorization, CSRF handling, form fields, redirects, models, migrations, or database contracts.
- Changing profile or password-change pages unless the implementation scope is explicitly expanded after review.
- Changing authentication, registration, landing-page, project-list, project-detail, task-list, or task-detail behavior unrelated to navigation consistency.

## Implementation Notes

- Reuse the existing topbar markup and `page-shell` pattern from `client_landing.html`, `project_list.html`, or `task_detail.html`.
- Inspect `project_form.html`, `project_confirm_delete.html`, `task_form.html`, and `task_confirm_delete.html` before editing.
- Preserve the existing centered panel treatment by placing it within the shared page shell rather than duplicating navigation markup inconsistently.
- Use branch `task-015-add-top-navigation-to-action-pages`.
- Pull request title: `[task-015] Add top navigation to action pages`.
- Run `@ux-developer` specification and browser validation before `@tech-lead` review.

## UX Specification

### Primary Flow

1. A signed-in client opens a project or task create, edit, or delete action page.
2. The client sees the same Client tasks brand and sign-out control used across workspace pages.
3. The client completes the form or reviews the destructive-action confirmation.
4. The client submits the action or uses the existing back/keep/cancel link to return to the relevant workspace context.

### Navigation Contract

- Use one shared topbar structure matching the existing project list/detail and task detail pages.
- Keep the Client tasks brand link pointed to the client workspace landing page.
- Keep sign out as the existing POST form with CSRF protection and the existing `Sign out` label.
- Place the topbar at the top of the shared page shell, above the centered action panel; do not place navigation inside the form panel.
- Keep the current action-page eyebrow, heading, form fields, confirmation copy, destructive styling, and back/keep links unchanged except for layout integration.

### Required Page States

- Project create form, including a validation-error render.
- Project edit form with existing project values.
- Project delete confirmation with the project name and task-removal warning.
- Task create form, including project selection and rich-text editor where present.
- Task edit form with existing task values.
- Task delete confirmation with the task name and irreversible-action warning.
- Authorized and unauthorized access behavior for each included page family.
- Profile and password-change pages remain unchanged and are explicitly outside this ticket.

### Layout and Responsive Behavior

- Desktop action pages retain a centered, readable form/confirmation panel below the full-width page-shell topbar.
- Mobile action pages keep the topbar visible without clipping the brand or sign-out control; the action panel uses the existing mobile padding and fits the viewport.
- Preserve the current 420px confirmation-panel and 560px form-panel reading widths unless a minimal adjustment is required to accommodate the shared shell.
- Keep long project/task names, validation messages, and field help text wrapped within the panel.
- Ensure action buttons, back links, editor controls, and navigation do not overlap or create horizontal page overflow.

### Accessibility and Interaction

- Preserve the semantic `header` landmark and add the existing topbar consistently to every included action page.
- Keyboard order should be: brand link, sign-out control, contextual back/keep link, form controls, then the primary or destructive submit action.
- Preserve visible focus indicators and ensure focus remains visible after validation errors or responsive reflow.
- Keep navigation and action labels descriptive and consistent with existing workspace pages.
- Preserve CSRF-protected sign-out and action forms; do not replace POST actions with links.
- Ensure error messages remain adjacent to their fields and do not push the submit action off-screen without usable scrolling.

### Browser Validation Handoff

- Desktop: validate one form page and one delete confirmation at 1440px wide; confirm the topbar aligns with the page shell and the panel remains centered.
- Intermediate: validate at approximately 900px wide; confirm the topbar, form fields, validation messages, and action buttons remain readable.
- Mobile: validate at 390px wide; confirm persistent navigation, wrapped content, visible focus, and no horizontal overflow.
- Exercise one create/edit validation-error state and one delete confirmation state for both project and task flows where practical.
- Verify that sign out, back/keep/cancel links, and submit controls remain reachable and retain their existing destinations and methods.

## Approval

Status: Completed and merged in PR #14.
