# Ticket: Document Agent Workflow in README

## User Story

As a developer adopting this project workflow, I want the README to explain how to use the `@product-owner`, `@developer`, and `@tech-lead` agents so that I can move work from an idea to reviewed, mergeable code consistently.

## Context

The project uses three specialized agents with distinct responsibilities. The README needs to be the accessible onboarding reference for users applying the same workflow in their own project.

## Scope

- Document the responsibility and expected handoff for each agent.
- Explain the complete workflow from feature request and ticket grooming through implementation, pull request review, and merge.
- Document the human approval/refinement gate between grooming and implementation.
- Document the `.tasks/todo/`, `.tasks/in-progress/`, and `.tasks/done/` lifecycle.
- Document ticket, feature branch, and pull request naming conventions.
- Document the Definition of Done and required validation commands.
- Include concise, copyable example prompts for grooming, implementation, pull request creation, and technical review.
- Preserve the existing Django setup, authentication, run, and test instructions.

## Acceptance Criteria

- [x] The README explains that `@product-owner` creates groomed tickets with user stories, scope, acceptance criteria, and implementation notes.
- [x] The README explains that a human must approve or refine a ticket before implementation.
- [x] The README explains that `@developer` implements approved tickets, writes tests, validates the work, and prepares the pull request.
- [x] The README explains that `@tech-lead` reviews code and double-checks security, authorization, performance, migrations, tests, and acceptance criteria before merge.
- [x] The README documents the ticket lifecycle from `.tasks/todo/` to `.tasks/in-progress/` to `.tasks/done/`.
- [x] The README documents `task-NNN` IDs, branch naming, pull request title/body conventions, and examples.
- [x] The README documents the Definition of Done, including tests, `manage.py check`, migration checks, Black, Flake8, docstrings, and migrations when models change.
- [x] The README includes usable example prompts for all three agents and the main workflow stages.
- [x] Existing Django setup and usage instructions remain available and accurate.
- [x] The documentation is clear to a developer applying this workflow in another project.

## Out of Scope

- Changing agent instruction files or agent behavior.
- Adding CI/CD automation or external project-management integrations.
- Changing Django application behavior.

## Implementation Notes

- Update only `README.md` unless a documentation link requires a minimal related change.
- Use branch `task-006/document-agent-workflow-in-readme`.
- Pull request title: `[task-006] Document agent workflow in README`.

## Approval

Status: Implemented and validated.

Validation: README content reviewed against all acceptance criteria; existing Django setup and usage instructions remain present.