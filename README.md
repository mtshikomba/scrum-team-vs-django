# Django Project

Minimal Django project scaffold for local development.

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