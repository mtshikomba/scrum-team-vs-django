from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.test import TestCase

from core.models import Task


class HealthCheckViewTests(TestCase):
    """Verify that the initial application health endpoint is available."""

    def test_health_check_returns_ok(self) -> None:
        """The health endpoint returns a successful JSON response."""
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})


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
        self.other_user = User.objects.create_user(
            username="other@example.com", password="test-password"
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
            title="Review project brief",
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.HIGH,
        )
        Task.objects.create(client=self.other_user, title="Private task")
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
