from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.conf import settings
from .models import UserProfile  # Add this import

User = get_user_model()


class UserCreateForm(UserCreationForm):
    """Form for creating new users with additional fields."""

    phone = forms.CharField(
        max_length=15, required=False, help_text="Enter your phone number."
    )

    # Get the choices from the model if possible, otherwise provide default choices
    try:
        user_type_choices = User.USER_TYPE_CHOICES
    except AttributeError:
        user_type_choices = ((1, "Student"), (2, "Instructor"), (3, "Admin"))

    user_type = forms.ChoiceField(choices=user_type_choices, required=True)

    class Meta:
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"
        self.fields["email"].label = "Email Address"
        self.fields["phone"].label = "Phone Number"
        self.fields["user_type"].label = "Register as:"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data.get("phone", "")

        # Only set user_type if the field exists in the model
        if hasattr(user, "user_type"):
            user.user_type = self.cleaned_data.get("user_type")

        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    """Form for editing basic user information."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True


class UserProfileForm(forms.ModelForm):
    """Form for editing the user profile specific information."""

    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = UserProfile
        fields = []  # Add other fields from UserProfile if needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("instance") and hasattr(kwargs["instance"], "user"):
            if hasattr(kwargs["instance"].user, "phone"):
                self.initial["phone"] = kwargs["instance"].user.phone

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Save the phone number to the related User model
            if hasattr(profile.user, "phone"):
                profile.user.phone = self.cleaned_data.get("phone", "")
                profile.user.save()
            profile.save()
        return profile
