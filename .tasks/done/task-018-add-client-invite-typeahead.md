# Ticket: Add Client Invite Typeahead

## User Story

As a project owner, I want to type `@` in the client invitation field and see eligible clients appear as suggestions so that I can quickly select the right collaborator without memorizing exact usernames.

## Context

The collaboration page currently uses a free-text `Client username` field. The owner must enter an exact username and receives feedback only after submitting the form. The invitation form already enforces Client-group membership, self-invite prevention, active-membership checks, and duplicate-pending checks, but it does not provide an in-context list of eligible clients.

The suggestions must be generated server-side from the authenticated project owner’s eligible invite targets. The UI must not expose arbitrary users, non-client users, unrelated account data, or clients who are already active/pending for the project.

## Scope

- Update the project collaboration invite field to support `@`-triggered client suggestions.
- Show a filtered list of eligible Client users as the owner types after `@` or searches by username.
- Allow the owner to select a suggestion and populate the invitation field with the exact invite target.
- Preserve the existing server-side invitation validation and CSRF-protected submit flow.
- Exclude the project owner, non-Client users, active collaborators, and pending invitees from suggestions.
- Add keyboard navigation and a non-pointer selection path for the suggestion list.
- Handle loading, empty, error, and invalid/unknown selection states without leaking account information.
- Preserve the collaboration page’s existing spacing, responsive layout, pending invitations, active collaborators, revoke, and remove controls.
- Add focused tests for suggestion filtering, authorization, query matching, selection/submit behavior, and privacy boundaries.
- Validate the typeahead at desktop and mobile widths.

## Acceptance Criteria

- [x] Typing `@` in the invite field opens an accessible suggestion list of eligible Client users for the current project.
- [x] Typing additional characters after `@` filters suggestions by username without requiring an exact full-string match.
- [x] Suggestions display only safe identifying text needed for selection, such as the username; no email, password, group, or unrelated account data is exposed.
- [x] The project owner is excluded from suggestions.
- [x] Users outside the `Client` group are excluded from suggestions.
- [x] Active collaborators and users with pending invitations for the project are excluded from suggestions.
- [x] Selecting a suggestion populates the invite field with the exact accepted username and allows the existing invitation form to submit normally.
- [x] The suggestion list supports keyboard navigation, selection, Escape to dismiss, and visible focus; pointer selection remains available.
- [x] Suggestions have accessible combobox/listbox semantics, an accessible label, and a clear active option state; selection is not communicated by color alone.
- [x] The owner receives a clear empty state when no eligible clients match and a safe error state if suggestions cannot load.
- [x] Unauthenticated users, non-owners, guessed project IDs, and unauthorized suggestion requests cannot enumerate Client users.
- [x] Existing invitation validation remains authoritative on submit, including self, non-client, duplicate-active, duplicate-pending, and unknown-user rejection.
- [x] The collaboration page retains consistent spacing and responsive behavior at desktop and mobile widths with no horizontal overflow.
- [x] Focused tests cover eligible filtering, `@`/query matching, owner and project authorization, exclusion rules, invalid requests, and existing invitation lifecycle behavior.
- [x] Browser validation passes at 1440px, 900px, and 390px for opening suggestions, filtering, keyboard selection, empty results, submit flow, and unauthorized access.
- [x] No new account data is persisted and no database migration is added unless implementation evidence shows it is required.

## Out of Scope

- Inviting users who do not already have a Client account.
- Email delivery, external notifications, account search outside the current project invite flow, or organization-wide directory features.
- Exposing email addresses, profiles, avatars, roles, or other account metadata in suggestions.
- Changing project membership permissions, invitation lifecycle states, or owner/collaborator authorization rules.
- Replacing the existing invitation form submission or removing its server-side validation.
- Changing unrelated project/task layouts or collaboration spacing beyond what is required to fit the suggestion list.

## Implementation Notes

