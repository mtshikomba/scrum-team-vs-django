# Django Project

Minimal Django project scaffold for local development.

## Agent Workflow

This project uses three agents to move work from an idea to reviewed code:

### `@product-owner`

Turns a loose request into a groomed Markdown ticket. The ticket should include a user story, scope, acceptance criteria, out-of-scope items, and implementation notes. The product owner pauses for human approval or refinement before implementation begins.

### `@developer`

Implements an approved ticket, writes the required Django tests, and validates the change. The developer moves the ticket through the task lifecycle and prepares the feature branch and pull request.

### `@tech-lead`

Reviews the pull request after it is created. The review checks architecture, authorization, CSRF/XSS risks, query performance, migrations, tests, and adherence to the acceptance criteria before merge.

## End-to-End Process

1. Ask `@product-owner` to run `#groom-ticket` for the feature request.
2. Review the generated ticket and reply **Approve** or **Refine**.
3. After approval, ask `@developer` to implement the ticket. The ticket moves from `.tasks/todo/` to `.tasks/in-progress/`.
4. The developer writes tests first where practical, implements the smallest complete change, and runs the project checks.
5. The developer moves the completed ticket to `.tasks/done/`, pushes the feature branch, and creates a pull request into `main`.
6. Ask `@tech-lead` to review the pull request and address any findings.
7. Merge only after the tech-lead review passes and the Definition of Done checks are green.

## Task and Git Conventions

Use one task ID across the ticket, branch, and pull request:

- Tickets: `.tasks/{status}/task-NNN-{kebab-case-summary}.md`
- Lifecycle: `.tasks/todo/` -> `.tasks/in-progress/` -> `.tasks/done/`
- Branches: `task-NNN/{kebab-case-summary}`
- Pull request titles: `[task-NNN] Imperative summary`
- Pull request bodies: include the ticket ID, implementation summary, acceptance-criteria status, tests and validation, and migration notes when applicable.

Use three-digit sequential IDs that are never reused. Keep summaries concise, lowercase ASCII, and kebab-case. Preserve the same ticket filename while moving it between lifecycle folders.

Example:

```text
Ticket: .tasks/todo/task-006-add-task-filters.md
Branch: task-006/add-task-filters
Pull request: [task-006] Add task filters
```

## Definition of Done

Before a ticket is complete:

- Django unit or integration tests pass.
- `python manage.py check` passes.
- `python manage.py makemigrations --check --dry-run` passes.
- Black formatting passes.
- Flake8 linting passes.
- New models and views have concise Google-style docstrings.
- A migration is generated and included when models change.
- Acceptance criteria are checked off in the completed ticket.

## Example Prompts

Groom a request:

```text
@product-owner run #groom-ticket: Add [feature description].
```

Implement an approved ticket:

```text
@developer implement task-006-add-task-filters.md.
```

Create a pull request:

```text
@developer create a PR into main for task-006.
```

Review a pull request:

```text
@tech-lead review PR #123.
```

## Setup

This project targets Python 3.9 or newer within the supported Django 4.2 range.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
```

The settings module reads environment variables from the shell. Load `.env` with your preferred environment manager when needed; Django does not read `.env` files automatically.

### Create a local client user

Client access is granted through membership in the Django `Client` group. Create the group and assign a user with the Django shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import Group, User

client_group, _ = Group.objects.get_or_create(name="Client")
user = User.objects.get(username="your-username")
user.groups.add(client_group)
```

Membership in `Client` is required for the client landing page; staff status alone does not grant access.

## Run

```bash
python manage.py runserver
```

The health check is available at `http://127.0.0.1:8000/health/`.

## Test and quality checks

```bash
python manage.py test
black --check .
flake8 .
```

Use `black .` to format the project after making changes.