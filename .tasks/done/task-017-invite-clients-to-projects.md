# Ticket: Invite Clients to Collaborate on Projects

## User Story

As a project owner, I want to invite other client users to my project so that we can collaborate on the project and its related tasks without exposing the project to clients who were not invited.

## Context

Projects currently have one `client` owner, and project/task authorization is based on that single relationship. A project owner needs a controlled collaboration model that distinguishes ownership from membership, grants invited clients access only to the relevant project and tasks, and preserves owner-only control over project membership.

The invitation workflow must define how an invited client receives and accepts an invitation, how a pending invitation is represented, and what collaborators may do after joining. Existing task ownership and client authorization rules must not be broadened implicitly.

## Scope

- Add project membership/invitation behavior for existing users in the Client group.
- Allow only the project owner to invite another eligible client to a project.
- Provide a clear pending-invitation and acceptance flow for the invited client.
- Allow the project owner to view pending/active invitees and revoke an invitation or remove an active collaborator.
- Grant accepted collaborators access to the invited project and its related tasks only.
- Define and enforce collaborator permissions for viewing, creating, editing, deleting, and moving tasks; owner-only project CRUD and membership management must remain protected unless explicitly expanded.
- Prevent duplicate invitations/memberships, self-invites, invitations to non-client users, and access through guessed project/task/invitation identifiers.
- Preserve existing single-owner behavior for projects without collaborators.
- Add focused authorization, invitation lifecycle, and collaboration tests, including CSRF and cross-client boundaries.
- Include UX acceptance criteria and browser validation for owner invite management and invited-client acceptance/access states.

## Acceptance Criteria

- [x] A project owner can open a project collaboration control and invite an existing user who belongs to the `Client` group.
- [x] A non-owner collaborator cannot invite users, revoke invitations, remove collaborators, edit project details, or delete the project.
- [x] The owner cannot invite themselves, invite a non-client user, create duplicate pending invitations, or create duplicate active memberships.
- [x] An invitation has a clear pending state and can be accepted only by its intended client; accepting it creates one active project membership.
- [x] An invited client cannot view or act on the project or its tasks before accepting the invitation.
- [x] After acceptance, the collaborator can access only the invited project and its related tasks, not the owner’s other projects or another client’s projects/tasks.
- [x] Collaborator permissions are explicit and enforced consistently for task viewing, creation, editing, deletion, and status-lane moves; owner-only project and membership actions remain protected.
- [x] The project owner can see active collaborators and pending invitations and can revoke pending invitations or remove an active collaborator without deleting the project or its tasks.
- [x] Removing a collaborator immediately prevents further project/task access while preserving existing project/task records and ownership.
- [x] Invitation acceptance, revocation, removal, and task/project actions require CSRF protection where state changes occur.
- [x] Invalid, expired/revoked, already accepted, already active, or guessed invitation identifiers fail safely without leaking project or user information.
- [x] Existing owner-only project access, task ownership behavior, client-group authorization, and unrelated projects remain unchanged.
- [x] Focused tests cover invitation lifecycle, duplicate/self/non-client cases, owner/collaborator permissions, cross-project/cross-client access, removal/revocation, and CSRF protection.
- [x] Browser validation covers the owner invite flow, pending invitation, acceptance, collaborator project/task access, denied owner-only actions, and responsive desktop/mobile states.
- [x] Any new models or fields include explicit verbose names, help text, indexes/constraints where appropriate, Google-style docstrings, and clean migrations; if no schema change is required, no migration is added.

## Out of Scope

- Inviting users who do not already have a registered Client account.
- Email delivery, external notification providers, password resets, or organization/team administration.
- Sharing projects with staff, superusers, anonymous users, or users outside the Client group.
- Cross-project task assignment, task ownership transfer, multi-owner projects, comments, real-time collaboration, or activity feeds.
- Changing the existing task statuses, lane/list UI, project design language, or unrelated profile/authentication flows.
- Allowing collaborators to edit project metadata, delete projects, or manage memberships unless a later approved ticket expands their permissions.

## Implementation Notes

- Preserve `Project.client` as the immutable project owner unless implementation evidence and an approved scope update require a different ownership model.
- Prefer an explicit membership/invitation model with unique constraints and indexed project/user/status fields rather than inferring access from task ownership.
- Centralize project-access and permission checks so project detail, task CRUD, task status moves, and invitation endpoints cannot drift apart.
- Use opaque or otherwise non-guessable invitation identifiers/tokens and validate the intended authenticated recipient server-side.
- Decide the collaborator task policy before implementation and document it in the ticket: recommended default is view/create/edit/move tasks but no project CRUD or membership management.
- Inspect existing project/task views, forms, templates, tests, and URL patterns before editing.
- Use branch `task-017-invite-clients-to-projects`.
- Pull request title: `[task-017] Invite clients to collaborate on projects`.
- Run `@ux-developer` specification and browser validation before `@tech-lead` review.

