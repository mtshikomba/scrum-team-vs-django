# Ticket: Harden Ticket Lifecycle Workflow

## User Story

As a team using the scrum-agent workflow, I want the ticket lifecycle rules and recent cleanup to be documented and reproducible so that completed work does not leave duplicate task files or ambiguous status copies.

## Context

Recent workflow maintenance removed stale copies of completed tickets from `.tasks/in-progress/` and strengthened the README and workspace instructions. This work should be tracked as a documented process improvement so future agents follow the same single-copy lifecycle.

## Scope

- Document that a ticket must be moved, never copied, between `.tasks/todo/`, `.tasks/in-progress/`, and `.tasks/done/`.
- Require exactly one canonical copy of each ticket at any time.
- Require duplicate checks before starting or completing a ticket.
- Require source-absent and destination-present verification after every move.
- Document the cleanup of stale lifecycle copies while preserving the canonical completed tickets.
- Keep the agent responsibilities, approval gates, naming conventions, and Definition of Done aligned between `README.md` and `copilot-instructions.md`.

## Acceptance Criteria

- [x] `README.md` explicitly documents move-not-copy behavior for tickets.
- [x] `copilot-instructions.md` explicitly documents the single-canonical-copy rule.
- [x] Both documents require duplicate checks and source/destination verification after ticket moves.
- [x] `.tasks/todo/` and `.tasks/in-progress/` contain no stale copies of completed tickets.
- [x] `.tasks/done/` contains exactly one canonical copy for every completed ticket through `task-008`.
- [x] Existing agent responsibilities, task naming, approval gates, and Definition of Done remain documented.
- [x] No application code, database schema, or runtime behavior changes are introduced.
- [x] Documentation diagnostics pass and the final diff contains only intended workflow/documentation cleanup.

## Out of Scope

- Changes to Django models, views, forms, migrations, or frontend behavior.
- New agent personas, automated CI enforcement, or external project-management integrations.
- Renaming existing task IDs or rewriting completed ticket histories.

## Implementation Notes

- Preserve the current canonical tickets in `.tasks/done/`.
- Use branch `task-009-harden-ticket-lifecycle-workflow`.
- Pull request title: `[task-009] Harden ticket lifecycle workflow`.

## Approval

Status: Implemented and validated.

Validation: documentation diagnostics passed; task folders verified with one canonical copy per completed ticket.