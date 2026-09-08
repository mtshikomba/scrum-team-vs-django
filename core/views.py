from django.http import HttpRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count, QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)

from core.forms import ClientRegistrationForm, ProjectForm, TaskForm
from core.models import Project, Task


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

    def get_projects(self) -> QuerySet[Project]:
        """Return only projects owned by the authenticated client."""
        return Project.objects.filter(client=self.request.user).annotate(
            task_count=Count("tasks")
        )

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
                "projects": self.get_projects(),
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

    def dispatch(self, request: HttpRequest, *args: object, **kwargs: object):
        """Send clients to project creation until they have a project."""
        if not request.user.is_authenticated or not self.test_func():
            return super().dispatch(request, *args, **kwargs)
        if not Project.objects.filter(client=request.user).exists():
            return redirect("project-create")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self) -> dict[str, object]:
        """Limit selectable projects to those owned by the client."""
        kwargs = super().get_form_kwargs()
        kwargs["client"] = self.request.user
        return kwargs

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

    def get_form_kwargs(self) -> dict[str, object]:
        """Limit selectable projects to those owned by the client."""
        kwargs = super().get_form_kwargs()
        kwargs["client"] = self.request.user
        return kwargs

    def get_success_url(self) -> str:
        """Return the updated task detail route."""
        return self.object.get_absolute_url()


class ClientTaskDeleteView(ClientTaskQuerysetMixin, DeleteView):
    """Delete one task owned by the authenticated client."""

    model = Task
    template_name = "core/task_confirm_delete.html"
    success_url = reverse_lazy("client-landing")


class ClientProjectQuerysetMixin(ClientAccessMixin):
    """Limit project views to projects owned by the authenticated client."""

    def get_queryset(self) -> QuerySet[Project]:
        """Return only projects owned by the authenticated client."""
        return Project.objects.filter(client=self.request.user).annotate(
            task_count=Count("tasks")
        )


class ClientProjectListView(ClientProjectQuerysetMixin, TemplateView):
    """Display the authenticated client's projects."""

    template_name = "core/project_list.html"

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Add the client's projects to the page context."""
        context = super().get_context_data(**kwargs)
        context["projects"] = self.get_queryset()
        return context


class ClientProjectCreateView(ClientAccessMixin, CreateView):
    """Create a project owned by the authenticated client."""

    model = Project
    form_class = ProjectForm
    template_name = "core/project_form.html"

    def get_form_kwargs(self) -> dict[str, object]:
        """Pass the authenticated client to project validation."""
        kwargs = super().get_form_kwargs()
        kwargs["client"] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Set project ownership from the authenticated user."""
        form.instance.client = self.request.user
        return super().form_valid(form)


class ClientProjectDetailView(ClientProjectQuerysetMixin, DetailView):
    """Display one project and its owned tasks."""

    model = Project
    template_name = "core/project_detail.html"


class ClientProjectUpdateView(ClientProjectQuerysetMixin, UpdateView):
    """Update a project owned by the authenticated client."""

    model = Project
    form_class = ProjectForm
    template_name = "core/project_form.html"

    def get_form_kwargs(self) -> dict[str, object]:
        """Pass the authenticated client to project validation."""
        kwargs = super().get_form_kwargs()
        kwargs["client"] = self.request.user
        return kwargs


class ClientProjectDeleteView(ClientProjectQuerysetMixin, DeleteView):
    """Delete a project owned by the authenticated client."""

    model = Project
    template_name = "core/project_confirm_delete.html"
    success_url = reverse_lazy("project-list")


class HealthCheckView(View):
    """Return a small response that confirms the application is running."""

    def get(self, request: HttpRequest) -> JsonResponse:
        """Return the current application health status."""
        return JsonResponse({"status": "ok"})
