# Ticket: Add Invitee Invitation Inbox

## User Story

As an invited client, I want to see that I have been invited to a project when I log in so that I can review the project invitation and accept or decline it without needing an emailed or manually copied invitation link.

## Context

Project invitations currently have recipient-protected token routes for acceptance and decline, but the authenticated client workspace does not query or display received pending invitations. An invitee can log in successfully and see no indication that an invitation exists, and the project is correctly hidden until acceptance but has no discoverable path into the invitation UI.

The invitation token must remain private and recipient-authorized. The new UI should make pending invitations discoverable from the workspace while preserving the existing invitation lifecycle, project privacy, and owner/collaborator permissions.

## Scope

- Add an authenticated invitation inbox or invitation panel discoverable from the client workspace.
- Show pending invitations received by the current Client user, including the project name and inviter identity where appropriate.
- Provide direct Accept and Decline actions from the inbox and/or a dedicated invitation detail page.
- Preserve the existing recipient-only invitation token validation and CSRF-protected state changes.
- Remove or update an invitation from the pending inbox immediately after acceptance, decline, revocation, or other terminal state.
- Ensure accepted collaborators can then discover and access the invited project through the normal project workspace/list flow.
- Keep projects and related tasks hidden before acceptance and prevent non-recipients from discovering invitation metadata.
- Add focused tests for inbox visibility, pending/terminal states, recipient and non-recipient authorization, accept/decline actions, and project discoverability after acceptance.
- Validate the invitee experience at desktop and mobile widths, including empty and populated inbox states.

## Acceptance Criteria

- [x] A signed-in Client user with pending invitations sees a clearly labeled invitation notification or inbox entry from the main workspace.
- [x] The pending entry identifies the project and inviter using only approved, non-sensitive display data.
- [x] The invitee can open the invitation UI and accept or decline directly without manually copying a token URL.
- [x] Accept and Decline actions remain CSRF-protected and use the existing recipient-only authorization checks.
- [x] After acceptance, the invitation no longer appears as pending and the project appears in the invitee’s accessible project list/detail flow.
- [x] After decline, the invitation no longer appears as pending and the invitee does not gain project or task access.
- [x] Revoked, accepted, declined, invalid, or otherwise terminal invitations are not shown as actionable pending invitations.
- [x] A Client user with no pending invitations sees a clear empty/inactive state without misleading notification chrome.
- [x] A non-recipient cannot see another user’s pending invitation, project name, inviter identity, or invitation actions by guessing URLs or IDs.
- [x] Projects and related tasks remain inaccessible before acceptance and become accessible only after acceptance according to existing collaborator permissions.
- [x] Existing owner invitation management, project/task access boundaries, and invitation token behavior remain intact.
- [x] Focused tests cover pending inbox visibility, empty/terminal states, recipient authorization, accept/decline transitions, revocation, and post-acceptance project access.
- [x] Browser validation passes at 1440px, 900px, and 390px for logged-in invitees, including populated inbox, empty inbox, accept, decline, denied access, and responsive layout states.
- [x] No new sensitive account data is exposed, and any schema change is accompanied by a clean migration with explicit field metadata and constraints.

## Out of Scope

- Email delivery, push notifications, external notification providers, or invitation reminders.
- Inviting users who are not already registered Client users.
- Changing project owner/collaborator permissions, invitation lifecycle rules, or project/task authorization beyond making pending invitations discoverable.
- Exposing invitation tokens in the workspace, URLs beyond the existing protected action routes, or visible assistive text.
- Reworking unrelated task lanes, project layouts, profile pages, or authentication flows.

## Implementation Notes

