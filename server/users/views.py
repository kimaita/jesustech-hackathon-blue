from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login

from .forms import UserCreateForm, UserEditForm, UserProfileForm
from .models import UserProfile, User


# Create your views here.
class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("users:login")
    template_name = "users/signup.html"


# Homepage view
class HomePage(TemplateView):
    template_name = "index.html"


@login_required
def profile_view(request):
    """View for displaying the user profile"""
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    context = {"user": user, "profile": profile}
    return render(request, "users/profile.html", context)


@login_required
def edit_profile(request):
    """View for editing the user profile"""
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("users:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "users/edit_profile.html", context)
