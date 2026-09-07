# Ticket: Client Task Management Landing Page

## User Story

As a client user, I want a clear landing page for the task management project so that I can quickly understand my current work, review task progress, and take the next relevant action.

## Scope

- Create a client-facing landing page as the authenticated entry point for client users.
- Present a concise welcome/context area without marketing-style content.
- Show the client's task summary, including outstanding, in-progress, and completed work.
- Display the client's task list with title, status, priority, due date, and last updated information where available.
- Provide a clear primary action to open or create a task according to the approved task workflow.
- Add useful empty, loading, and error states for the task summary and task list.
- Make the page usable on desktop and mobile screen sizes.
- Add navigation to the relevant task-management views and a visible sign-out action.

## Acceptance Criteria

- [ ] An authenticated client user is directed to the client landing page after sign-in or when visiting the client home route.
- [ ] Unauthenticated users cannot access the client landing page and are redirected to the configured sign-in flow.
- [ ] The page clearly identifies the client context and provides a task summary for the current user or organization.
- [ ] The task list displays task title and status, and displays priority, due date, and last updated values when those fields exist.
- [ ] Task data is scoped to the authenticated client; a client cannot view another client's tasks by changing a URL, query parameter, or request payload.
- [ ] The primary task action routes to the correct create or task-detail workflow and preserves the authenticated client context.
- [ ] Empty, loading, and recoverable error states are rendered without exposing sensitive data or stack traces.
- [ ] The layout is responsive and remains usable at mobile and desktop viewport sizes without overlapping or clipped content.
- [ ] The page includes navigation to the task-management area and a working sign-out action.
- [ ] Django views remain thin, use the existing authentication and permission patterns, and query task data through the Django ORM.
- [ ] Tests cover authenticated access, unauthenticated access, client data isolation, task summary/list rendering, and the empty state.
- [ ] Formatting, linting, and the relevant Django test suite pass.

## Out of Scope

- Full task creation, editing, assignment, commenting, or file-upload workflows unless required by the existing task-management design.
- Billing, reporting, administrative dashboards, or internal staff workflows.
- Production deployment, external analytics, and third-party integrations.

## Implementation Notes

- Confirm the existing user, organization/client, and task domain models before implementation.
- Reuse the project’s existing authentication, permission, URL, and frontend conventions rather than introducing a parallel access model.
- Define the landing page route and template/component boundary during technical review.
- The ticket should be implemented on branch `task-002/client-task-management-landing-page` with pull request title `[task-002] Add client task management landing page`.

## Approval

Status: Awaiting human approval.

Reply with **Approve** to move this ticket to `.tasks/in-progress/` for implementation, or **Refine** with changes to the scope or acceptance criteria.