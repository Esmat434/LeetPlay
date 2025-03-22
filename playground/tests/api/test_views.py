from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from rest_framework.authtoken.models import Token

from playground.models import (
    Question,Solved
)

User = get_user_model()

class TestQuestionGetPostView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(
            username = "test",email = "test@gmail.com", birth_date = "2000-03-01",
            password = "Test111@"
        )
        self.token = Token.objects.create(user = self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token.key}")
    
    def test_question_get_metohd_validate(self):
        response = self.client.get(reverse("question-get-post"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_question_post_method_validate(self):
        data = {
            "title":"test","link":"https://test.com","category":"Easy","tag":"Array"
        }
        response = self.client.post(reverse("question-get-post"),data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

class TestQuestionGetPutDeleteView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(
            username = "test",email = "test@gmail.com",birth_date = "2000-03-04",
            password = "Test111@"
        )
        self.token = Token.objects.create(user = self.superuser)
        self.question = Question.objects.create(
            title="test",link="https://test.com",category="Easy",tag="Array"
        )
        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token.key}")
    
    def test_question_get_method_validate(self):
        response = self.client.get(reverse("question-get-put-delete",args=[self.question.pk]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_question_get_method_invalid(self):
        response = self.client.get(reverse("question-get-put-delete",args=[0]))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_question_put_method_validate(self):
        data = {
            "category":"Hard"
        }
        response = self.client.put(reverse("question-get-put-delete",args=[self.question.pk]),data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_question_put_method_invalid(self):
        data = {
            "title":"change"
        }
        response = self.client.put(reverse("question-get-put-delete",args=[0]),data=data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_question_delete_method_validate(self):
        response = self.client.delete(reverse("question-get-put-delete",args=[self.question.pk]))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    
    def test_question_delete_method_invalid(self):
        response = self.client.delete(reverse("question-get-put-delete",args=[0]))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

class TestSolvedGetPostView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username = "test",email = "test@gmail.com",birth_date = "2000-03-01",
            password = "Test111@"
        )
        self.token = Token.objects.create(user = self.user)
        self.question = Question.objects.create(
            title = "test",link = "https://test.com",category = "Easy",tag = "Array"
        )
        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token.key}")
    
    def test_solved_get_method_validate(self):
        response = self.client.get(reverse("question-solved-get-post"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_solved_post_method_validate(self):
        data = {
            "question":self.question.pk
        }
        response = self.client.post(reverse("question-solved-get-post"),data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_solved_post_method_invalid(self):
        data = {
            "question":0
        }
        response = self.client.post(reverse("question-solved-get-post"),data=data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

class TestSolvedGetPutDeleteView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username = "test",email = "test@gmail.com",birth_date = "2000-03-01",
            password = "Test111@"
        )
        self.token = Token.objects.create(user = self.user)
        self.question = Question.objects.create(
            title = "test",link = "https://test.com",category = "Easy",tag = "Array"
        )
        self.solved = Solved.objects.create(
            user = self.user,question = self.question
            )
        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token.key}")
    
    def test_solved_get_method_validate(self):
        response = self.client.get(reverse("question-solved-get-put-delete",args=[self.solved.pk]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_solved_get_method_invalid(self):
        response = self.client.get(reverse("question-solved-get-put-delete",args=[0]))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_solved_put_method_validate(self):
        question = Question.objects.create(
            title = "first",link = "https://first.com",category = "Hard",tag = "String"
        )
        data = {
            "question": question.pk
        }
        response = self.client.put(reverse("question-solved-get-put-delete",args=[self.solved.pk]),data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_solved_put_method_invalidate(self):
        data = {
            "question":0
        }
        response = self.client.put(reverse("question-solved-get-put-delete",args=[self.solved.pk]),data=data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_solved_delete_method_validate(self):
        response = self.client.delete(reverse("question-solved-get-put-delete",args=[self.solved.pk]))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    
    def test_solved_delete_method_invalidate(self):
        response = self.client.delete(reverse("question-solved-get-put-delete",args=[0]))
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)