# Ticket: Add Client Profile Management

## User Story

As a logged-in client, I want to update my personal profile details so that my account information stays current while my client authorization remains protected.

## Context

Clients can register, sign in, and manage project tasks, but the workspace does not provide a profile-management flow. The profile feature must use the existing Django user/authentication model and must not allow clients to alter authorization or administrative fields.

## Scope

- Add an authenticated client profile page reachable from the client workspace.
- Allow clients to update approved personal fields, such as first name, last name, email, and password through Django-supported forms.
- Validate submitted profile and password data with server-side Django forms.
- Preserve the user’s username, `Client` group membership, staff status, superuser status, permissions, and account ownership.
- Require the current password before changing the password, if password updates are included in the same flow.
- Protect profile updates with CSRF and prevent partial updates on invalid submissions.
- Redirect successfully saved changes back to the profile or client workspace with clear success feedback.
- Add tests for access control, valid updates, invalid input, password behavior, and privilege-boundary resistance.

## Acceptance Criteria

- [x] An authenticated user in the `Client` group can open the profile page from the client workspace.
- [x] Anonymous users are redirected to the configured login flow.
- [x] Authenticated non-client and staff users cannot access the client profile route unless explicitly assigned to the `Client` group.
- [x] Clients can update approved personal fields and see persisted values after a successful save.
- [x] Invalid profile input is handled by Django form validation without partial updates.
- [x] Password changes use Django's supported `PasswordChangeForm` and require the current password.
- [x] A successful password change invalidates old credentials and accepts the new credentials.
- [x] Username, `Client` group membership, staff status, superuser status, permissions, and ownership cannot be changed through the profile form.
- [x] Profile updates are CSRF-protected and do not expose passwords or sensitive data.
- [x] Tests cover authorization, valid updates, password behavior, and privilege-boundary resistance.
- [x] Django tests, system checks, migration checks, Black, and Flake8 pass.
- [x] The client workspace provides navigation to the profile page and back to project/task work.

## Out of Scope

- Email verification, avatar uploads, social login, multi-factor authentication, or external identity providers.
- Staff/admin profile management.
- Account deletion, organization membership changes, billing details, or notification preferences.

## Implementation Notes

- Reuse the existing Django `User`, `ClientAccessMixin`, authentication routes, and workspace styling.
- Prefer `UserChangeForm`, `PasswordChangeForm`, or dedicated restricted forms over manual request parsing.
- Keep authorization fields out of form definitions entirely.
- Use branch `task-010-client-profile-management`.
- Pull request title: `[task-010] Add client profile management`.

## Approval

Status: Implemented and validated.

Validation: 30 Django tests passed; system checks, migration checks, Black, Flake8, and mobile browser verification passed.