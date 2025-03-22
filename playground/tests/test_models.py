from django.test import TestCase
from django.contrib.auth import get_user_model

from playground.models import (
    Question,Solved
)

User = get_user_model()

class TestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username = "test",email = "test@gmail.com",birth_date = "2000-03-01",
            password = "Test111@"
        )
        self.question = Question.objects.create(
            title = "test",link = "https://test.com",category = "Easy",tag = "Array"
        )

    def test_question_model_validate_data(self):
        self.assertEqual(self.question.title,"test")
        self.assertEqual(self.question.link,"https://test.com")
    
    def test_solved_model_validate_data(self):
        solved = Solved.objects.create(user = self.user,question = self.question)
        self.assertEqual(solved.user,self.user)