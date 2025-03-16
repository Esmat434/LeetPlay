import uuid
from django.test import SimpleTestCase
from django.urls import reverse,resolve

from accounts.api.views import (
    CreateUserView,GetUpdateUserView,LoginView,LogoutView,ProfileView,PasswrdForgotView,
    SetNewPasswordView
)

class TestUrls(SimpleTestCase):
    def test_create_user_resolves(self):
        response = reverse('api-signup')
        self.assertEqual(resolve(response).func.view_class,CreateUserView)
    
    def test_get_update_user_resolves(self):
        response = reverse('api-user-update')
        self.assertEqual(resolve(response).func.view_class,GetUpdateUserView)
    
    def test_get_login_resolves(self):
        response = reverse('api-login')
        self.assertEqual(resolve(response).func.view_class,LoginView)
    
    def test_logout_resolves(self):
        response = reverse('api-logout')
        self.assertEqual(resolve(response).func.view_class,LogoutView)
    
    def test_profile_resolves(self):
        response = reverse('api-profile')
        self.assertEqual(resolve(response).func.view_class,ProfileView)
    
    def test_password_forgot_resolves(self):
        response = reverse('api-password-forgot')
        self.assertEqual(resolve(response).func.view_class,PasswrdForgotView)
    
    def test_set_new_password_resolves(self):
        response = reverse('api-set-new-password',args=[uuid.uuid4()])
        self.assertEqual(resolve(response).func.view_class,SetNewPasswordView)