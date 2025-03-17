import json
from rest_framework.authtoken.models import Token
from django.test import TestCase,RequestFactory
from django.urls import reverse
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.timezone import now,timedelta
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import JsonResponse

from accounts.middlewares.AutoLogout import AutoLogoutMiddleware
from accounts.middlewares.ExceptionHandling import ExceptionHandlingMiddleware
from accounts.middlewares.MaintenanceMode import MaintenanceModeMiddleware
from accounts.middlewares.RateLimiting import RateLimitingMiddleware
from accounts.middlewares.Security import ScurityMiddleware

User = get_user_model()

class TestAutoLogoutMiddleware(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username = 'test',email = 'test@gmail.com', birth_date = "2000-03-01", 
            password= "Test111@"
        )
        
        self.token = Token.objects.create(user = self.user)
        
        self.token.created = now() - timedelta(days=11)
        self.token.save()

    def test_auto_logged_out_api_validate(self):
        request = self.factory.get(reverse('api-profile'))
        request.user = self.user
        request.META['HTTP_AUTHORIZATION'] = f"Bearer {self.token.key}"
        response = AutoLogoutMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        self.assertEqual(response.status_code,401)
        data = json.loads(response.content)
        self.assertEqual(data['error'],"Token Expired.")
    
    
    def test_auto_logged_out_api_invalid(self):
        request = self.factory.get(reverse('api-profile'))
        request.user = self.user
        self.token.created = now()
        self.token.save()
        request.META['HTTP_AUTHORIZATION'] = f"Bearer {self.token.key}"
        response = AutoLogoutMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        self.assertEqual(response.status_code,200)
        data = json.loads(response.content)
        self.assertEqual(data['message'],"ok")
    
    def test_auto_logged_out_users_validate(self):
        request = self.factory.get(reverse('profile'))
        self.user.last_login = now() - timedelta(days=11)
        self.user.save()
        request.user = self.user
        
        middleware = SessionMiddleware(lambda req:JsonResponse({"message":"ok"}))
        middleware.process_request(request)
        request.session.save()

        response = AutoLogoutMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        self.assertEqual(response.status_code,401)
    
    def test_auto_logged_out_users_invalid(self):
        request = self.factory.get(reverse('profile'))
        self.user.last_login = now()
        self.user.save()
        request.user = self.user

        response = AutoLogoutMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        self.assertEqual(response.status_code,200)
        data = json.loads(response.content)
        self.assertEqual(data["message"],"ok")

class TestExceptionHandlingMiddleware(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_exception_handling_middleware_validate(self):
        def error_view(request):
            raise ValueError("Something went wrong!") 
        
        request = self.factory.get(reverse('api-profile'))
        response = ExceptionHandlingMiddleware(error_view)(request)
        self.assertEqual(response.status_code,500)
        data = json.loads(response.content)
        self.assertEqual(data['error'],"An unexpected error occurred.")
        self.assertEqual(data['details'],"Something went wrong!")
    
    def test_exception_handling_middleware_invalid(self):
        request = self.factory.get(reverse('api-profile'))
        response = ExceptionHandlingMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        self.assertEqual(response.status_code,200)
        data = json.loads(response.content)
        self.assertEqual(data['message'],"ok")

class TestMaintenaneceModeMiddleware(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_maintenance_mode_validate(self):
        settings.MAINTENANCE_MODE = True
        request = self.factory.get('/api/token/')
        response = MaintenanceModeMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        self.assertEqual(response.status_code,503)
    
    def test_maintenence_mode_invalid(self):
        settings.MAINTENANCE_MODE = False
        request = self.factory.get('/api/token/')
        response = MaintenanceModeMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        self.assertEqual(response.status_code,200)
        data = json.loads(response.content)
        self.assertEqual(data["message"],"ok")

class TestRateLimitingMiddleware(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        cache.clear()
    
    def test_rate_limit_validate(self):
        request = self.factory.get(reverse('api-profile'))

        for i in range(100):
            response = RateLimitingMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        response = RateLimitingMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        self.assertEqual(response.status_code,403)
    
    def test_rate_limit_invalid(self):
        request = self.factory.get(reverse('api-profile'))

        for i in range(99):
            response = RateLimitingMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        response = RateLimitingMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        self.assertEqual(response.status_code,200)
        data = json.loads(response.content)
        self.assertEqual(data['message'],"ok")

class TestSecurityMiddleware(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_scurity_validate(self):
        request = self.factory.get('/api/token/')
        response = ScurityMiddleware(lambda req:JsonResponse({"message":"ok"}))(request)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response["X-Content-Type-Options"],"nosniff")
        self.assertEqual(response["X-Frame-Options"],"DENY")
        self.assertEqual(response["X-XSS-Protection"],"1; mode=block")
        self.assertEqual(response["Cache-Control"],"no-store, no-cache, must-revalidate, max-age=0")
        self.assertEqual(response["Pragma"],"no-cache")
        self.assertEqual(response["Expires"],"0")
        self.assertEqual(response["Referrer-Policy"],"strict-origin-when-cross-origin")