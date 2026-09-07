# Ticket: Add Client Registration Page

## User Story

As a prospective client, I want to register through a client-facing sign-up page so that I can create my account and access my task management workspace without staff intervention.

## Context

The project now protects client-facing routes with membership in the Django `Client` group, but there is no self-service account creation flow. Registration must create a regular user and assign client access without allowing a registrant to grant themselves staff or administrative privileges.

## Scope

- Add a public client registration page reachable from the sign-in experience.
- Collect the minimum identity and credential fields required by the existing Django user model.
- Validate required fields, password confirmation, password strength, and duplicate identity values.
- Create the user using Django’s supported password hashing and validation APIs.
- Assign every successfully registered user to the existing `Client` group.
- Keep new users as regular, non-staff, non-superuser accounts.
- Redirect a successful registration to the client sign-in or landing flow according to the project’s authentication convention.
- Provide clear recoverable validation errors without exposing sensitive data.
- Add tests for successful registration, invalid input, duplicate identity, client-group assignment, and privilege boundaries.

## Acceptance Criteria

- [x] Anonymous users can open the registration page from the sign-in experience.
- [x] The registration form includes username, email, and password fields without staff, superuser, group, or permission inputs.
- [x] Invalid submissions re-render the form with useful field-level errors and do not create a partial user.
- [x] Password confirmation and Django password validation are enforced.
- [x] Duplicate usernames are rejected without creating another user.
- [x] A successful registration creates exactly one user with a securely hashed password.
- [x] A successful registration assigns the user to the existing `Client` group.
- [x] A registered user cannot set `is_staff`, `is_superuser`, permissions, or other elevated access through form data.
- [x] Successful registration redirects to the sign-in flow and does not automatically bypass authentication.
- [x] Registration uses CSRF protection, Django forms/authentication primitives, and a thin view.
- [x] Tests cover successful registration, invalid input, duplicate identity, client-group assignment, and privilege boundaries.
- [x] Django tests, system checks, migration checks, Black, and Flake8 pass.

## Out of Scope

- Email verification, password reset, social login, multi-factor authentication, or external identity-provider integration.
- Staff/admin registration or invitation workflows.
- Organization creation, billing, onboarding questionnaires, or task creation during registration.

## Implementation Notes

- Reuse the existing Django `User` model and `Client` group established by `task-003` unless technical review identifies a concrete need for a custom user model.
- Prefer a dedicated Django `Form` or `UserCreationForm` over manual request parsing.
- Preserve the existing login and client landing routes, and ensure a registered user can complete the full sign-in flow.
- Implement on branch `task-004-client-registration-page`.
- Pull request title: `[task-004] Add client registration page`.

## Approval

Status: Implemented and validated.

Validation: 11 Django tests passed; system checks, migration checks, Black, Flake8, and mobile browser verification passed.