- Start from `ProjectInviteForm`, `ClientProjectInviteView`, and `project_collaborators.html`.
- Prefer a narrow owner-authorized suggestion endpoint or a server-rendered progressive-enhancement approach; never return users outside the eligible project invite queryset.
- Use a minimum query length after `@`, debounce client requests if JavaScript is used, and avoid revealing whether a specific non-eligible username exists.
- Keep the submitted username authoritative on the server and reuse `ProjectInviteForm` validation.
- Preserve CSRF protection for invitation creation; suggestion requests must not mutate data.
- Use branch `task-018-add-client-invite-typeahead`.
- Pull request title: `[task-018] Add client invite typeahead`.
- Run `@ux-developer` specification and browser validation before `@tech-lead` review.

## UX Specification

### Primary Flow

1. The project owner opens the existing collaboration page and focuses **Client username**.
2. Typing `@` opens an anchored suggestion list of eligible clients; typing additional characters filters the list.
3. The owner moves through suggestions with Arrow Up/Down or pointer, selects one with Enter/Space or click, and sees the exact username placed in the field.
4. The owner submits the existing invitation form and receives the same pending-invitation confirmation and validation behavior.

### Combobox and Suggestion Behavior

- Treat the input as a labeled combobox with `aria-expanded`, `aria-controls`, `aria-autocomplete`, and an active-option state.
- Render suggestions in a positioned listbox directly below the input, aligned to the input width and contained within the collaboration panel.
- Show the `@` trigger as the input affordance without requiring the owner to remove it before selecting; normalize the submitted value to the accepted username format.
- Use a short debounce and a minimum query threshold after `@`; do not issue a broad directory request for an empty query unless the product explicitly requires it.
- Display only usernames, with no email addresses, roles, profile fields, or hidden account metadata.
- Keep the suggestion list open while the owner continues typing and close it on Escape, selection, blur, or submit.
- Preserve the existing panel spacing; the popover must not change surrounding layout or push the active/pending sections unexpectedly.

### Required States

- `@` entered with eligible suggestions available.
- Filtered suggestions for a partial username query.
- Active keyboard-highlighted suggestion with clear text/state distinction.
- No matching eligible clients.
- Loading suggestions and suggestion-request failure.
- Selected username ready for invitation submission.
- Server-side validation errors for unknown, self, non-client, duplicate-active, or duplicate-pending targets.
- Unauthorized/non-owner or invalid-project suggestion request with a privacy-safe response.
- Long usernames and narrow viewport layouts without clipping, overlap, or horizontal overflow.

### Accessibility and Interaction

- Keep the existing visible label and help text associated with the input.
- Use listbox/option semantics and `aria-activedescendant` or an equivalent accessible active-option pattern.
- Ensure Arrow navigation, Enter selection, Escape dismissal, Tab progression, and pointer selection all work without requiring a mouse.
- Announce result counts, no-match state, loading, and errors through an appropriate status/live region without exposing hidden account data.
- Preserve visible focus on the input and selected option; restoring focus to the input after selection is preferred.
- Keep the Send invitation action reachable in the existing logical order and preserve CSRF-protected submission.

### Responsive Behavior and Spacing

- Desktop: suggestion list aligns to the input and remains above or within the panel’s visual boundary without covering the panel heading or action.
- Intermediate widths: long usernames wrap or truncate safely while the option remains selectable and readable.
- Mobile at 390px: the list fits the panel width, does not create horizontal scrolling, and does not obscure the Send invitation action after selection.
- Maintain the established collaboration-panel rhythm: consistent panel padding, form-field gap, suggestion-list offset, and spacing before active/pending sections.

### Browser Validation Handoff

- Validate at 1440px, 900px, and 390px.
- Exercise `@` opening, partial-query filtering, keyboard selection, Escape dismissal, pointer selection, no matches, loading/error feedback, and successful submit.
- Verify owner/self/non-client/duplicate users are absent from results and server-side invalid submissions remain safely rejected.
- Verify non-owners cannot load or enumerate suggestions and existing collaboration panels retain their spacing and responsive behavior.

## Approval

Status: Completed and merged in PR #17.

## UX Review

Status: PASS.

Browser validation confirmed `@` opens eligible usernames, partial queries filter results, ArrowDown/Enter selects a client, and the mobile layout remains aligned with no horizontal overflow. Owner-only filtering and server-side invitation validation remain authoritative.
