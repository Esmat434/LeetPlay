from django.urls import path
from .auth_views import (
    CreateUserView,
    UpdateUserView,
    LoginView,
    LogoutView,
    ProfileView,
    PasswrdForgotView,
    SetNewPasswordView
)

urlpatterns = [
    path("signup/", CreateUserView.as_view(), name="signup"),
    path("user/update/", UpdateUserView.as_view(), name="user-update"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "password-forgot/",
        PasswrdForgotView.as_view(),
        name="password-forgot",
    ),
    path(
        "set-password/<uuid:token>/", SetNewPasswordView.as_view(), name="set-password"
    ),
]
