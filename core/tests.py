from django.test import TestCase


class HealthCheckViewTests(TestCase):
    """Verify that the initial application health endpoint is available."""

    def test_health_check_returns_ok(self) -> None:
        """The health endpoint returns a successful JSON response."""
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
