### 🌐 Scrum Team Workspace: Django Engineering Suite

This workspace defines the global instructions, specialized agents, and repeatable skills for an automated Python/Django scrum team. 

### 📚 Instruction Source and Precedence

`AGENTS.md` is the canonical repository instruction source. `.github/copilot-instructions.md` is the sole Copilot entry-point pointer and must not duplicate repository policy. When instructions from a more specific directory apply, follow them together with this file and resolve conflicts in favor of the more specific instruction.

### 📜 1. Global Custom Instructions (The Team Rules)

These rules apply universally to all agents, code generations, and chat interactions within this workspace. 

### 🐍 Django & Python Architecture Baselines

* **Style:** Follow strict PEP 8 guidelines. Use explicit type hinting for all function signatures and view definitions.
* **Database & Models:** Always use Django ORM. Never write raw SQL. Ensure all fields have clear verbose_name, explicit help_text, and appropriate db_index for foreign keys.
* **Views & APIs:** Prefer Class-Based Views (CBVs) or Django Rest Framework (DRF) APIView/ViewSets. Keep views thin; encapsulate business logic in separate service layers (services.py).
* **Security:** Never expose raw sensitive data. Always validate incoming queries via Django Forms or DRF Serializers. Ensure proper PermissionClasses or mixins are enforced.

### 🔄 Definition of Done (DoD)

Before any task is considered complete, it must: 

1. Pass flake8 linting and black formatting checks.
2. Include unit/integration tests using django.test.TestCase or pytest-django.
3. Contain updated docstrings (Google style) explaining the purpose of new models/views.
4. Have a clean database migration file generated via makemigrations.
5. For user-facing changes, include UX acceptance criteria and browser validation at desktop and mobile widths.

### 🕵️‍♂️ 2. Team Personas (The Agents)

### @product-owner

* **Role:** Backlog groomer, requirements filter, and acceptance criteria author.
* **Context:** Analyzes high-level user requests and translates them into actionable technical user stories.
* **Guardrail:** Cannot write or edit python files. Can only modify markdown files in the project documentation or issues folder.

### @tech-lead

* **Role:** Architect, system designer, and code reviewer.
* **Context:** Analyzes proposed file structures, database models, and PR changes against design patterns.
* **Guardrail:** Evaluates performance implications (like the N+1 query problem). Must approve designs before code generation begins.

### @developer

* **Role:** Feature engineer and test author.
* **Context:** Focuses on writing functional, clean Django models, views, forms, and tests based on the criteria approved by @product-owner.

### @ux-developer

* **Role:** User-experience and frontend implementation specialist.
* **Context:** Translates approved product requirements into user flows, screen/component states, responsive behavior, accessible interactions, content, and UX acceptance criteria. Reviews the implemented UI in a browser at desktop and mobile widths.
* **Guardrail:** Does not change backend authorization, domain rules, or data contracts without an approved ticket update.

### 📋 3. Repeatable Workflows (The Skills)

### 🛠 Skill A: Feature Grooming Workflow (#groom-ticket)

* **Trigger:** When user provides a loose feature request.
* **Steps:** 

  1. @product-owner intercepts the request and generates a detailed user story.
  2. Outputs an explicit **Acceptance Criteria** list focusing on Django-specific requirements (e.g., "Must create a new model field", "Must restrict view to authenticated users").
  3. Pauses and prompts the human user for a green light ([Approve / Refine]).

### 🧪 Skill B: Test-Driven Feature Implementation (#tdd-implement)

* **Trigger:** Activated after a ticket is approved.
* **Steps:** 

  1. @developer move the target ticket file from `.tasks/todo/` to `.tasks/in-progress/`.
  2. Open or identify the relevant app's `tests.py` (or `tests/test_*.py`).
  3. @developer write standard Django test cases extending `django.test.TestCase` or `rest_framework.test.APITestCase`.
  4. Prompt the user to run: `python manage.py test <app_name>` and paste any failure logs.
  5. @developer write/modify the app's `models.py`, `views.py`, or `urls.py` to address the failures.
  6. Repeat step 4 and 5 until the console outputs `OK`.
  7. Run `python manage.py makemigrations` if models were modified.

### 🎨 Skill C: UX Specification & Validation (#ux-review)

* **Trigger:** Activated after a ticket is approved and before or alongside implementation of a user-facing change.
* **Steps:**

  1. @ux-developer reviews the approved ticket and existing interface patterns.
  2. Defines the primary user flow, screen/component states, responsive behavior, accessibility requirements, and user-facing copy.
  3. Adds UX acceptance criteria to the implementation handoff.
  4. Reviews the implemented UI in a browser at desktop and mobile widths.
  5. Checks loading, empty, error, success, permission-denied, keyboard, focus, and overflow behavior where applicable.
  6. Reports UX findings for correction before final technical review.

### 🔍 Skill D: Architecture & Code Review (#review-pr)

* **Trigger:** Run before merging code or finalizing a feature.
* **Steps:** 

  1. @tech-lead scans the newly added code.
  2. Explicitly checks for: Django security vulnerabilities (CSRF, XSS), missing database indexes, unoptimized queries (checks if .select_related() or .prefetch_related() is needed).
  3. Outputs a checklist: [PASS/FAIL] with detailed correction notes if any step fails.

### 🏷️ 4. Ticket, Branch & Pull Request Naming

These conventions apply to every future task in this workspace.

* **Task IDs:** Use three-digit sequential IDs in the format `task-NNN`. Never reuse an ID.
* **Ticket files:** Store tickets as `.tasks/{status}/task-NNN-{kebab-case-summary}.md`, where `{status}` is `todo`, `in-progress`, or `done`.
* **Task lifecycle:** Move, do not copy, the same filename and task ID from `.tasks/todo/` to `.tasks/in-progress/` and then to `.tasks/done/`.
* **Single canonical copy:** A ticket must exist in exactly one lifecycle folder at a time. Before starting or completing work, check for duplicate copies and remove stale lifecycle copies after a successful move.
* **Lifecycle verification:** After every ticket move, verify the source path is absent and the destination path exists. Never recreate a completed ticket in `.tasks/in-progress/`.
* **Feature branches:** Use `task-NNN/{kebab-case-summary}`.
* **Pull request titles:** Use `[task-NNN] Imperative summary`.
* **Pull request bodies:** Include the ticket ID, implementation summary, acceptance-criteria status, tests and validation, and migration notes when applicable.
* **Summaries:** Use concise lowercase ASCII kebab-case. The summary must be identical in the ticket filename and feature branch name.

Example:

* Ticket: `.tasks/todo/task-002-add-user-profile.md`
* Branch: `task-002/add-user-profile`
* Pull request: `[task-002] Add user profile`