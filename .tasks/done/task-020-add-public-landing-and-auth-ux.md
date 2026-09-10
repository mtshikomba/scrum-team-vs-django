# Ticket: Add Public Landing Page and Improve Authentication UX

## User Story

As a prospective or returning client, I want a clear public landing page that explains the task-management workspace and links directly to sign in and registration, while the login and registration pages should feel polished, trustworthy, and easy to complete.

## Context

The root URL currently serves the authenticated client workspace and redirects anonymous users to sign in. There is no public customer-facing landing page that explains the product or provides a clear path to account access. The existing login and registration screens are functional but minimal centered forms with limited orientation, navigation, and error-state polish.

This change should introduce a public entry experience while preserving the authenticated workspace at a stable route and keeping the existing authentication, CSRF, redirect, authorization, and registration behavior intact.

## Scope

- Add a public, unauthenticated customer-facing landing page that explains the core workspace value and primary capabilities.
- Provide prominent, direct links to the existing login and registration routes.
- Define a clear behavior for authenticated users visiting the public landing route; they should be able to continue to the workspace without losing their session.
- Improve login and registration UI/UX using the established visual language while preserving form fields, CSRF protection, validation, error messages, password handling, and redirect behavior.
- Add clear cross-navigation between login and registration and a route back to the public landing page where appropriate.
- Include accessible headings, labels, focus states, keyboard navigation, readable validation errors, and responsive layouts.
- Add focused tests for public access, authenticated behavior, route links, form rendering, and existing security/redirect boundaries.
- Validate public landing, login, and registration pages in a browser at desktop and mobile widths.

## Acceptance Criteria

- [x] Anonymous users can open the public landing page without being redirected to login.
- [x] The landing page clearly communicates the system’s core capabilities: project-based task management, status-lane/list views, collaboration invitations, task details, and client-owned workspace access.
- [x] The landing page provides prominent links to the existing sign-in and registration pages.
- [x] Authenticated users visiting the public landing route receive a clear path to the workspace and do not lose their session; the chosen redirect behavior is covered by tests.
- [x] The landing page preserves a coherent first viewport and shows useful continuation content on desktop and mobile without requiring authentication to understand the product.
- [x] Login and registration pages share a consistent branded visual treatment and include clear links to each other and the public landing page.
- [x] Login preserves the `next` parameter and redirects successfully authenticated users according to existing behavior.
- [x] Registration continues to create a regular Client user, rejects invalid submissions, and does not grant elevated privileges.
- [x] Login and registration validation errors remain visible, associated with the relevant fields, and usable with keyboard and assistive technology.
- [x] All authentication forms retain CSRF protection, password masking/handling, and existing security boundaries.
- [x] Public landing, login, and registration pages have visible focus states, logical keyboard order, accessible headings/labels, sufficient contrast, and no horizontal overflow.
- [x] Browser validation passes at 1440px, 900px, and 390px for public landing, login, registration, and representative validation-error states.
- [x] Focused Django tests and project quality checks pass, including tests, Django checks, migration checks, Black, and Flake8.
- [x] No project/task data models, collaboration permissions, invitation rules, or unrelated authenticated workspace behavior are changed.
- [x] No database migration is introduced unless implementation evidence shows it is required.

## Out of Scope

- Replacing the authenticated client workspace or redesigning project/task management screens.
- Adding payment, billing, analytics, external marketing integrations, email campaigns, or a CMS.
- Changing authentication providers, password policy, user roles, Client-group rules, authorization boundaries, or session behavior.
- Adding new product capabilities beyond accurately presenting existing project, task, lane/list, rich-description, and collaboration features.
- Changing invitation lifecycle or collaborator permissions.

## Implementation Notes

- Add a public landing view/template and route without weakening `ClientAccessMixin` protection on the authenticated workspace.
- Decide and document the public route/workspace route behavior before implementation; preserve existing named routes where possible to minimize redirect regressions.
- Reuse the established `landing.css` design language, but introduce scoped public/auth styles rather than destabilizing task/project layouts.
- Keep all login/registration form rendering server-side and compatible with Django’s existing authentication views and `ClientRegistrationForm`.
- Test anonymous and authenticated access separately, including the login `next` flow.
- Use branch `task-020-add-public-landing-and-auth-ux`.
- Pull request title: `[task-020] Add public landing and auth UX`.
- Run `@ux-developer` specification and browser validation before `@tech-lead` review.

