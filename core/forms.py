from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from core.models import Project, Task
from core.sanitization import clean_rich_text


class ClientRegistrationForm(UserCreationForm):
    """Create a regular user and grant membership in the Client group."""

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit: bool = True) -> User:
        """Save the user and assign the standard client authorization group."""
        user = super().save(commit=commit)
        if commit:
            client_group, _ = Group.objects.get_or_create(name="Client")
            user.groups.add(client_group)
        return user


class TaskForm(forms.ModelForm):
    """Validate client-editable task fields."""

    class Meta:
        model = Task
        fields = ("project", "title", "description", "status", "priority", "due_date")
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args: object, client: User, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(client=client)

    def clean_description(self) -> str:
        """Sanitize rich-text content before saving it."""
        return clean_rich_text(self.cleaned_data.get("description", ""))


class ProjectForm(forms.ModelForm):
    """Validate project names for the authenticated client."""

    class Meta:
        model = Project
        fields = ("name", "description")

    def __init__(self, *args: object, client: User, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.client_user = client

    def clean_name(self) -> str:
        """Reject duplicate project names for the current client."""
        name = self.cleaned_data["name"]
        duplicate_projects = Project.objects.filter(client=self.client_user, name=name)
        if self.instance.pk:
            duplicate_projects = duplicate_projects.exclude(pk=self.instance.pk)
        if duplicate_projects.exists():
            raise forms.ValidationError("You already have a project with this name.")
        return name


class ClientProfileForm(forms.ModelForm):
    """Validate personal fields a client may update on their profile."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
