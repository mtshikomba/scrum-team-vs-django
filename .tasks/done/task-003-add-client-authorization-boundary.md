# Ticket: Add Client Authorization Boundary

## User Story

As a task management system, we want an explicit client authorization boundary so that only users identified as clients can access client-facing task workflows, while staff and other authenticated accounts are denied or routed to their appropriate experience.

## Context

The client landing page currently uses authentication as its only access control. The project does not yet define how a user is identified as a client, so any authenticated account can reach the client-facing route. This ticket addresses the authorization gap identified during the `task-002` technical review.

## Scope

- Choose and document the project’s client authorization mechanism, using Django’s existing user, group, or permission model unless a domain-specific model is justified.
- Apply the client authorization boundary to the client landing page and all existing client-facing task routes.
- Define the expected behavior for authenticated users who are not clients, such as a `403` response or redirect to an appropriate route.
- Preserve client task isolation so an authorized client can access only its own tasks.
- Update setup or seed guidance so a developer can create a valid client user locally.
- Add focused tests for authorized clients, anonymous users, authenticated non-clients, and cross-client task access.

## Acceptance Criteria

- [x] The Django `Client` group is the documented source of truth for client authorization.
- [x] An authorized client can access the client landing page.
- [x] An authenticated user without client authorization receives `403` for the client landing page.
- [x] Anonymous users continue to follow the configured sign-in flow.
- [x] Client task queries remain scoped to the authorized client.
- [x] Staff status alone does not grant client access, and this behavior is tested and documented.
- [x] Tests cover authorized access, unauthorized authenticated access, anonymous access, staff access, and client data isolation.
- [x] The implementation uses Django authentication primitives consistently and keeps views thin.
- [x] No model changes were required; migration checks pass with no changes detected.
- [x] Django tests, system checks, migration checks, Black, and Flake8 pass.
- [x] README setup guidance explains how to create or assign a client user locally.

## Out of Scope

- Building a separate staff dashboard or administrative authorization experience.
- Replacing the project’s authentication backend.
- Implementing task creation, editing, assignment, or detail workflows beyond protecting routes that already exist.
- Production identity-provider integration.

## Implementation Notes

- Review the existing `Task.client` relationship and current user model before choosing the authorization source of truth.
- Prefer a Django Group or Permission when it expresses the policy without introducing unnecessary schema complexity.
- Preserve the existing task-002 branch/PR history; implement this follow-up on branch `task-003-add-client-authorization-boundary`.
- Pull request title: `[task-003] Add client authorization boundary`.

## Approval

Status: Implemented and validated.

Validation: 6 Django tests passed; system checks, migration checks, Black, and Flake8 passed.