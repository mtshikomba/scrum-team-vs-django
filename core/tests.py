from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.test import Client as TestClient
from django.test import TestCase

from core.models import Project, Task


class HealthCheckViewTests(TestCase):
    """Verify that the initial application health endpoint is available."""

    def test_health_check_returns_ok(self) -> None:
        """The health endpoint returns a successful JSON response."""
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})


class ClientProfileTests(TestCase):
    """Verify client profile access and privilege boundaries."""

    def setUp(self) -> None:
        self.client_group = Group.objects.create(name="Client")
        self.user = User.objects.create_user(
            username="profile-client", password="old-password"
        )
        self.user.groups.add(self.client_group)
        self.other_user = User.objects.create_user(
            username="profile-other", password="other-password"
        )
        self.client.force_login(self.user)

    def test_client_can_update_personal_profile_fields(self) -> None:
        """A client can save approved personal fields."""
        response = self.client.post(
            "/profile/",
            {
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "ada@example.com",
            },
        )

        self.assertRedirects(response, "/profile/")
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Ada")
        self.assertEqual(self.user.last_name, "Lovelace")
        self.assertEqual(self.user.email, "ada@example.com")

    def test_profile_payload_cannot_change_authorization(self) -> None:
        """Unauthorized user fields are ignored by the profile form."""
        self.client.post(
            "/profile/",
            {
                "first_name": "Safe",
                "username": "hijacked",
                "is_staff": "on",
                "is_superuser": "on",
                "groups": [self.client_group.pk],
            },
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "profile-client")
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.groups.filter(name="Client").exists())

    def test_anonymous_and_non_client_profile_access_is_denied(self) -> None:
        """Only client users can access profile pages."""
        self.client.logout()
        self.assertRedirects(
            self.client.get("/profile/"), "/accounts/login/?next=/profile/"
        )
        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get("/profile/").status_code, 403)

    def test_password_change_requires_current_password(self) -> None:
        """Password changes use Django validation and invalidate old credentials."""
        response = self.client.post(
            "/profile/password/",
            {
                "old_password": "old-password",
                "new_password1": "new-secure-password",
                "new_password2": "new-secure-password",
            },
        )

        self.assertRedirects(response, "/profile/")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new-secure-password"))
        self.assertFalse(self.user.check_password("old-password"))

    def test_password_change_rejects_wrong_current_password(self) -> None:
        """An incorrect current password leaves the account unchanged."""
        response = self.client.post(
            "/profile/password/",
            {
                "old_password": "wrong-password",
                "new_password1": "new-secure-password",
                "new_password2": "new-secure-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("old-password"))


class ClientRegistrationTests(TestCase):
    """Verify secure registration and automatic client authorization."""

    def test_registration_page_is_public(self) -> None:
        """Anonymous users can open the registration form."""
        response = self.client.get("/accounts/register/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create your account")

    def test_successful_registration_creates_client_user(self) -> None:
        """Valid registration creates a regular user in the Client group."""
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "new-client",
                "email": "new-client@example.com",
                "password1": "secure-registration-password",
                "password2": "secure-registration-password",
            },
        )

        self.assertRedirects(response, "/accounts/login/")
        user = User.objects.get(username="new-client")
        self.assertTrue(user.check_password("secure-registration-password"))
        self.assertTrue(user.groups.filter(name="Client").exists())
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_invalid_registration_does_not_create_user(self) -> None:
        """Invalid passwords re-render errors without creating a user."""
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "invalid-client",
                "email": "invalid@example.com",
                "password1": "short",
                "password2": "different",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "password")
        self.assertFalse(User.objects.filter(username="invalid-client").exists())

    def test_duplicate_username_is_rejected(self) -> None:
        """A duplicate username is rejected without creating another user."""
        User.objects.create_user(username="existing-client", password="password")

        response = self.client.post(
            "/accounts/register/",
            {
                "username": "existing-client",
                "email": "new@example.com",
                "password1": "secure-registration-password",
                "password2": "secure-registration-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that username already exists")
        self.assertEqual(User.objects.filter(username="existing-client").count(), 1)

    def test_registration_cannot_grant_elevated_privileges(self) -> None:
        """Privilege fields in submitted data are ignored by the form."""
        self.client.post(
            "/accounts/register/",
            {
                "username": "regular-client",
                "email": "regular@example.com",
                "password1": "secure-registration-password",
                "password2": "secure-registration-password",
                "is_staff": "on",
                "is_superuser": "on",
            },
        )

        user = User.objects.get(username="regular-client")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class ClientLandingPageTests(TestCase):
    """Verify authentication and client isolation on the landing page."""

    def setUp(self) -> None:
        self.client_group = Group.objects.create(name="Client")
        self.client_user = User.objects.create_user(
            username="client@example.com", password="test-password"
        )
        self.client_user.groups.add(self.client_group)
        self.project = Project.objects.create(
            client=self.client_user, name="Client project"
        )
        self.other_user = User.objects.create_user(
            username="other@example.com", password="test-password"
        )
        self.other_project = Project.objects.create(
            client=self.other_user, name="Other project"
        )

    def test_anonymous_users_are_redirected_to_login(self) -> None:
        """Anonymous users cannot access the client landing page."""
        response = self.client.get("/")

        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_client_login_redirects_to_landing_page(self) -> None:
        """A client who signs in is sent to the client landing page."""
        response = self.client.post(
            "/accounts/login/",
            {"username": "client@example.com", "password": "test-password"},
        )

        self.assertRedirects(response, "/")

    def test_authenticated_non_client_is_forbidden(self) -> None:
        """An authenticated user outside the Client group is denied."""
        self.client.force_login(self.other_user)

        response = self.client.get("/")

        self.assertEqual(response.status_code, 403)

    def test_staff_status_does_not_grant_client_access(self) -> None:
        """Staff status alone does not bypass the client boundary."""
        self.other_user.is_staff = True
        self.other_user.save(update_fields=["is_staff"])
        self.client.force_login(self.other_user)

        response = self.client.get("/")

        self.assertEqual(response.status_code, 403)

    def test_landing_page_shows_only_authenticated_client_tasks(self) -> None:
        """A client sees its own task summary and not another client's task."""
        own_task = Task.objects.create(
            client=self.client_user,
            project=self.project,
            title="Review project brief",
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.HIGH,
        )
        Task.objects.create(
            client=self.other_user,
            project=self.other_project,
            title="Private task",
        )
        self.client.force_login(self.client_user)

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, own_task.title)
        self.assertNotContains(response, "Private task")
        self.assertEqual(response.context["task_counts"]["in_progress"], 1)

    def test_landing_page_shows_empty_state_without_tasks(self) -> None:
        """A client without tasks receives a useful empty state."""
        self.client.force_login(self.client_user)

        response = self.client.get("/")

        self.assertContains(response, "No tasks yet")


