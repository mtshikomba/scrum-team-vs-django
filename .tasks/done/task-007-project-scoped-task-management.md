# Ticket: Add Project-Scoped Task Management

## User Story

As a client, I want my tasks to belong to a project so that I can organize my work in a meaningful project context and create tasks only after I have created or selected a project.

## Context

Tasks currently belong directly to a client user. The task-management workflow must become project-first: a client creates a project, selects one of their projects, and then manages tasks within that project. Project and task ownership must remain isolated between clients.

## Scope

- Add a `Project` domain model owned by a client user with the required name and description fields.
- Add project create, list, detail, edit, and delete workflows for authorized clients.
- Associate every task with exactly one project and retain the task’s client ownership boundary.
- Require a client to create or select a project before the create-task form is available.
- Limit project and task querysets to the authenticated client on every read and mutation.
- Update the landing page and navigation to show the client’s projects and project-scoped task summaries.
- Make task creation require a selected project; do not trust a hidden or submitted client/owner field.
- Define and implement a safe migration strategy for existing tasks before making the project relationship required.
- Add project and task empty, validation, not-found, forbidden, delete-confirmation, and recoverable error states.
- Update tests and documentation for the project-first workflow.

## Acceptance Criteria

- [x] An authorized client can create, view, edit, and delete only projects they own.
- [x] Project names are validated and required; invalid project submissions do not create partial records.
- [x] An authorized client cannot access or mutate another client’s project by changing a URL, primary key, query parameter, or submitted payload.
- [x] A client with no projects is directed to create a project before accessing task creation.
- [x] The create-task workflow requires selecting one of the authenticated client’s projects.
- [x] A task cannot be created without a project, and submitted owner/client/project fields cannot move ownership across clients.
- [x] Existing tasks receive a per-client `Legacy project` during migration before the project relationship becomes required.
- [x] Task list, detail, edit, delete, and summary views are scoped to the authenticated client and project relationships.
- [x] A client cannot view, edit, or delete another client’s task or project through an object identifier or crafted request.
- [x] Project and task mutations use Django forms, server-side validation, and CSRF-protected requests.
- [x] Project and task workflows remain usable on desktop and mobile layouts, including empty and error states.
- [x] Tests cover project CRUD, project ownership isolation, project-required task creation, task/project ownership isolation, migration behavior, and authorization.
- [x] `makemigrations` produces a clean migration, and Django tests, system checks, migration checks, Black, and Flake8 pass.
- [x] README documentation explains the project-first workflow for clients.

## Out of Scope

- Sharing projects between clients or assigning collaborators.
- Staff project administration, billing, reporting, comments, attachments, notifications, or real-time updates.
- Project templates, archiving, bulk task actions, search, filtering, pagination, or external integrations.

## Implementation Notes

- Reuse the existing Django `User` model and `Client` group authorization boundary.
- Prefer Django ORM relations and ownership-filtered querysets; keep views thin.
- Decide the existing-task migration strategy during technical review before implementing the required relationship.
- Use branch `task-007-project-scoped-task-management`.
- Pull request title: `[task-007] Add project-scoped task management`.

## Approval

Status: Implemented and validated.

Validation: 23 Django tests passed; project migration/backfill applied; system checks, migration checks, Black, Flake8, and desktop browser verification passed.