# Ticket: Prefill Project on Task Creation

## User Story

As a client working inside a project, I want **New task** to associate the task with that project automatically so I can start entering task details without selecting the project again, while keeping project selection available when I edit an existing task.

## Context

The project detail page currently links **New task** to the generic task-create route. The create view renders the full accessible-project selector, even when the client started from a specific project. This adds unnecessary choice and makes it easier to create a task in the wrong project.

The task edit flow should remain flexible: when editing an existing task, the client must still be able to change its project among projects they are allowed to access, subject to existing authorization and validation rules.

## Scope

- Make the project detail **New task** action carry the current project context into task creation.
- Use the project context to preselect and lock the project on the create form, or otherwise make the project association explicit without requiring a second selection.
- Preserve the generic task-create flow for workspace-level creation, where a client may still need to choose from accessible projects.
- Keep the project selector available and editable in the existing task edit UI.
- Refresh the Create Task and Edit Task form UI/UX together so both flows share the same task-form shell, field rhythm, action hierarchy, and responsive behavior.
- Make the project association state explicit in both modes: contextual/locked project on create and clearly editable project control on edit.
- Keep rich-text description controls, validation messages, help text, and action buttons visually contained and consistent across create/edit.
- Validate the project context server-side; do not trust a client-submitted project ID or allow access to another client’s project.
- Preserve collaborator permissions: accepted collaborators may create tasks in projects they can access, while project ownership/task authorization boundaries remain intact.
- Keep existing task fields, rich-text sanitization, status/priority defaults, redirects, CSRF protection, and validation behavior.
- Add focused tests for project-scoped create, generic create, edit project selection, invalid/unauthorized project context, and collaborator access.
- Validate the project-scoped create and edit flows in a browser at desktop and mobile widths.

## Acceptance Criteria

- [x] Clicking **New task** from a project detail page opens task creation with that project already associated.
- [x] The project-scoped create form does not require the user to select the same project again and clearly identifies the target project.
- [x] Submitting a project-scoped create request persists the task in the originating project even if a different project ID is posted or the project context is tampered with.
- [x] A project-scoped create URL cannot be used to create a task in another client’s project; unauthorized or invalid project context fails safely.
- [x] The generic workspace-level **New task** flow remains available and continues to require a valid accessible project selection when no project context is supplied.
- [x] Editing an existing task continues to show an editable project selector containing only projects the current user may use.
- [x] Changing a task’s project through the edit UI remains supported and server-validated.
- [x] Create Task and Edit Task use a consistent branded layout, heading hierarchy, spacing, field labels, help/error treatment, and submit/back navigation.
- [x] The create form clearly identifies whether it is project-scoped or generic; the edit form clearly identifies the current project and keeps it editable.
- [x] Rich-text description/editor controls, status/priority/due-date fields, validation errors, and action buttons remain readable without clipping or overlap in both modes.
- [x] Task create/edit forms preserve logical keyboard order, visible focus, accessible labels, and usable error recovery.
- [x] Accepted collaborators can create a task from their accessible project detail page, while non-members cannot use that project context.
- [x] Existing task fields, rich descriptions, status, priority, due date, CSRF protection, authorization, and success redirects remain unchanged.
- [x] Focused tests cover project-scoped creation, generic creation, tampered/unauthorized project context, edit project changes, collaborator creation, and existing task boundaries.
- [x] Browser validation passes at 1440px, 900px, and 390px for project-scoped create, generic create, validation errors, and task edit.
- [x] No model or migration change is introduced unless implementation evidence shows it is required.

## Out of Scope

- Removing project selection from the task edit UI.
- Treating Create Task and Edit Task as separate visual experiences with inconsistent layout or interaction patterns.
- Changing project ownership, collaborator permissions, task statuses, task lanes/List view, or project/task navigation beyond the create-link context.
- Adding new task fields, task templates, bulk creation, or project switching after a task is created.
- Changing task detail, project CRUD, authentication, profile, invitation, or public landing behavior.

## Implementation Notes

