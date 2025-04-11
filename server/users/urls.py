# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import api_views

app_name = "users"

urlpatterns = [
    # Web interface URLs
    path("signup/", views.SignUp.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # Password reset URLs
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # User profile URLs
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    # API URLs
    path(
        "api/register/", api_views.UserRegistrationView.as_view(), name="api-register"
    ),
    path("api/token/", api_views.CustomAuthToken.as_view(), name="api-token"),
    path("api/profile/", api_views.UserProfileView.as_view(), name="api-profile"),
]