- Start from `ClientLandingPageView`, `client_landing.html`, `ProjectInvitation` state handling, and the existing accept/decline views/routes.
- Query only pending invitations where `invitee=request.user`; do not infer invitation visibility from project IDs or client-submitted identifiers.
- Prefer a small workspace invitation panel with a dedicated detail/confirmation route if the existing accept/decline page should remain focused.
- Keep the existing recipient validation as the server-side authority for every state-changing action.
- Use branch `task-019-add-invitee-invitation-inbox`.
- Pull request title: `[task-019] Add invitee invitation inbox`.
- Run `@ux-developer` specification and browser validation before `@tech-lead` review.

## UX Specification

### Primary Invitee Flow

1. A signed-in invitee opens the normal client workspace and immediately sees a labeled pending-invitations affordance when invitations exist.
2. The invitee opens the invitation panel or inbox entry and sees each pending project invitation with the project name and inviter username.
3. The invitee chooses **Review invitation**, then sees the existing confirmation view with **Accept invitation** and **Decline invitation** actions.
4. Accepting returns the invitee to the project and makes it discoverable in the normal project list; declining returns to the workspace without granting access.
5. Terminal or revoked invitations disappear from actionable pending UI and are not presented as broken active tasks.

### Workspace Discoverability

- Add a clear invitation notification or inbox panel to the authenticated workspace near the intro/topbar and before task-focused content; do not hide it behind an unrelated project route.
- When pending invitations exist, show a concise count and a direct action such as **Review invitations**.
- The populated panel should list project name, inviter, pending status, and a review link without exposing invitation tokens.
- The empty state should omit urgent notification treatment and use concise copy such as “No pending invitations.”
- Keep the existing task summary and lane/list workflow visually primary after the invitation panel has been acknowledged.
- Preserve invitation visibility after ordinary login and page refresh until the invitation reaches a terminal state.

### Required States

- Workspace with one pending invitation.
- Workspace with multiple pending invitations.
- Workspace with no pending invitations.
- Invitation detail/confirmation with Accept and Decline actions.
- Accepted invitation followed by project list/detail access.
- Declined invitation followed by no project access.
- Revoked, accepted, declined, invalid, or already-used invitation opened through an old link.
- Non-recipient or unauthenticated access to invitation routes with privacy-safe denial.
- Long project/inviter names and narrow mobile layouts without clipping or horizontal overflow.

### Accessibility and Interaction

- Use a semantic invitation section with a heading and accessible count; do not rely on a badge color or icon alone.
- Keep Review, Accept, and Decline controls keyboard reachable in a logical order with visible focus.
- Preserve CSRF-protected POST actions for Accept and Decline and make the consequences clear in the copy.
- Announce state changes after acceptance or decline and return focus to a predictable workspace/project heading.
- Do not expose the invitation token in visible text, accessible names, data attributes intended for assistive technology, or the workspace URL.
- Ensure an empty inbox is understandable without suggesting that the user has missing work.

### Responsive Behavior

- Desktop at 1440px: invitation panel aligns with the workspace shell and does not compete with the task summary.
- Intermediate at 900px: multiple invitation entries remain scannable with actions aligned and no awkward wrapping.
- Mobile at 390px: invitation entries stack vertically, action buttons remain full-width or comfortably tappable, and the panel introduces no horizontal overflow.
- Keep spacing consistent with existing workspace sections and preserve the current project/task lane layout below the invitation UI.

### Browser Validation Handoff

- Validate logged-in invitee discovery at 1440px, 900px, and 390px with one and multiple pending invitations.
- Exercise Review, Accept, Decline, empty inbox, revoked/terminal invitation, non-recipient denial, and post-acceptance project discovery.
- Verify project/task content remains hidden before acceptance and accessible after acceptance.
- Keyboard-check invitation notification, review link, Accept, Decline, focus restoration, and live feedback.

## Approval

Status: Completed and merged in PR #18.

## UX Review

Status: PASS.

Browser validation confirmed a logged-in invitee sees the Pending invitations panel, project/inviter details, and a token-free Review invitation link. The populated inbox fit at 390px with no horizontal overflow; existing recipient-protected Accept/Decline actions and post-acceptance project discovery remain covered by tests.
