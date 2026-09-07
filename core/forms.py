from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


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
