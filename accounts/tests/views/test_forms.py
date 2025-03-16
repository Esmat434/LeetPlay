from django.test import TestCase
from unittest.mock import patch
from accounts.views.forms import (
    UserForm,UserUpdateForm,LoginForm,PasswordForgotForm,SetNewPasswordForm
)
from accounts.models import CustomUser

class TestUserForm(TestCase):
    @patch("django_recaptcha.fields.ReCaptchaField.clean", return_value="dummy-recaptcha-response")
    def test_user_form_validated_data(self, mock_clean):
        data = {
            "username": "testuser",
            "email": "test@gmail.com",
            'birth_date':'2000-03-01',
            "password": "Test111@",
            "password2": "Test111@",
            "recaptcha": "dummy-recaptcha-response"  
        }
        form = UserForm(data)
        self.assertTrue(form.is_valid())
    
    @patch("django_recaptcha.fields.ReCaptchaField.clean", return_value = "dummy-data")
    def test_user_form_invalid_birth_date(self,mock_clean):
        data = {
            'username':'test','email':'test@gmail.com','birth_date':'2025-01-02',
            'password':'Test111@','password2':'Test111@','recaptcha':'dummy-data'
        }
        form = UserForm(data)
        self.assertFalse(form.is_valid())
    
    @patch("django_recaptcha.fields.ReCaptchaField.clean", return_value = "dummy-data")
    def test_user_form_invalid_match_passwords(self,mock_clean):
        data = {
            'username':'test','email':'test@gmail.com','birth_date':'2000-03-01',
            'password':'Test111@','password2':'Mistake11@','recaptcha':'dummy-data'
        }
        form = UserForm(data)
        self.assertFalse(form.is_valid())
    
    @patch("django_recaptcha.fields.ReCaptchaField.clean", return_value = "dummy_data")
    def test_user_form_invalid_password_validation(self,mock_clean):
        data = {
            'username':'test','email':'test@gmail.com','birth_date':'2000-02-03',
            'password':'test','password2':'test','recaptcha':'dummy-data'
        }
        form = UserForm(data)
        self.assertFalse(form.is_valid())

class TestUserUpdateForm(TestCase):
    def test_user_update_form_validated_data(self):
        data = {
            'username':'test','email':'test@gmail.com','first_name':'','last_name':'',
            'avatar':'','birth_date':'2000-03-01'
        }
        form = UserUpdateForm(data)
        self.assertTrue(form.is_valid())
    
    def test_user_update_form_invalid_birth_date(self):
        data = {
            'username':'test','email':'test@gmail.com','first_name':'','last_name':'',
            'avatar':'','birth_date':'2024-03-01'
        }
        form = UserUpdateForm(data)
        self.assertFalse(form.is_valid())

class TestLoginForm(TestCase):
    def test_login_form_validated_data(self):
        data = {
            'username':'test','password':'Test111@','remember_me':True
        }
        form = LoginForm(data)
        self.assertTrue(form)
    
    def test_login_form_invalid_password(self):
        data = {
            'username':'test','password':'mistake','remember_me':True
        }
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

class TestPasswordForgotForm(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = 'test',email = 'test@gmail.com',birth_date = '2000-03-01',password = 'Test111@'
        )
    
    def test_password_forgot_form_validated_data(self):
        data = {
            'email':'test@gmail.com'
        }
        form = PasswordForgotForm(data)
        self.assertTrue(form.is_valid())

    def test_password_forgot_form_invalid_email(self):
        data = {
            'email':'mistake@gmail.com'
        }
        form = PasswordForgotForm(data)
        self.assertFalse(form.is_valid())

class TestSetNewPasswordForm(TestCase):
    def test_set_new_password_form_validated_data(self):
        data = {
            'password1':'Test111@',
            'password2':'Test111@'
        }
        form = SetNewPasswordForm(data)
        self.assertTrue(form.is_valid())
    
    def test_set_new_password_form_invalid_match_password(self):
        data = {
            'password1':'Test123@',
            'Password2':'Mistake123@'
        }
        form = SetNewPasswordForm(data)
        self.assertFalse(form.is_valid())
    
    def test_set_new_password_form_invalid_password_validation(self):
        data = {
            'password1':'test',
            'password2':'test'
        }
        form = SetNewPasswordForm(data)
        self.assertFalse(form.is_valid())