- Start from the project detail **New task** URL, `ClientTaskCreateView`, `ClientTaskUpdateView`, `TaskForm`, and `task_form.html`.
- Prefer an explicit project context parameter or nested route, but validate it against `accessible_projects(request.user)` server-side.
- Separate create and update form behavior so project locking applies only to project-scoped creation; the edit form must retain its project field.
- Use scoped task-form styles/components so create and edit stay visually synchronized without destabilizing project, collaboration, or authentication forms.
- Include browser checks for both create and edit at 1440px, 900px, and 390px, including validation errors and rich-text editor rendering.
- Preserve the generic `/tasks/new/` route for workspace-level creation.
- Use branch `task-021-prefill-project-on-task-create`.
- Pull request title: `[task-021] Prefill project on task creation`.
- Run `@ux-developer` specification and browser validation before `@tech-lead` review.

## UX Specification

### Primary Flows

#### Project-Scoped Create

1. A client opens a project and chooses **New task**.
2. The task form identifies the originating project near the heading and does not ask the client to choose it again.
3. The client completes task details and submits; the task remains associated with that project.

#### Generic Create and Edit

1. A client opens the workspace-level **New task** flow and sees an accessible project selector because no project context is supplied.
2. A client opens **Edit task** and sees the current project selected in an editable project selector.
3. The client can change the project, review validation errors, and save without losing entered non-sensitive values.

### Shared Task Form UX

- Use one consistent task-form shell for Create Task and Edit Task: same topbar, back-link placement, eyebrow, heading scale, form width, field spacing, help text, error treatment, and primary action placement.
- Use explicit mode copy: **Create a task** for creation and **Edit task** for updates; show the project name/context clearly in both modes.
- In project-scoped create, present the project as a read-only/contextual summary or disabled control with an accessible explanation; do not make the locked association look like a broken field.
- In generic create and edit, keep the project selector visible, labeled, keyboard accessible, and visually consistent with the other form fields.
- Keep rich-text description/editor controls inside the same readable form width with sufficient vertical space, no clipping, and clear relationship to its label/help/error text.
- Keep status, priority, due date, and title fields in a predictable scan order; preserve server-rendered errors adjacent to their fields.
- Keep the primary submit action full-width or clearly dominant, with a stable position after the form; preserve the existing back navigation.

### Required States

- Project-scoped create with locked/contextual project.
- Generic create with editable project selector.
- Edit task with current project selected and editable.
- Project-scoped invalid/unauthorized context.
- Generic create validation error.
- Edit validation error after a project change attempt.
- Rich-text editor loading/rendered state and long description wrapping.
- Long project/task names, missing due date, and mobile narrow layout.

### Accessibility and Interaction

- Use visible labels and associated help/error content for every task field, including the project context summary or selector.
- Preserve logical keyboard order from contextual back link through project/details fields to submit; locked project context must not create a misleading focus stop.
- Maintain visible focus states for selector, inputs, editor controls, and submit action.
- Ensure validation errors are announced/associated without moving focus unpredictably or overlapping fields.
- Preserve CSRF protection, password/session behavior, and server-side project authorization; client-side disabled/read-only presentation must never be the security boundary.
- Keep create/edit action labels and project association understandable to screen-reader and keyboard users.

### Responsive Behavior and Spacing

- Desktop at 1440px: keep the shared form panel centered and readable, with project context and editor controls aligned to the form rhythm.
- Intermediate at 900px: preserve field grouping, editor width, and action placement without awkward empty space or wrapping collisions.
- Mobile at 390px: fit the form panel to the viewport, stack controls cleanly, keep the project context readable, and prevent horizontal overflow.
- Create and edit must use the same panel padding, field gaps, error spacing, and submit-button dimensions at each breakpoint.

### Browser Validation Handoff

- Validate project-scoped create, generic create, and edit at 1440px, 900px, and 390px.
- Exercise project context display/lock, editable project selection on edit, validation errors, rich-text editor rendering, keyboard traversal, and responsive overflow.
- Verify a tampered project context is rejected server-side and that the UI does not claim success for an unauthorized project.

## Approval

Status: Implemented and validated; UX review passed, ready for technical review.

## UX Review

Status: PASS.

Browser validation confirmed project-scoped New task opens with the project identified and locked, Edit task retains an editable project selector, both flows share the task form shell, and the rich-text editor remains within the form at 390px without horizontal overflow. Full Django and quality checks passed.
