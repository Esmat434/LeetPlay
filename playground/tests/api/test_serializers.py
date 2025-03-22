from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from playground.models import (
    Question
)

from playground.api.serializers import (
    QuestionSerializer,SolvedSerializer
)

User = get_user_model()

class TestQuestionSerializer(APITestCase):
    def test_question_serializer_validate_data(self):
        data = {
            "title":"test","link":"https://test.com","category":"Easy","tag":"Array"
        }
        serializer = QuestionSerializer(data = data)
        self.assertTrue(serializer.is_valid())

class TestSolvedSerializer(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "test",email = "test@gmail.com", birth_date = "2000-03-01",
            password = "Test111@"
        )
        self.question = Question.objects.create(title = "test q",link = "www.testq.com",
                                                category = "Easy",tag = "Array") 
    def test_solved_serializer_validate_data(self):
        data = {
            "user":"test",
            "question":1
        }
        serializer = SolvedSerializer(data = data)
        self.assertTrue(serializer.is_valid())