## UX Specification

### Primary Flows

#### Owner Invite Flow

1. The project owner opens a project detail page and chooses a clearly labeled collaboration control.
2. The owner searches for or enters an existing Client username using a validated form; the UI must not reveal arbitrary user data through search results.
3. The owner reviews the invite target and submits the CSRF-protected invitation.
4. The project page confirms the invitation is pending and shows it in the pending-invitations list.
5. The owner can revoke a pending invitation or remove an active collaborator from the same collaboration area, with confirmation for destructive membership changes.

#### Invitee Acceptance Flow

1. An invited client sees a pending invitation in an authenticated invitations area or receives a clearly linked in-app invitation state.
2. The invitee sees the project name, inviter/owner identity where appropriate, and the available Accept and Decline actions without seeing project content before acceptance.
3. Accepting changes the invitation to active membership and takes the client to the project detail page.
4. Declined, revoked, expired, already accepted, or invalid invitations show a safe explanatory state and do not expose project content.

### Permission-Aware Interface

- Show collaboration-management controls only to the project owner.
- Show owner identity and a collaborator roster with clear Pending and Active states; do not expose unrelated client accounts.
- For accepted collaborators, show project and task content plus the permitted task actions, but hide or disable project edit, project delete, invite, revoke, and remove controls.
- Keep existing task links, lanes/list view, task creation, task editing, task deletion, and status movement consistent with the approved collaborator permission policy.
- When a collaborator loses access, return a privacy-safe not-found or access-denied state and remove stale project actions without revealing whether the project still exists.

### Required States

- Owner collaboration area with no invitations or collaborators.
- Owner with one or more pending invitations.
- Owner with active collaborators and pending invitations together.
- Valid invite form with eligible Client target.
- Self-invite, non-client, duplicate-pending, duplicate-active, and unknown-user validation errors.
- Invitee pending invitation with Accept and Decline actions.
- Invitee accepted invitation and collaborator project view.
- Revoked, declined, expired/already-used, and invalid invitation states.
- Owner-only controls hidden from or denied to collaborators.
- Empty project/task states for an accepted collaborator.
- Long usernames/project names and narrow mobile layouts without clipping or horizontal overflow.

### Layout and Responsive Behavior

- Place collaboration controls and membership status in an identifiable project-level section near the existing project actions, without competing with the primary task workflow.
- Keep the project name and task section visually dominant; use a compact management area for invitations and collaborators.
- On desktop, separate invite form, pending invitations, and active collaborators into scannable groups with stable widths and clear headings.
- On mobile, stack the invite form, membership rows, and confirmation actions vertically; keep each username/status/action group readable without horizontal scrolling.
- Long usernames and project names must wrap within their containers; destructive actions must remain visually distinct and reachable.
- Preserve the existing project/task lanes and List toggle layout for collaborators and owners.

### Accessibility and Interaction

- Use semantic headings and a labeled collaboration section, with status communicated as text rather than color alone.
- Keep invite, accept, decline, revoke, and remove actions keyboard reachable in a logical order with visible focus.
- Associate validation errors with the invite field and preserve entered values after recoverable validation failures.
- Require confirmation before removing an active collaborator or revoking an invitation; make the consequence explicit.
- Announce successful invitations, acceptance, revocation, removal, and failures through an accessible status region.
- Preserve CSRF protection on every state-changing form/action and avoid exposing invitation tokens in visible text or assistive labels.
- Do not rely on email delivery, hover, drag, or color to communicate invitation state.

### Browser Validation Handoff

- Desktop: validate the owner invite/manage flow at 1440px, including pending and active membership rows and project task access.
- Intermediate: validate around 900px for form wrapping, action grouping, long names, and permission-aware controls.
- Mobile: validate at 390px for invitation acceptance, owner management, collaborator task access, denied owner-only actions, and no horizontal overflow.
- Exercise successful invite and acceptance, duplicate/self/invalid invite errors, revocation/removal confirmation, and post-removal access denial.
- Keyboard-check the invite form, membership actions, acceptance controls, confirmation dialogs, focus restoration, and live feedback.

## Approval

Status: Implemented, UX-reviewed, and ready for merge.

## UX Review

Status: PASS.

Browser validation covered the owner collaboration page at mobile width, pending invitation display, invitee Accept/Decline state, successful acceptance, collaborator project/task access, and hidden owner-only project controls. The collaboration page had no horizontal overflow and preserved the existing project/task navigation. Django tests, checks, migration validation, and Flake8 passed.

Follow-up UX fix: collaboration panels now use consistent desktop and mobile spacing, form rhythm, section separation, and full-width stacked actions on narrow screens. Live validation measured 32px panel gaps at desktop and 24px at mobile width with no horizontal overflow.
