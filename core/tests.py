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
