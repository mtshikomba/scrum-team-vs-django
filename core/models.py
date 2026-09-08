from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from core.sanitization import clean_rich_text


class Project(models.Model):
    """A project owned by a client and containing the client's tasks."""

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="client_projects",
        verbose_name="client",
        help_text="The client user who owns this project.",
        db_index=True,
    )
    name = models.CharField(
        max_length=200,
        verbose_name="name",
        help_text="A name that identifies the project.",
    )
    description = models.TextField(
        blank=True,
        verbose_name="description",
        help_text="Optional context about the project.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created at",
        help_text="When the project was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="updated at",
        help_text="When the project was last changed.",
    )

    class Meta:
        ordering = ("-updated_at", "name")
        verbose_name = "project"
        verbose_name_plural = "projects"
        constraints = [
            models.UniqueConstraint(
                fields=("client", "name"), name="unique_project_name_per_client"
            )
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        """Return the client-facing detail URL for this project."""
        from django.urls import reverse

        return reverse("project-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    """A task owned by a client user."""

    class Status(models.TextChoices):
        OUTSTANDING = "outstanding", "Outstanding"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="client_tasks",
        verbose_name="client",
        help_text="The client user who owns this task.",
        db_index=True,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="project",
        help_text="The project containing this task.",
        db_index=True,
    )
    title = models.CharField(
        max_length=200,
        verbose_name="title",
        help_text="A short description of the task.",
    )
    description = CKEditor5Field(
        blank=True,
        config_name="default",
        verbose_name="description",
        help_text="Rich-text context and notes for the task.",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OUTSTANDING,
        verbose_name="status",
        help_text="The current workflow status of the task.",
        db_index=True,
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="priority",
        help_text="The relative urgency of the task.",
    )
    due_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="due date",
        help_text="The date by which the task should be completed.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="updated at",
        help_text="The last time the task was changed.",
    )

    class Meta:
        ordering = ("-updated_at", "title")
        verbose_name = "task"
        verbose_name_plural = "tasks"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        """Return the client-facing detail URL for this task."""
        from django.urls import reverse

        return reverse("task-detail", kwargs={"pk": self.pk})

    def get_safe_description(self) -> str:
        """Return the task description with unsafe markup removed."""
        return clean_rich_text(self.description)
