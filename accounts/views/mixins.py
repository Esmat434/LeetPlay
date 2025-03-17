from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.mixins import *


# this login required mixin check the auth token
class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)


# this is for those person want to go login page when already exists
class LogoutrequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.HOME_URL)
        return super().dispatch(request, *args, **kwargs)
