# Ticket: Fix Anonymous Task Creation Access

## User Story

As an anonymous visitor, I want protected task-creation routes to redirect me to sign in instead of raising an application error so that unauthorized access follows the normal authentication flow.

## Context

The task-007 tech-lead review found that `ClientTaskCreateView.dispatch()` checks for projects before `LoginRequiredMixin` authenticates the request. An anonymous request to `/tasks/new/` can therefore query projects with `AnonymousUser` and raise an exception instead of returning the configured login redirect.

## Scope

- Correct the dispatch/authentication ordering in the client task-creation view.
- Ensure the project-existence redirect runs only after the user has passed authentication and client authorization.
- Preserve the project-first behavior for authenticated clients with no projects.
- Add regression coverage for anonymous, authenticated non-client, authenticated client-without-project, and authenticated client-with-project access.
- Update the task-007 implementation/PR with the fix and validation evidence.

## Acceptance Criteria

- [x] An anonymous `GET /tasks/new/` returns a `302` redirect to `/accounts/login/?next=/tasks/new/` and does not raise an exception.
- [x] An authenticated non-client cannot use `/tasks/new/` and receives the configured authorization response.
- [x] An authenticated client with no projects is redirected to `/projects/new/`.
- [x] An authenticated client with at least one project can access the task form normally.
- [x] The fix does not weaken client-group authorization or project/task ownership isolation.
- [x] Regression tests cover the original anonymous-request failure and the project-first branches.
- [x] Django tests, system checks, migration checks, Black, and Flake8 pass.
- [x] The correction is isolated to task-007 behavior and ready for re-review.

## Out of Scope

- Changes to project/task data models or migrations.
- New task-management features or changes to the project-first product workflow.
- Changes to authentication backends or login policy.

## Implementation Notes

- Prefer letting `LoginRequiredMixin` and `UserPassesTestMixin` run before checking project existence, or guard the custom dispatch with `request.user.is_authenticated`.
- Preserve the existing `task-007-project-scoped-task-management` branch/PR context if the repository workflow allows a direct correction; otherwise use branch `task-008-fix-anonymous-task-access` and link it to task-007.
- Pull request title when implemented separately: `[task-008] Fix anonymous task creation access`.

## Approval

Status: Implemented and validated.

Validation: 25 Django tests passed; system checks, migration checks, Black, and Flake8 passed.