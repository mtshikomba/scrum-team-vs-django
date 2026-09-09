# Ticket: Add Task Status Lanes and List Toggle

## User Story

As a client, I want to view my tasks in vertical lanes grouped by status and move tasks between those lanes so that I can manage workflow at a glance, while retaining the current task list when I prefer a tabular view.

## Context

The client workspace **Task list** section and the project detail **Project tasks** section currently render tasks as tables. Each task already has one of three statuses: Outstanding, In progress, or Completed, and the existing task form allows a client to change status. The interface needs a faster visual workflow without removing the current list option.

Lanes should be the default view. Clients must be able to switch between the lane view and the current task-list/table view in both sections. Moving a task between lanes must persist the corresponding status through an owner-authorized request and preserve all existing task data.

## Scope

- Add a status-lane view to the client workspace **Task list** section.
- Add the same status-lane view to the project detail **Project tasks** section.
- Group tasks into the three existing status lanes: Outstanding, In progress, and Completed.
- Make lanes the default presentation when the section loads.
- Add an accessible control to switch between the default lane view and the current task-list/table view.
- Allow an authorized client to move a task between lanes and persist the task status without changing title, description, project, priority, due date, or ownership.
- Keep task links, priority, due date, task counts, empty states, and existing task actions available in both presentation modes.
- Preserve client ownership boundaries for viewing and moving tasks, including project-scoped access.
- Add focused tests for default view, view switching, lane grouping, status persistence, invalid transitions/values, and unauthorized access.
- Validate the interaction and responsive layout in a browser at desktop and mobile widths.

## Acceptance Criteria

- [x] The workspace **Task list** section renders the lane view by default.
- [x] The project detail **Project tasks** section renders the lane view by default.
- [x] Both sections provide an accessible toggle or segmented control for switching between **Lanes** and the existing **List** view.
- [x] The selected presentation mode is clear to keyboard and assistive-technology users, and switching modes does not navigate away or lose task context.
- [x] Each lane is labeled with the existing status name and contains only tasks with that status: Outstanding, In progress, or Completed.
- [x] A task can be moved from one lane to another by an authorized owner, and the corresponding status is persisted server-side.
- [x] Moving a task updates the visible lane and status metadata without changing the task title, description, project, priority, due date, or client owner.
- [x] The workspace view shows only the authenticated client’s tasks, and a client cannot move another client’s task by guessing an identifier or status endpoint.
- [x] The project detail view shows and updates only tasks belonging to that project and the authenticated client; cross-project and cross-client moves are rejected.
- [x] The existing list/table view remains available and retains task links, status, priority, due date, and current empty-state behavior.
- [x] Lane and list views preserve task links and existing task actions, including opening task details and using the existing task edit flow.
- [x] Empty lanes have a clear, stable presentation, and the all-empty state remains understandable in both sections.
- [x] The lane layout supports readable task cards at desktop and intermediate widths and becomes usable without horizontal overflow at mobile widths.
- [x] Drag/drop or equivalent move controls are keyboard accessible, have a non-pointer alternative, and expose a clear success or error state when a move is accepted or rejected.
- [x] Invalid status values, missing tasks, missing CSRF tokens, unauthenticated requests, and unauthorized task/project access fail safely without changing data.
- [x] Focused Django tests and project quality checks pass, including tests, Django checks, migration checks, Black, and Flake8.
- [x] Browser validation passes at desktop and mobile widths for default lanes, switching to list view, empty lanes, populated lanes, and at least one successful and one rejected move.
- [x] No new task fields or database migrations are introduced unless implementation evidence shows they are required.

## Out of Scope

- Adding new task statuses, priorities, filters, sorting, pagination, or project-management features.
- Changing the task model’s existing status choices or task ownership rules.
- Removing or redesigning the current list/table view.
- Replacing the existing task detail, task form, project detail, or project navigation flows.
- Introducing multi-user assignment, collaboration, comments, notifications, or real-time synchronization.
- Changing profile, authentication, project CRUD, or unrelated landing-page sections.

## Implementation Notes

- Start from the existing `#task-list` section in `core/templates/core/client_landing.html` and the task section in `core/templates/core/project_detail.html`.
- Reuse the existing status values, status classes, task links, priority labels, due-date display, and empty-state language where appropriate.
- Keep the list view available as a progressive enhancement fallback if client-side interaction is unavailable.
- Use an authenticated, CSRF-protected server path for status changes; enforce ownership and project scope in the view rather than trusting client-submitted identifiers.
- Define the behavior for a failed move so the UI restores the previous lane or clearly indicates that the server rejected the change.
- Use branch `task-016-add-task-status-lanes-and-list-toggle`.
- Pull request title: `[task-016] Add task status lanes and list toggle`.
- Run `@ux-developer` specification and browser validation before `@tech-lead` review.

## UX Specification

### Primary Flow

