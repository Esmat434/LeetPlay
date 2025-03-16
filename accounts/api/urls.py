from django.urls import path
from .views import (
    CreateUserView,GetUpdateUserView,LoginView,LogoutView,ProfileView,PasswrdForgotView,
    SetNewPasswordView
)

urlpatterns = [
    path('api/signup/',CreateUserView.as_view(),name='api-signup'),
    path('api/user-update/',GetUpdateUserView.as_view(),name='api-user-update'),
    path('api/login/',LoginView.as_view(),name='api-login'),
    path('api/logout/',LogoutView.as_view(),name='api-logout'),
    path('api/profile/',ProfileView.as_view(),name='api-profile'),
    path('api/password-forgot/',PasswrdForgotView.as_view(),name='api-password-forgot'),
    path('api/set-new-password/<uuid:token>/',SetNewPasswordView.as_view(),name='api-set-new-password')
]