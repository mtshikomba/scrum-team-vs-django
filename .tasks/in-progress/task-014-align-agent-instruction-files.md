# Ticket: Align Agent Instruction Files

## User Story

As a contributor or coding agent, I want `AGENTS.md` and the repository instruction files to have a clear, consistent source of truth so that the project workflow, coding standards, and task lifecycle rules are applied predictably regardless of which instruction file is loaded.

## Context

The workspace now contains `AGENTS.md` with the full Django engineering workflow. The root `copilot-instructions.md` and `.github/copilot-instructions.md` delegate to `AGENTS.md`, while the repository has historically documented overlapping agent, UX, quality, and ticket-lifecycle rules in instruction files and `README.md`. This needs to be made deliberate and internally consistent so agents do not receive conflicting or incomplete guidance.

## Scope

- Decide and document the canonical source of repository agent instructions.
- Align `AGENTS.md`, root `copilot-instructions.md`, and `.github/copilot-instructions.md` so their delegation, precedence, and discovery behavior are clear.
- Reconcile overlapping workflow rules across the instruction files, including agent responsibilities, approval gates, UX review, ticket lifecycle, branch/PR naming, and Definition of Done.
- Preserve the existing product-owner, UX-developer, developer, and tech-lead workflow unless an explicit documentation correction is required.
- Update `README.md` only where its workflow or setup guidance becomes inaccurate after the instruction-file alignment.
- Keep the documentation ASCII-compatible where practical and preserve concise, actionable instructions.
- Verify that exactly one canonical task-014 ticket exists in the lifecycle folders.

## Acceptance Criteria

- [x] The repository has one clearly identified canonical instruction source, and the relationship between `AGENTS.md`, root `copilot-instructions.md`, and `.github/copilot-instructions.md` is documented.
- [x] Instruction discovery and precedence are unambiguous for agents operating from the repository root and from GitHub-related contexts.
- [x] Agent responsibilities and guardrails are consistent across the applicable instruction files, including the product-owner restriction to documentation/ticket work and the UX-developer boundary around backend/domain changes.
- [x] The documented workflow consistently places product approval, UX specification, implementation, UX/browser validation, technical review, and merge in the intended order.
- [x] Ticket lifecycle, canonical-copy, branch naming, PR naming, and merge requirements are consistent and do not introduce duplicate or contradictory rules.
- [x] Definition-of-Done requirements are consistent, including tests, Django checks, formatting/linting, migrations when applicable, and responsive browser validation for user-facing work.
- [x] `README.md` and the instruction hierarchy do not contain stale references to superseded filenames, agents, commands, or workflow stages.
- [x] Documentation-only validation passes: links and referenced paths are checked, Markdown structure is readable, and no application/runtime files, models, migrations, or data contracts are changed.
- [x] The final diff is limited to the agreed instruction/documentation files and the task-014 ticket.

## Out of Scope

- Changing Django models, views, forms, URLs, templates, CSS, migrations, or runtime behavior.
- Creating executable VS Code agents, prompts, skills, or external integrations.
- Changing the responsibilities of the product owner, UX developer, developer, or tech lead beyond clarifying their documentation.
- Resolving unrelated dirty-worktree changes or deciding ownership of existing untracked workspace configuration.
- Reworking the product documentation beyond instruction-file alignment and directly affected workflow references.

## Implementation Notes

- Inspect the current contents and repository tracking state of `AGENTS.md`, `copilot-instructions.md`, `.github/copilot-instructions.md`, and `README.md` before editing.
- Preserve one canonical ticket copy and verify its lifecycle path after each move.
- Use branch `task-014/align-agent-instruction-files`.
- Pull request title: `[task-014] Align agent instruction files`.
- This is a documentation-only change; no UX browser review or database migration is expected unless the implementation adds user-facing documentation changes that require it.
- Run documentation-focused validation plus the existing repository checks appropriate to changed files before technical review.

## Approval

Status: Implemented and validated; ready for technical review.