class ClientTaskManagementTests(TestCase):
    """Verify client-owned task CRUD and request protection."""

    def setUp(self) -> None:
        self.client_group = Group.objects.create(name="Client")
        self.client_user = User.objects.create_user(
            username="task-client@example.com", password="test-password"
        )
        self.client_user.groups.add(self.client_group)
        self.project = Project.objects.create(
            client=self.client_user, name="Task project"
        )
        self.other_user = User.objects.create_user(
            username="task-other@example.com", password="test-password"
        )
        self.task = Task.objects.create(
            client=self.client_user,
            project=self.project,
            title="Review project brief",
            status=Task.Status.OUTSTANDING,
            priority=Task.Priority.MEDIUM,
        )
        self.client.force_login(self.client_user)

    def test_client_can_create_task(self) -> None:
        """A valid task is assigned to the authenticated client."""
        response = self.client.post(
            "/tasks/new/",
            {
                "title": "Prepare project notes",
                "description": "<p>Important <strong>project</strong> notes.</p>",
                "project": self.project.pk,
                "status": Task.Status.IN_PROGRESS,
                "priority": Task.Priority.HIGH,
                "due_date": "2026-10-01",
            },
        )

        created_task = Task.objects.get(title="Prepare project notes")
        self.assertRedirects(response, "/")
        self.assertEqual(created_task.client, self.client_user)
        self.assertEqual(
            created_task.description, "<p>Important <strong>project</strong> notes.</p>"
        )

    def test_task_description_sanitizes_unsafe_html(self) -> None:
        """Task descriptions preserve formatting without executable markup."""
        response = self.client.post(
            "/tasks/new/",
            {
                "project": self.project.pk,
                "title": "Safe task",
                "description": (
                    '<p>Safe</p><script>alert("x")</script>'
                    '<a href="javascript:bad">bad</a>'
                ),
                "status": Task.Status.OUTSTANDING,
                "priority": Task.Priority.MEDIUM,
            },
        )

        self.assertRedirects(response, "/")
        task = Task.objects.get(title="Safe task")
        self.assertNotIn("script", task.description.lower())
        self.assertNotIn("javascript:", task.description.lower())
        self.assertContains(self.client.get(task.get_absolute_url()), "Safe")

    def test_task_without_description_shows_empty_state(self) -> None:
        """Tasks without descriptions render a clear empty state."""
        response = self.client.get(self.task.get_absolute_url())

        self.assertContains(response, "No description added yet")

    def test_invalid_task_does_not_create_record(self) -> None:
        """An invalid task form is shown without creating a task."""
        response = self.client.post(
            "/tasks/new/",
            {
                "title": "",
                "project": self.project.pk,
                "status": "invalid",
                "priority": Task.Priority.HIGH,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertEqual(Task.objects.count(), 1)

    def test_client_can_view_and_update_owned_task(self) -> None:
        """An owner can view and update its task."""
        detail_response = self.client.get(self.task.get_absolute_url())
        update_response = self.client.post(
            f"/tasks/{self.task.pk}/edit/",
            {
                "title": "Updated brief",
                "project": self.project.pk,
                "status": Task.Status.COMPLETED,
                "priority": Task.Priority.LOW,
                "due_date": "",
            },
        )

        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, self.task.title)
        self.assertRedirects(update_response, self.task.get_absolute_url())
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated brief")
        self.assertEqual(self.task.status, Task.Status.COMPLETED)

    def test_client_can_delete_owned_task(self) -> None:
        """An owner can confirm and delete its task."""
        confirm_response = self.client.get(f"/tasks/{self.task.pk}/delete/")
        delete_response = self.client.post(f"/tasks/{self.task.pk}/delete/", {})

        self.assertEqual(confirm_response.status_code, 200)
        self.assertContains(confirm_response, "Delete")
        self.assertRedirects(delete_response, "/")
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_other_client_cannot_access_owned_task(self) -> None:
        """Another client cannot read, update, or delete the task."""
        self.task.client = self.other_user
        self.task.save(update_fields=["client"])

        for path in (
            self.task.get_absolute_url(),
            f"/tasks/{self.task.pk}/edit/",
            f"/tasks/{self.task.pk}/delete/",
        ):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 404)

        response = self.client.post(
            f"/tasks/{self.task.pk}/edit/",
            {"title": "Attempted takeover", "status": Task.Status.COMPLETED},
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_mutations_require_csrf(self) -> None:
        """State-changing task requests reject missing CSRF tokens."""
        csrf_client = TestClient(enforce_csrf_checks=True)
        csrf_client.force_login(self.client_user)

        response = csrf_client.post(
            "/tasks/new/",
            {
                "title": "Missing token",
                "project": self.project.pk,
                "status": Task.Status.OUTSTANDING,
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Task.objects.filter(title="Missing token").exists())


class ClientProjectManagementTests(TestCase):
    """Verify project ownership and project-first task creation."""

    def setUp(self) -> None:
        self.client_group = Group.objects.create(name="Client")
        self.client_user = User.objects.create_user(
            username="project-client@example.com", password="test-password"
        )
        self.client_user.groups.add(self.client_group)
        self.other_user = User.objects.create_user(
            username="project-other@example.com", password="test-password"
        )
        self.other_project = Project.objects.create(
            client=self.other_user, name="Private project"
        )
        self.client.force_login(self.client_user)

    def test_client_can_create_and_view_project(self) -> None:
        """A client can create a project and see it in the project list."""
        response = self.client.post(
            "/projects/new/",
            {"name": "Website refresh", "description": "Public site work"},
        )

        project = Project.objects.get(name="Website refresh")
        self.assertRedirects(response, project.get_absolute_url())
        self.assertContains(self.client.get("/projects/"), project.name)

    def test_project_pages_use_the_full_width_layout_hook(self) -> None:
        """Project pages expose the layout hook that expands their content area."""
        project = Project.objects.create(client=self.client_user, name="Workspace")

        project_list_response = self.client.get("/projects/")
        project_detail_response = self.client.get(project.get_absolute_url())

        self.assertContains(project_list_response, 'class="detail-panel project-page"')
        self.assertContains(
            project_detail_response, 'class="detail-panel project-page"'
        )

    def test_project_and_task_action_pages_show_workspace_navigation(self) -> None:
        """Project and task action pages render the shared workspace navigation."""
        project = Project.objects.create(client=self.client_user, name="Workspace")
        task = Task.objects.create(
            client=self.client_user, project=project, title="Review navigation"
        )
        action_paths = (
            "/projects/new/",
            f"/projects/{project.pk}/edit/",
            f"/projects/{project.pk}/delete/",
            "/tasks/new/",
            f"/tasks/{task.pk}/edit/",
            f"/tasks/{task.pk}/delete/",
        )

        for path in action_paths:
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'class="topbar"')
                self.assertContains(response, 'class="brand"')
                self.assertContains(response, 'action="/accounts/logout/"')

    def test_project_name_is_unique_per_client(self) -> None:
        """A client cannot create duplicate project names."""
        Project.objects.create(client=self.client_user, name="Website refresh")

        response = self.client.post(
            "/projects/new/", {"name": "Website refresh", "description": "Again"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Project.objects.filter(
                client=self.client_user, name="Website refresh"
            ).count(),
            1,
        )

    def test_client_cannot_access_other_clients_project(self) -> None:
        """Project detail, edit, and delete are owner-scoped."""
        for path in (
            self.other_project.get_absolute_url(),
            f"/projects/{self.other_project.pk}/edit/",
            f"/projects/{self.other_project.pk}/delete/",
        ):
            self.assertEqual(self.client.get(path).status_code, 404)

    def test_task_creation_requires_a_project(self) -> None:
        """A client must choose a project before a task can be created."""
        Project.objects.create(client=self.client_user, name="Available project")
        response = self.client.post(
            "/tasks/new/",
            {
                "title": "Unassigned task",
                "status": Task.Status.OUTSTANDING,
                "priority": Task.Priority.MEDIUM,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertFalse(Task.objects.filter(title="Unassigned task").exists())

    def test_task_creation_redirects_when_client_has_no_projects(self) -> None:
        """A client must create a project before opening task creation."""
        self.client_user.client_projects.all().delete()

        response = self.client.get("/tasks/new/")

        self.assertRedirects(response, "/projects/new/")

    def test_anonymous_task_creation_redirects_to_login(self) -> None:
        """Anonymous users follow the login flow instead of raising an error."""
        self.client.logout()

        response = self.client.get("/tasks/new/")

        self.assertRedirects(response, "/accounts/login/?next=/tasks/new/")

    def test_non_client_task_creation_is_forbidden(self) -> None:
        """Authenticated users outside Client cannot create tasks."""
        self.client.force_login(self.other_user)

        response = self.client.get("/tasks/new/")

        self.assertEqual(response.status_code, 403)
