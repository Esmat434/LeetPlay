from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from accounts.models import CustomUser


class TestPermissions(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            birth_date="2000-01-02",
            password="Test111@",
        )
        self.token = Token.objects.create(user=self.user)

    def test_user_cannot_access(self):
        response = self.client.get(reverse("api-profile"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_access(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.key}")
        response = self.client.get(reverse("api-profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