1. A client opens the workspace or a project detail page and sees tasks in status lanes by default.
2. The client scans the Outstanding, In progress, and Completed lanes and opens a task from its existing task link when needed.
3. The client moves a task to another status using pointer drag/drop or the equivalent keyboard-accessible move control.
4. The client receives immediate success or error feedback, with the task remaining in or returning to the correct lane.
5. The client switches that section to **List** when a tabular comparison of status, priority, and due date is more useful.

### View Toggle

- Provide a compact, labeled two-option segmented control near each section heading: **Lanes** and **List**.
- **Lanes** is selected and visible on initial load for both the workspace Task list and project Project tasks sections.
- The selected option must expose its state through native semantics such as a radio group or equivalent `aria-pressed` state; do not communicate selection by color alone.
- Switching views happens in place without a page navigation, losing the current section anchor, or changing task data.
- Treat the workspace section and project section as independent view contexts; switching one does not unexpectedly change the other.
- Preserve the selected mode during an in-place interaction and define a refresh behavior that remains predictable; a short-lived client preference is acceptable only if it does not override the required initial lanes default unexpectedly.

### Lane Structure and Task Cards

- Render three stable lanes in status order: **Outstanding**, **In progress**, **Completed**.
- Each lane has a visible heading, task count, and a distinct drop target that remains present when empty.
- Keep task cards scannable and consistent: title/task link, priority, due date, and current status where useful.
- Preserve the existing task detail link and task edit path; do not make drag handles the only way to open or act on a task.
- Use the existing status color classes as supporting cues, with text labels remaining the primary status signal.
- On desktop and intermediate widths, show lanes as balanced vertical columns with enough width for long task titles and metadata.
- On mobile, stack the lanes vertically in the same status order; do not require horizontal scrolling to reach a lane.

### Moving Tasks and Feedback

- Pointer users may drag a task card to another lane, with a clear visual drop-target state and a non-ambiguous move completion state.
- Every task card must also expose a keyboard-accessible **Move to** action, such as a labeled menu or select containing the two alternative statuses.
- Do not require keyboard users to simulate dragging; the equivalent move control must work with Tab, Enter/Space, and standard menu/select keyboard behavior.
- While a move is saving, expose a pending state and prevent duplicate submissions for that task.
- On success, update the card’s lane and status label, update the affected lane counts and section task count if needed, and announce a concise success message through an `aria-live` region.
- On rejection or network failure, keep or restore the card in its original lane, announce the failure, and provide a retry path without losing the task link or metadata.
- Do not imply that a move changed project, ownership, priority, due date, title, or description.

### Required States

- Workspace Task list with tasks in all three lanes.
- Project Project tasks with tasks in one, two, and all three statuses.
- Empty individual lanes alongside populated lanes.
- No tasks at all, with a clear empty state in both workspace and project contexts.
- List view with the existing table headers and task metadata.
- Selected Lanes and selected List toggle states, including keyboard focus.
- Move pending, move success, rejected move, invalid status, and unauthorized/error response states.
- Long task title, long project name, missing due date, and priority/status combinations that must not overlap.

### Accessibility and Interaction

- Keep the existing `section` headings and add a programmatically associated label for each view toggle and lane.
- Ensure the toggle, every task link, every move control, and any drag/drop alternative are keyboard reachable in a logical order.
- Use visible focus indicators for toggles, task links, move controls, and drop targets; focus must remain visible after a move or view switch.
- Provide an accessible name and state for each lane drop target and do not rely on color, position, or drag gesture alone.
- Announce view changes and move results without forcing a full-page reload; keep errors adjacent to the relevant control where possible.
- Preserve CSRF protection and ensure unauthorized responses do not leak whether another client’s task exists.

### Browser Validation Handoff

- Desktop: validate at 1440px with populated workspace and project lanes; confirm three readable columns, toggle placement, task metadata, and drop-target states.
- Intermediate: validate at approximately 900px; confirm lanes remain balanced or reflow cleanly and controls do not overlap.
- Mobile: validate at 390px; confirm lanes stack vertically, the toggle remains usable, task cards wrap, and there is no horizontal overflow.
- Exercise both section toggles, initial default Lanes mode, switch to List and back, an empty lane, a populated lane, one successful move, and one rejected move.
- Keyboard-check the toggle, task link, Move to control, and status feedback; verify focus remains visible after switching and moving.

## Approval

Status: Completed and merged in PR #15.

## UX Review

Status: PASS.

Validation completed on the workspace Task list and project Project tasks sections. Lanes are the default view, List switching remains available, the three status lanes and empty lane states render correctly, keyboard status controls work, successful moves update the lane with live feedback, and rejected status requests return a safe error. Browser checks covered desktop, intermediate, and 390px mobile widths with no horizontal overflow; project task context and mobile lane stacking were verified.

Follow-up UX fix: moving a task into an empty lane now removes the placeholder instead of leaving the card below it. Moving the final task out of a lane restores the placeholder, and board spacing between the view controls, lanes, drop zones, and cards is consistent.
