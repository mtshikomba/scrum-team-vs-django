from django.contrib.auth.models import User
from django.db import models


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
    title = models.CharField(
        max_length=200,
        verbose_name="title",
        help_text="A short description of the task.",
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
