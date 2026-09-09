from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from core.models import Project, ProjectInvitation, ProjectMembership, Task
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

    def __init__(
        self,
        *args: object,
        client: User,
        projects=None,
        **kwargs: object,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.fields["project"].queryset = (
            projects if projects is not None else Project.objects.filter(client=client)
        )

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


class ProjectInviteForm(forms.Form):
    """Invite an existing Client user to a project."""

    username = forms.CharField(
        max_length=150,
        label="Client username",
        help_text="Enter the username of an existing Client user.",
    )

    def __init__(
        self, *args: object, project: Project, inviter: User, **kwargs: object
    ):
        super().__init__(*args, **kwargs)
        self.project = project
        self.inviter = inviter

    def clean_username(self) -> str:
        """Validate that the target is an eligible, non-member Client user."""
        username = self.cleaned_data["username"]
        try:
            invitee = User.objects.get(username=username)
        except User.DoesNotExist as error:
            raise forms.ValidationError("Enter an existing Client username.") from error
        if invitee == self.inviter:
            raise forms.ValidationError("You cannot invite yourself.")
        if not invitee.groups.filter(name="Client").exists():
            raise forms.ValidationError("The user must be a Client user.")
        if ProjectMembership.objects.filter(
            project=self.project, user=invitee, is_active=True
        ).exists():
            raise forms.ValidationError(
                "This client already collaborates on the project."
            )
        if ProjectInvitation.objects.filter(
            project=self.project,
            invitee=invitee,
            status=ProjectInvitation.Status.PENDING,
        ).exists():
            raise forms.ValidationError("This client is already invited.")
        self.invitee = invitee
        return username


class ClientProfileForm(forms.ModelForm):
    """Validate personal fields a client may update on their profile."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
