from django.http import Http404, HttpRequest, JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count, F, Q, QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)
from django.contrib.auth.views import PasswordChangeView
from typing import Iterable

from core.forms import (
    ClientProfileForm,
    ClientRegistrationForm,
    ProjectForm,
    ProjectInviteForm,
    TaskForm,
)
from django.contrib.auth.models import User

from core.models import Project, ProjectInvitation, ProjectMembership, Task


def build_task_lanes(tasks: Iterable[Task]) -> list[dict[str, object]]:
    """Group tasks into the stable status order used by task boards."""
    return [
        {
            "value": status.value,
            "label": status.label,
            "tasks": [task for task in tasks if task.status == status.value],
        }
        for status in Task.Status
    ]


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


class ClientProfileView(ClientAccessMixin, UpdateView):
    """Update personal fields for the authenticated client."""

    form_class = ClientProfileForm
    template_name = "core/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None) -> User:
        """Return only the currently authenticated user."""
        return self.request.user


class ClientPasswordChangeView(ClientAccessMixin, PasswordChangeView):
    """Change the password for the authenticated client."""

    form_class = PasswordChangeForm
    template_name = "core/password_change.html"
    success_url = reverse_lazy("profile")

    def get_form_kwargs(self) -> dict[str, object]:
        """Bind the password form to the authenticated user."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


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
        context["projects"] = self.get_projects()
        context["tasks"] = tasks
        context["task_lanes"] = build_task_lanes(tasks)
        context["task_statuses"] = Task.Status.choices
        context["task_view_label"] = "Task list"
        context["task_counts"] = {
            "outstanding": counts.get(Task.Status.OUTSTANDING, 0),
            "in_progress": counts.get(Task.Status.IN_PROGRESS, 0),
            "completed": counts.get(Task.Status.COMPLETED, 0),
        }
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
        if not accessible_projects(request.user).exists():
            return redirect("project-create")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self) -> dict[str, object]:
        """Limit selectable projects to those owned by the client."""
        kwargs = super().get_form_kwargs()
        kwargs["client"] = self.request.user
        kwargs["projects"] = accessible_projects(self.request.user)
        return kwargs

    def form_valid(self, form: TaskForm):
        """Set task ownership from the authenticated user, never form data."""
        form.instance.client = form.cleaned_data["project"].client
        return super().form_valid(form)


class ClientTaskQuerysetMixin(ClientAccessMixin):
    """Limit task detail, update, and delete operations to task owners."""

    def get_queryset(self) -> QuerySet[Task]:
        """Return tasks owned by or shared with the authenticated client."""
        return Task.objects.filter(
            Q(client=self.request.user)
            | Q(
                project__memberships__user=self.request.user,
                project__memberships__is_active=True,
            )
            | Q(project__client=self.request.user, client=F("project__client"))
        ).distinct()


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
        kwargs["projects"] = accessible_projects(self.request.user)
        return kwargs

    def get_success_url(self) -> str:
        """Return the updated task detail route."""
        return self.object.get_absolute_url()


class ClientTaskStatusView(ClientTaskQuerysetMixin, View):
    """Persist a status-lane move for an owned task."""

    def post(self, request: HttpRequest, pk: int) -> JsonResponse:
        """Update only the requested task status and return its label."""
        task = self.get_queryset().filter(pk=pk).first()
        if task is None:
            raise Http404

        status = request.POST.get("status")
        valid_statuses = {choice.value: choice.label for choice in Task.Status}
        if status not in valid_statuses:
            return JsonResponse({"error": "Invalid task status."}, status=400)

        task.status = status
        task.save(update_fields=["status", "updated_at"])
        return JsonResponse({"status": status, "label": valid_statuses[status]})


class ClientTaskDeleteView(ClientTaskQuerysetMixin, DeleteView):
    """Delete one task owned by the authenticated client."""

    model = Task
    template_name = "core/task_confirm_delete.html"
    success_url = reverse_lazy("client-landing")

    def get_queryset(self) -> QuerySet[Task]:
        """Return only tasks owned by the authenticated client for deletion."""
        return Task.objects.filter(client=self.request.user)


class ClientProjectQuerysetMixin(ClientAccessMixin):
    """Limit project views to projects owned by the authenticated client."""

    def get_queryset(self) -> QuerySet[Project]:
        """Return projects owned by or shared with the authenticated client."""
        return accessible_projects(self.request.user).annotate(
            task_count=Count("tasks")
        )


def accessible_projects(user: User) -> QuerySet[Project]:
    """Return projects the client owns or has actively joined."""
    return Project.objects.filter(
        Q(client=user) | Q(memberships__user=user, memberships__is_active=True)
    ).distinct()


class ClientProjectOwnerMixin(ClientAccessMixin):
    """Restrict project management to the immutable project owner."""

    def get_queryset(self) -> QuerySet[Project]:
        """Return only projects owned by the authenticated client."""
        return Project.objects.filter(client=self.request.user)


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

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Add stable status lanes for this project's tasks."""
        context = super().get_context_data(**kwargs)
        tasks = list(self.object.tasks.all())
        context["tasks"] = tasks
        context["task_lanes"] = build_task_lanes(tasks)
        context["task_statuses"] = Task.Status.choices
        context["task_view_label"] = "Project tasks"
        context["is_project_owner"] = self.object.client_id == self.request.user.id
        return context


class ClientProjectUpdateView(ClientProjectOwnerMixin, UpdateView):
    """Update a project owned by the authenticated client."""

    model = Project
    form_class = ProjectForm
    template_name = "core/project_form.html"

    def get_form_kwargs(self) -> dict[str, object]:
        """Pass the authenticated client to project validation."""
        kwargs = super().get_form_kwargs()
        kwargs["client"] = self.request.user
        return kwargs


