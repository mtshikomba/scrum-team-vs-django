# Ticket: Add Rich Task Descriptions

## User Story

As a client, I want each task to have a rich-text description so that I can provide context, notes, links, and structured details without relying on a plain one-line title.

## Context

Tasks currently contain only a title and workflow metadata. The task create and edit forms need a rich-text description field, and task detail views need to render that content safely without introducing stored-XSS risk.

## Scope

- Add an optional task description field to the `Task` model.
- Integrate a maintained rich-text editor appropriate for the existing Django application and document the dependency/configuration choice.
- Add the editor to task create and edit forms with an accessible fallback for users who cannot use the rich editor.
- Render task descriptions on the task detail view with an explicitly sanitized, allowed HTML subset.
- Preserve project/client ownership and authorization behavior for task descriptions.
- Add a migration that safely handles existing tasks by assigning an empty description.
- Add tests for create, edit, display, empty descriptions, validation, authorization, and unsafe HTML sanitization.

## Acceptance Criteria

- [x] `Task` has an optional description field with clear `verbose_name` and `help_text`.
- [x] Existing tasks migrate successfully with an empty description and retain all existing project/client relationships.
- [x] Authorized clients can create and edit tasks with rich-text descriptions.
- [x] Clients cannot read or modify another client’s task description through any route or crafted request.
- [x] The editor supports documented formatting controls and retains a textarea fallback through the form field.
- [x] Task detail renders the approved safe formatting subset.
- [x] Unsafe markup and executable content are removed before storage and display.
- [x] Description content is sanitized before being rendered as HTML.
- [x] Empty descriptions render a clear empty state.
- [x] Create/edit forms validate description input and preserve submitted values when other fields are invalid.
- [x] Tests cover rich-text save/display, empty descriptions, ownership isolation, and XSS sanitization.
- [x] The editor dependency and sanitization policy are documented in README setup guidance.
- [x] Django tests, system checks, migration checks, Black, and Flake8 pass.

## Out of Scope

- Real-time collaboration, comments, mentions, attachments, image uploads, version history, or revision comparison.
- Markdown support unless selected as the approved editor strategy.
- Changes to project/client authorization or task assignment workflows.

## Implementation Notes

- Select the editor and sanitization libraries during technical review; prefer maintained packages compatible with the project’s Python/Django versions.
- Keep the server-side stored value and rendered value boundaries explicit; sanitize on input and/or output according to the selected library’s guidance.
- Reuse the existing `TaskForm`, ownership-filtered task views, task detail template, and project-first workflow.
- Use branch `task-011-add-rich-task-descriptions`.
- Pull request title: `[task-011] Add rich task descriptions`.

## Approval

Status: Implemented and validated.

Validation: 32 Django tests passed; migration `core.0003_task_description` applied; system checks, migration checks, Black, Flake8, and editor/browser validation passed.