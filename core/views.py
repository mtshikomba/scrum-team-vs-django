from django.http import HttpRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count, QuerySet
from django.views import View
from django.views.generic import TemplateView

from core.models import Task


class ClientLandingPageView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Render the authenticated client's task management landing page."""

    template_name = "core/client_landing.html"
    login_url = "/accounts/login/"

    def test_func(self) -> bool:
        """Allow access only to users in the Client group."""
        return self.request.user.groups.filter(name="Client").exists()

    def get_tasks(self) -> QuerySet[Task]:
        """Return only tasks owned by the authenticated client."""
        return Task.objects.filter(client=self.request.user)

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Build task summary and task list data for the landing page."""
        context = super().get_context_data(**kwargs)
        tasks = self.get_tasks()
        status_counts = tasks.values("status").annotate(total=Count("id"))
        counts = {item["status"]: item["total"] for item in status_counts}
        context.update(
            {
                "tasks": tasks,
                "task_counts": {
                    "outstanding": counts.get(Task.Status.OUTSTANDING, 0),
                    "in_progress": counts.get(Task.Status.IN_PROGRESS, 0),
                    "completed": counts.get(Task.Status.COMPLETED, 0),
                },
            }
        )
        return context


class HealthCheckView(View):
    """Return a small response that confirms the application is running."""

    def get(self, request: HttpRequest) -> JsonResponse:
        """Return the current application health status."""
        return JsonResponse({"status": "ok"})
