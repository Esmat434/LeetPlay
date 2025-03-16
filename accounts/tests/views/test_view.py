import uuid
from django.urls import reverse
from django.test import TestCase,Client
from unittest.mock import patch
from accounts.views.forms import (
    UserForm,UserUpdateForm,LoginForm,PasswordForgotForm,SetNewPasswordForm
)
from accounts.models import (
    CustomUser,Password_Token
)

class TestSignupView(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_user_is_logged_out(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code,200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_create_user_view_get_method_validate_response(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/signup.html')
        self.assertIsInstance(response.context['form'],UserForm)

    @patch("django_recaptcha.fields.ReCaptchaField.clean", return_value="dummy-recaptcha-response")
    def test_create_user_view_post_method_validate_response(self,mock_clean):
        data = {
            'username':'test','email':'testemail@gmail.com','first_name':'',
            'last_name':'','avatar':'','birth_date':'2000-03-04',
            'password':'Test111@','password2':'Test111@','recaptcha':'dummy-data'
        }
        response = self.client.post(reverse('signup'),data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('login'))

    @patch("django_recaptcha.fields.ReCaptchaField.clean", return_value="dummy-recaptcha-response")
    def test_create_user_view_post_method_invalidate_birth_date(self,mock_clean):
        data = {
            'username':'test','email':'testemail@gmail.com','first_name':'','last_name':'',
            'avatar':'','birth_date':'2025-03-01','password':'Test111@','password2':'Test111@',
            'recaptcha':'dummy-data'
        }
        response = self.client.post(reverse('signup'),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/signup.html')
        self.assertIsInstance(response.context['form'],UserForm)
    
    @patch("django_recaptcha.fields.ReCaptchaField.clean", return_value="dummy-recaptcha-response")
    def test_create_user_view_post_method_invaladate_password(self,mock_clean):
        data = {
            'username':'test','email':'testemail@gmail.com','first_name':'','last_name':'',
            'avatar':'','birth_date':'2000-03-01','password':'Test111@','password2':'Test123@'
        }
        response = self.client.post(reverse('signup'),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/signup.html')
        self.assertIsInstance(response.context['form'],UserForm)
    
class TestUpdateUserView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'test',email = 'testemail@gmail.com',birth_date = '2000-03-04',
            password = 'Test111@'
        )
        self.client.login(username = 'test',password = 'Test111@')
    
    def test_user_if_logged_in(self):
        response = self.client.get(reverse('user-update'))
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_update_user_view_get_method_validate_response(self):
        response = self.client.get(reverse('user-update'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/updateAccount.html')
        self.assertIsInstance(response.context['form'],UserUpdateForm)
    
    def test_update_user_view_get_method_invalidate_response(self):
        self.client.logout()
        response = self.client.get(reverse('user-update'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('login'))

    def test_update_user_view_post_method_validate_response(self):
        update_data = {
            'username':'testChange','email': 'testemail@gmail.com','first_name':'',
            'last_name':'','avatar':'','birth_date':'2000-03-02'
        }
        response = self.client.post(reverse('user-update'),update_data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('profile'))
    
    def test_update_user_view_post_method_invalidate_birth_date(self):
        data = {
            'username':'testChange','email': 'testemail@gmail.com','first_name':'',
            'last_name':'','avatar':'','birth_date':'2025-03-02'
        }
        response = self.client.post(reverse('user-update'),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/updateAccount.html')
        self.assertIsInstance(response.context['form'],UserUpdateForm)

class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'test',email = 'testemal@gmail.com',birth_date = '2000-03-4',
            password = 'Test111@'
        )
        self.data = {
            'username':'test','password':'Test111@','remember_me':True
        }

    def test_user_is_logged_out(self):
        response = self.client.get(reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_view_get_method_validated_response(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/login.html')
        self.assertIsInstance(response.context['form'],LoginForm)

    def test_login_view_post_method_validate_response(self):
        response = self.client.post(reverse('login'),self.data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))
    
    def test_login_view_post_method_invalid_password(self):
        data = {
            'username':'test','password':'dskjljkjdsl','remember_me':True
        }
        response = self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/login.html')
        self.assertIsInstance(response.context['form'],LoginForm)
    
    def test_login_view_post_method_invalid_authentication(self):
        data  = {
            'username':'testuser','password':'TestUser123@','remember_me':True
        }
        response = self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/login.html')
        self.assertIsInstance(response.context['form'],LoginForm)

class TestLogoutView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'test',email = 'testemail@gmail.com',birth_date = '2000-03-04',
            password = 'Test111@'
        )
        self.client.login(
            username = 'test', password = 'Test111@'
        )
    
    def test_user_is_logged_in(self):
        response = self.client.get(reverse('logout'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_logout_view_get_method(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/logout.html')
    
    def test_logout_post_method(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))

class TestProfileView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'test', email = 'testemail@gmail.com',
            birth_date = '2000-03-01',password = 'Test111@'
        )
        self.client.login(username = 'test', password = 'Test111@')
    
    def test_user_is_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_profile_view_get_method(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/profile.html')
        self.assertEqual(response.context['user'],self.user)


class PasswordForgotView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'test', email = 'testemail@gmail.com', birth_date = '2000-02-03',
            password = 'Test111@'
        )

    def test_user_is_logged_out(self):
        response = self.client.get(reverse('password-forgot'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_password_forgot_view_get_method_validated_response(self):
        response = self.client.get(reverse('password-forgot'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/password_forgot.html')
        self.assertIsInstance(response.context['form'],PasswordForgotForm)
    
    def test_password_forgot_view_post_method_validated_response(self):
        data = {
            'email':'testemail@gmail.com'
        }
        response = self.client.post(reverse('password-forgot'),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/message.html')
    
    def test_password_forgot_view_post_method_invalid_response(self):
        data = {
            'email':'mistake@gmail.com'
        }
        response = self.client.post(reverse('password-forgot'),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/password_forgot.html')
        self.assertEqual(response.context['error'],'your email is invalid.')

class TestSetNewPasswordView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'test', email = 'testemail@gmail.com', birth_date = '2000-03-02',
            password = 'Test111@'
        )
        self.key = Password_Token.objects.create(
            user = self.user
        )

    def test_set_new_password_view_get_method_validated_response(self):
        response = self.client.get(reverse('set-password',args=[self.key.token]))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/set_password.html')
        self.assertIsInstance(response.context['form'],SetNewPasswordForm)
    
    def test_set_new_password_view_get_method_invalid_token(self):
        response = self.client.get(reverse('set-password',args=[uuid.uuid4()]))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/error.html')
        self.assertEqual(response.context['error'],'Your token is expired Please create another token.')
    
    def test_set_new_password_view_post_method_validated_reponse(self):
        data = {
            'password1':'Test123@',
            'password2':'Test123@'
        }
        response = self.client.post(reverse('set-password',args=[self.key.token]),data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('login'))
    
    def test_set_new_password_view_post_method_invalid_passwords(self):
        data = {
            'password1':'Test123@',
            'password2':'Fast111%'
        }
        response = self.client.post(reverse('set-password',args=[self.key.token]),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/set_password.html')
        self.assertIsInstance(response.context['form'],SetNewPasswordForm)
