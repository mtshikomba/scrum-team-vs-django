# Ticket: Enable Client Task Management

## User Story

As a logged-in client, I want to create, view, update, and delete my own tasks so that I can manage the work associated with my project from the task management workspace.

## Context

The client landing page currently displays client-owned tasks, but clients cannot manage them. This ticket adds the authenticated client task workflow while preserving the `Client` group authorization boundary and strict per-user ownership checks.

## Scope

- Add authenticated client workflows to create, view, edit, and delete tasks owned by the current client.
- Reuse the existing `Task` fields and status/priority choices unless a concrete domain requirement requires a model change.
- Add task forms with server-side validation for title, status, priority, and due date.
- Provide clear navigation from the client landing page to create a task and to task detail/edit/delete actions.
- Confirm destructive deletion before the request is submitted and protect all state-changing requests with CSRF.
- Preserve the existing task summary and list while making task rows actionable.
- Provide useful empty, validation, not-found, forbidden, and recoverable error states.
- Keep the workflow scoped to authorized users in the Django `Client` group.

## Acceptance Criteria

- [x] Only authenticated users in the `Client` group can access client task management routes.
- [x] Anonymous users are redirected to the configured sign-in flow.
- [x] Authenticated non-client and staff users cannot access client task management routes unless explicitly assigned to the `Client` group.
- [x] An authorized client can create a task with valid title, status, priority, and optional due date values.
- [x] Invalid or incomplete task submissions re-render the form with field-level errors and do not create or partially update a task.
- [x] An authorized client can view and edit only tasks they own.
- [x] An authorized client cannot view, edit, or delete another client’s task by changing a URL, primary key, query parameter, or submitted payload.
- [x] An authorized client can delete an owned task only through a CSRF-protected request with an explicit confirmation step.
- [x] Task list and summary counts reflect create, update, and delete operations after successful requests.
- [x] Task detail, form, delete confirmation, empty, and not-found states are implemented with responsive layouts.
- [x] Views remain thin, use Django forms and ORM querysets, and enforce ownership server-side rather than relying on hidden form fields or UI controls.
- [x] Tests cover authorization, CRUD success paths, invalid input, CSRF-protected mutations, ownership isolation, and deletion behavior.
- [x] No model changes were required; migration checks pass with no changes detected.
- [x] Django tests, system checks, migration checks, Black, and Flake8 pass.

## Out of Scope

- Staff task management, task assignment to other users, comments, attachments, notifications, or real-time updates.
- Bulk actions, task search/filtering, pagination, recurring tasks, or external integrations.
- Email verification, password reset, and other account workflows.

## Implementation Notes

- Reuse the existing `Task` model, `Client` group authorization, landing page styles, and authentication routes.
- Prefer Django generic editing views or equivalent thin views with ownership-filtered querysets.
- Use branch `task-005-client-task-management`.
- Pull request title: `[task-005] Enable client task management`.

## Approval

Status: Implemented and validated.

Validation: 18 Django tests passed; system checks, migration checks, Black, Flake8, and desktop/mobile browser verification passed.