from django.urls import reverse
from django.test import TestCase,Client
from accounts.models import CustomUser

class TestLoginrRequiresMixin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'test', email = 'test@gmail.com', birth_date = '2000-02-03',
            password = 'Test111@'
        )
    
    def test_view_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('login'))
    
    def test_view_with_login(self):
        self.client.login(username = 'test', password = 'Test111@')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/profile.html')
        self.assertEqual(response.context['user'],self.user)

class TestLogoutRequiresMixin(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username = 'test', email = 'test@gmail.com', birth_date = '2000-02-01',
            password = 'Test111@'
        )
        self.client.login(username = 'test', password = 'Test111@')
    
    def test_view_requires_logout(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse('home'))
    
    def test_view_with_logout(self):
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'accounts/login.html')