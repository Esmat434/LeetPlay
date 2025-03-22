from rest_framework.permissions import BasePermission
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token

class IsAuthenticatedAndSuperuserPermission(BasePermission):
    message = "No Token Provided."

    def has_permission(self, request, view):
        auth_token = get_authorization_header(request).decode('utf-8')
        token_key = auth_token.split(" ")[1] if " " in auth_token else None

        if not token_key:
            self.message = "No Token Provided."
            return False

        try:
            token = Token.objects.get(key=token_key)
            request.user = token.user
        except Token.DoesNotExist:
            self.message = "Invalid Token."
            return False
        
        methods = ["POST", "PUT", "DELETE"]
        if request.method in methods and not request.user.is_superuser:
            self.message = "You don't have permission."
            return False

        return True

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        auth_token = get_authorization_header(request).decode("utf-8")
        token_key = auth_token.split(" ")[1] if " " in auth_token else None

        if not token_key:
            return False
        
        try:
            token = Token.objects.get(key = token_key)
            request.user = token.user
            return True
        except Token.DoesNotExist:
            return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET","HEAD","OPTIONS"]:
            return True
        return obj.user == request.user