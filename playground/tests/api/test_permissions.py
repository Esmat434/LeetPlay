from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()

class TestIsAuthenticationTokenAndSuperUser(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username = "test user", email = "testuser@gmail.com", birth_date = "2000-03-01",
            password = "TestUser11@"
        )
        self.superuser = User.objects.create_superuser(
            username = "test super", email = "testsuper@gmai.com",birth_date = "2000-04-05",
            password = "TestSuper22@"
        )

        self.token_user = Token.objects.create(user = self.user)
        self.token_superuser = Token.objects.create(user = self.superuser)
    
    def test_is_authentication_token_validate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token_user.key}")
        response = self.client.get(reverse('question-get-post'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_is_authentication_token_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {uuid.uuid4()}")
        response = self.client.get(reverse('question-get-post'))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_is_authentication_token_and_is_superuser_validate(self):
        data = {
            "title":"test","link":"https://test.com","category":"Easy","tag":"Array"
        }
        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token_superuser.key}")
        response = self.client.post(reverse("question-get-post"),data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_is_authentication_token_and_is_superuser_invalid(self):
        data = {
            "title":"test","link":"https://test.com","category":"Easy","tag":"Array"
        }
        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token_user.key}")
        response = self.client.post(reverse("question-get-post"),data=data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

class TestIsOwnerOrReadOnly(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username = "test",email = "test@gmail.com",birth_date = "2000-04-05",
            password = "Test111@"
        )
        self.token = Token.objects.create(user = self.user)
    
    def test_is_owner_or_read_only_validate(self):
        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {self.token.key}")
        response = self.client.get(reverse("question-solved-get-post"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_is_owner_or_read_only_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {uuid.uuid4()}")
        response = self.client.get(reverse("question-solved-get-post"))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)