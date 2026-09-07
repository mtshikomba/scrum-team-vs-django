from django.http import HttpRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count, QuerySet
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)

from core.forms import ClientRegistrationForm, TaskForm
from core.models import Task


class ClientAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restrict a view to authenticated users in the Client group."""

    login_url = "/accounts/login/"

    def test_func(self) -> bool:
        """Return whether the current user has client access."""
        return self.request.user.groups.filter(name="Client").exists()


class ClientRegistrationView(CreateView):
    """Render and process the public client registration form."""

    form_class = ClientRegistrationForm
    template_name = "registration/register.html"
    success_url = "/accounts/login/"


class ClientLandingPageView(ClientAccessMixin, TemplateView):
    """Render the authenticated client's task management landing page."""

    template_name = "core/client_landing.html"

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


class ClientTaskCreateView(ClientAccessMixin, CreateView):
    """Create a task owned by the authenticated client."""

    model = Task
    form_class = TaskForm
    template_name = "core/task_form.html"
    success_url = reverse_lazy("client-landing")

    def form_valid(self, form: TaskForm):
        """Set task ownership from the authenticated user, never form data."""
        form.instance.client = self.request.user
        return super().form_valid(form)


class ClientTaskQuerysetMixin(ClientAccessMixin):
    """Limit task detail, update, and delete operations to task owners."""

    def get_queryset(self) -> QuerySet[Task]:
        """Return only tasks owned by the authenticated client."""
        return Task.objects.filter(client=self.request.user)


class ClientTaskDetailView(ClientTaskQuerysetMixin, DetailView):
    """Display one task owned by the authenticated client."""

    model = Task
    template_name = "core/task_detail.html"


class ClientTaskUpdateView(ClientTaskQuerysetMixin, UpdateView):
    """Update one task owned by the authenticated client."""

    model = Task
    form_class = TaskForm
    template_name = "core/task_form.html"

    def get_success_url(self) -> str:
        """Return the updated task detail route."""
        return self.object.get_absolute_url()


class ClientTaskDeleteView(ClientTaskQuerysetMixin, DeleteView):
    """Delete one task owned by the authenticated client."""

    model = Task
    template_name = "core/task_confirm_delete.html"
    success_url = reverse_lazy("client-landing")


class HealthCheckView(View):
    """Return a small response that confirms the application is running."""

    def get(self, request: HttpRequest) -> JsonResponse:
        """Return the current application health status."""
        return JsonResponse({"status": "ok"})