class ClientProjectDeleteView(ClientProjectOwnerMixin, DeleteView):
    """Delete a project owned by the authenticated client."""

    model = Project
    template_name = "core/project_confirm_delete.html"
    success_url = reverse_lazy("project-list")


class ClientProjectInviteView(ClientProjectOwnerMixin, View):
    """Invite and list Client collaborators for an owned project."""

    def get(self, request: HttpRequest, pk: int):
        """Render the owner invitation form and current membership states."""
        project = get_object_or_404(self.get_queryset(), pk=pk)
        return render(
            request,
            "core/project_collaborators.html",
            {
                "project": project,
                "form": ProjectInviteForm(project=project, inviter=request.user),
                "invitations": project.invitations.select_related("invitee"),
                "memberships": project.memberships.filter(
                    is_active=True
                ).select_related("user"),
            },
        )

    def post(self, request: HttpRequest, pk: int):
        """Create a pending invitation for an eligible Client user."""
        project = get_object_or_404(self.get_queryset(), pk=pk)
        form = ProjectInviteForm(request.POST, project=project, inviter=request.user)
        if form.is_valid():
            ProjectInvitation.objects.create(
                project=project, inviter=request.user, invitee=form.invitee
            )
            return redirect(project.get_absolute_url())
        return render(
            request,
            "core/project_collaborators.html",
            {"project": project, "form": form, "invitations": [], "memberships": []},
        )


class ClientProjectInviteSuggestionsView(ClientProjectOwnerMixin, View):
    """Return eligible Client usernames for an owner's invite combobox."""

    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        """Return a small, privacy-filtered username result set."""
        project = get_object_or_404(self.get_queryset(), pk=pk)
        query = request.GET.get("q", "").strip()
        if query.startswith("@"):
            query = query[1:]

        active_ids = ProjectMembership.objects.filter(
            project=project, is_active=True
        ).values("user_id")
        pending_ids = ProjectInvitation.objects.filter(
            project=project, status=ProjectInvitation.Status.PENDING
        ).values("invitee_id")
        results = (
            User.objects.filter(groups__name="Client", username__icontains=query)
            .exclude(pk=request.user.pk)
            .exclude(pk__in=active_ids)
            .exclude(pk__in=pending_ids)
            .order_by("username")
            .values("username")[:10]
        )
        return JsonResponse({"results": list(results)})


class ClientProjectInvitationAcceptView(ClientAccessMixin, View):
    """Accept a pending invitation for its intended Client recipient."""

    def get(self, request: HttpRequest, token):
        """Render the pending invitation confirmation for its recipient."""
        invitation = self._get_invitation(request, token)
        return render(
            request, "core/project_invitation.html", {"invitation": invitation}
        )

    def post(self, request: HttpRequest, token):
        """Activate membership and consume the invitation token."""
        invitation = self._get_invitation(request, token)
        ProjectMembership.objects.update_or_create(
            project=invitation.project,
            user=request.user,
            defaults={"is_active": True},
        )
        invitation.status = ProjectInvitation.Status.ACCEPTED
        invitation.accepted_at = timezone.now()
        invitation.save(update_fields=["status", "accepted_at"])
        return redirect(invitation.project.get_absolute_url())

    def _get_invitation(self, request: HttpRequest, token) -> ProjectInvitation:
        """Return a pending invitation only to its intended recipient."""
        invitation = (
            ProjectInvitation.objects.filter(
                token=token,
                invitee=request.user,
                status=ProjectInvitation.Status.PENDING,
            )
            .select_related("project", "inviter")
            .first()
        )
        if invitation is None:
            raise Http404
        return invitation


class ClientProjectInvitationDeclineView(ClientAccessMixin, View):
    """Decline a pending invitation for its intended recipient."""

    def post(self, request: HttpRequest, token):
        """Mark the recipient's pending invitation as declined."""
        invitation = ProjectInvitation.objects.filter(
            token=token, invitee=request.user, status=ProjectInvitation.Status.PENDING
        ).first()
        if invitation is None:
            raise Http404
        invitation.status = ProjectInvitation.Status.DECLINED
        invitation.save(update_fields=["status"])
        return redirect("client-landing")


class ClientProjectInvitationRevokeView(ClientProjectOwnerMixin, View):
    """Revoke a pending invitation owned by the current project owner."""

    def post(self, request: HttpRequest, pk: int, invitation_id: int):
        """Mark a pending invitation as revoked."""
        project = get_object_or_404(self.get_queryset(), pk=pk)
        invitation = get_object_or_404(
            ProjectInvitation,
            pk=invitation_id,
            project=project,
            status=ProjectInvitation.Status.PENDING,
        )
        invitation.status = ProjectInvitation.Status.REVOKED
        invitation.save(update_fields=["status"])
        return redirect("project-invite", pk=project.pk)


class ClientProjectMemberRemoveView(ClientProjectOwnerMixin, View):
    """Remove an active collaborator without deleting project data."""

    def post(self, request: HttpRequest, pk: int, membership_id: int):
        """Deactivate an active project membership."""
        project = get_object_or_404(self.get_queryset(), pk=pk)
        membership = get_object_or_404(
            ProjectMembership,
            pk=membership_id,
            project=project,
            is_active=True,
        )
        membership.is_active = False
        membership.save(update_fields=["is_active"])
        return redirect("project-invite", pk=project.pk)


class HealthCheckView(View):
    """Return a small response that confirms the application is running."""

    def get(self, request: HttpRequest) -> JsonResponse:
        """Return the current application health status."""
        return JsonResponse({"status": "ok"})
