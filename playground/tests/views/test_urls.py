from django.test import SimpleTestCase,Client
from django.urls import reverse,resolve
from playground.views.code_view import (
    QuestionListCreateView
)

class TestUrls(SimpleTestCase):
    def setUp(self):
        self.client = Client()
    
    def test_home_url(self):
        response = reverse('home')
        self.assertEqual(resolve(response).func.view_class,QuestionListCreateView)