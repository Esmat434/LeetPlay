from django.contrib.auth import login
from rest_framework.permissions import BasePermission
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


class IsAuthenticationToken(BasePermission):
    def has_permission(self, request, view):
        auth_header = get_authorization_header(request).decode("utf-8")
        token_key = auth_header.split(" ")[1] if " " in auth_header else None

        if not token_key:
            raise AuthenticationFailed({"detail": "No Token Provider."})

        try:
            token = Token.objects.get(key=token_key)
            login(request, token.user)
            return True
        except Token.DoesNotExist:
            raise AuthenticationFailed({"detail": "Invalid Token."})


class AllowAnyUser(BasePermission):
    def has_permission(self, request, view):
        return True
