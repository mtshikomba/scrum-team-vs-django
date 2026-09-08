# Ticket: Add UX Developer Workflow

## User Story

As a team adopting this project workflow, I want a dedicated `@ux-developer` agent and UX review stage so that user-facing features are designed, accessible, responsive, and validated before technical review and merge.

## Context

The workflow recently gained a UX-focused agent responsible for translating approved requirements into user flows, interface states, responsive behavior, accessibility criteria, and browser validation. This process update must be documented consistently in the workspace instructions and README.

## Scope

- Document the `@ux-developer` role, responsibilities, and guardrails.
- Add a UX specification and validation stage between product approval, implementation, and technical review.
- Define UX acceptance criteria for user-facing tickets, including responsive behavior, accessibility, content, and relevant UI states.
- Require browser validation at desktop and mobile widths for user-facing changes.
- Add reusable prompts for UX specification and implemented-UI review.
- Update the Definition of Done and workflow diagrams/steps where applicable.
- Keep `README.md` and `copilot-instructions.md` aligned.

## Acceptance Criteria

- [x] `README.md` documents `@ux-developer` responsibilities and the handoff with `@product-owner`, `@developer`, and `@tech-lead`.
- [x] `copilot-instructions.md` documents the `@ux-developer` persona, guardrails, and `#ux-review` workflow.
- [x] The documented workflow places UX specification after product approval and UX validation before final technical review.
- [x] User-facing Definition of Done includes responsive, accessibility, and relevant UI-state validation.
- [x] UX acceptance criteria cover user flow, loading, empty, error, success, permission-denied, keyboard/focus, and overflow behavior where applicable.
- [x] Browser validation at desktop and mobile widths is explicitly required and documented.
- [x] Copyable prompts exist for defining UX before implementation and reviewing implemented UI.
- [x] Existing agent responsibilities, task lifecycle, naming conventions, approval gates, and Django Definition of Done remain intact.
- [x] Documentation diagnostics pass and no Django application/runtime files are changed.

## Out of Scope

- Creating a new executable agent configuration or external design-tool integration.
- Changing application behavior, models, views, forms, or migrations.
- Replacing the existing product-owner, developer, or tech-lead responsibilities.

## Implementation Notes

- Update only `README.md` and `copilot-instructions.md` unless a documentation link requires a minimal related change.
- Preserve the single-canonical-copy ticket lifecycle.
- Use branch `task-012-add-ux-developer-workflow`.
- Pull request title: `[task-012] Add UX developer workflow`.

## Approval

Status: Implemented and validated.

Validation: README and Copilot instructions reviewed; UX workflow terms and documentation diagnostics verified.