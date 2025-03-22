from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class TestQuestionListCreatView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username = 'test',email = "test@gmail.com",birth_date = "2000-03-01",
            password = "Test111@"
        )
        self.client.login(username = "test",password = "Test111@")
    
    def test_question_list_create_view_validate_get_method(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home/playground.html')
    
    def test_question_list_created_view_validate_post_method(self):
        data = {
            'category':"Easy",
            'tag':"Array"
        }
        response = self.client.post(reverse('home'),data=data)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home/playground.html')