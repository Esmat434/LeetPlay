from django.utils.timezone import now
from django.contrib.auth import logout
from django.http import JsonResponse
from datetime import timedelta
from rest_framework.authtoken.models import Token

class AutoLogoutMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        if request.user.is_authenticated and not request.path.startswith('/api/'):
            last_login = request.user.last_login
            if last_login and (now() - last_login) > timedelta(days=10):
                logout(request)
                return JsonResponse({"error":"You logged out."},status = 401)
        
        if request.path.startswith('/api/'):
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token_key = auth_header.split(" ")[1]
                try:
                    token = Token.objects.get(key = token_key)
                    if (now() - token.created) > timedelta(days=10):
                        token.delete()
                        return JsonResponse({"error":"Token Expired."},status=401)
                except Token.DoesNotExist:
                    return JsonResponse({'error': 'Invalid Token'}, status=401)
        return self.get_response(request)