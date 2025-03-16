from django.urls import reverse
from django.test import TestCase,Client
from unittest.mock import patch
from accounts.models import CustomUser,Password_Token

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    @patch("django_recaptcha.fields.ReCaptchaField.clean", return_value="dummy-recaptcha-response")
    def test_user_can_registeration_login_and_logout(self,mock_clean):
        data = {
            "username": "testuser",
            "email": "test@gmail.com",
            'birth_date':'2000-03-01',
            "password": "Test111@",
            "password2": "Test111@",
            "recaptcha": "dummy-recaptcha-response"  
        }
        response = self.client.post(reverse('signup'),data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('login'))

class UserLoginLogout(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = 'test',email = 'test@gmail.com',birth_date = '2000-03-02',
            password = 'Test111@'
        )
    
    def test_user_can_login_and_logout(self):
        # login user
        data = {
            'username':'test','password':'Test111@','remember_me':True
        }
        response = self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))

        # logout user
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))

class UserProfileUpdateAccount(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'test',email = 'test@gmail.com',birth_date = '2000-03-01',
            password = 'Test111@'
        )
        self.client.login(username = 'test', password = 'Test111@')
    
    def test_user_can_check_profile_and_update_account(self):
        # check profile
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/profile.html')
        self.assertEqual(response.context['user'],self.user)

        # update account
        data = {
            'username':'testChange','email':'test@gmail.com','first_name':'','last_name':'',
            'avatar':'','birth_date':'2000-03-02'
        }
        response = self.client.post(reverse('user-update'),data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('profile'))

class PasswordForgotSetNewPassword(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'test', email = 'test@gmail.com', birth_date = '2000-03-01',
            password = 'Test111@'
        )
        self.key = Password_Token.objects.create(
            user = self.user
        )
    
    def test_password_forgot_and_set_new_password(self):
        # password forgot
        data = {
            'email':'test@gmail.com'
        }
        response = self.client.post(reverse('password-forgot'),data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/message.html')

        # set new password
        data = {
            'password1':'Test123@',
            'password2':'Test123@'
        }
        response = self.client.post(reverse('set-password',args=[self.key.token]),data)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('login'))