## UX Specification

### Public Entry Flow

1. An anonymous visitor opens the public root landing page and immediately understands what Client tasks helps them manage.
2. The visitor scans the primary capabilities: project-based tasks, status lanes and list view, rich task context, and controlled client collaboration.
3. The visitor chooses **Sign in** or **Create an account** from the primary navigation or hero actions.
4. An authenticated user visiting the public entry route sees a clear **Open workspace** action and can continue without losing their session.

### Landing Page Structure

- Use the product name and a literal task-management value proposition as the first-viewport signal.
- Keep the primary experience actionable: prominent Sign in and Create account controls, with no dead-end marketing interaction.
- Show a restrained feature overview using existing system capabilities only: projects, tasks, status lanes/List view, rich descriptions, and invited collaboration.
- Include a visible continuation cue to the feature overview or next content section without making the page feel like an unrelated marketing site.
- Keep copy concise, specific, and client-facing; do not claim email notifications, automation, integrations, or capabilities not present in the system.
- Provide a consistent top navigation with brand, Sign in, and Create account links; authenticated users receive an obvious workspace link instead.

### Authentication Experience

- Login and registration share the same branded shell, typography, field rhythm, button treatment, and public landing link.
- Keep the form as the visual focus, with concise supporting copy explaining the next step and clear cross-navigation between the two auth flows.
- Preserve field labels, password masking, CSRF, `next` handling, server-rendered errors, and registration security behavior.
- Make invalid submission states easy to scan: errors remain adjacent to their fields, do not collapse layout, and preserve entered non-sensitive values.
- Keep the primary action label explicit: **Sign in** or **Create account**; avoid competing secondary actions inside the form.
- Provide a safe path back to the public landing page without disrupting a pending authentication flow.

### Required States

- Anonymous public landing page.
- Authenticated visitor on the public route with an Open workspace action.
- Login initial, invalid credentials, and successful `next` redirect states.
- Registration initial, validation-error, duplicate username, password mismatch, and successful completion states.
- Narrow mobile landing, login, and registration layouts.
- Keyboard focus on public navigation, hero actions, fields, submit buttons, and cross-links.

### Accessibility and Interaction

- Use one clear page heading per screen and semantic navigation/main/section landmarks.
- Ensure every auth field has a visible label and any error is programmatically associated with the relevant field.
- Preserve logical keyboard order: navigation, primary landing action, supporting content, then footer/secondary links; auth brand/back link, fields, submit, and cross-navigation.
- Provide visible focus states with sufficient contrast and ensure focus is not hidden by responsive layout changes.
- Do not rely on color, large imagery, or placeholder text alone to communicate product value or field requirements.
- Keep action links descriptive and distinguishable for screen readers; public and authenticated destinations must be clear.

### Responsive Behavior

- Desktop at 1440px: establish a confident first viewport with product identity, primary actions, and a visible hint of the feature overview below.
- Intermediate at 900px: preserve hierarchy and readable feature content without awkward empty bands or crowded navigation.
- Mobile at 390px: stack hero actions and feature content cleanly, keep navigation tappable, and prevent horizontal overflow.
- Login and registration panels remain readable at all widths, with form controls fitting the viewport and errors not overlapping subsequent fields/actions.
- Preserve the established teal/yellow/ink visual language while using scoped public/auth styles that do not alter workspace task/project layouts unexpectedly.

### Browser Validation Handoff

- Validate public landing, login, and registration at 1440px, 900px, and 390px.
- Exercise anonymous landing access, Sign in/Create account links, authenticated workspace continuation, invalid login, invalid registration, and successful `next` redirect.
- Verify keyboard traversal and visible focus across navigation, hero actions, auth fields, submit buttons, and cross-links.
- Check clipping, overlap, contrast, readable line lengths, and horizontal overflow on all three surfaces.

## Approval

Status: Completed and merged in PR #19.

## UX Review

Status: PASS.

Browser validation confirmed the public landing page, login, and registration surfaces at desktop, intermediate, and mobile widths. Public navigation links work, authenticated workspace access remains protected at `/workspace/`, auth cross-links are visible, and no horizontal overflow was observed.

Follow-up UX fix: added a collaboration-focused closing CTA and a basic Client Tasks brand footer so the public landing page has a complete ending. The CTA and footer were browser-checked at 1440px, 900px, and 390px with responsive stacking and no horizontal overflow.
