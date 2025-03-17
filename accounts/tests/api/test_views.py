import json
import uuid
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from accounts.api.serializers import (
    UserSerializer,
    UserUpdateSerializer,
    LoginSerializer,
    CheckEmailExistsSerializer,
    SetNewPasswordSerializer,
)

from accounts.models import CustomUser, Password_Token


class TestCreateUserView(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_view_validate_data(self):
        data = {
            "username": "test",
            "email": "test@gmail.com",
            "birth_date": "2000-02-03",
            "password": "Test111@",
            "password2": "Test111@",
        }
        response = self.client.post(reverse("api-signup"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_view_invalid_birth_date(self):
        data = {
            "username": "test",
            "email": "test@gmail.com",
            "birth_date": "2024-02-03",
            "password": "Test111@",
            "password2": "Test111@",
        }
        response = self.client.post(reverse("api-signup"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["birth_date"][0]), "your age must be at least 18+."
        )

    def test_create_user_view_invalid_password_validation(self):
        data = {
            "username": "test",
            "email": "test@gmail.com",
            "birth_date": "2000-03-02",
            "password": "test",
            "password2": "test",
        }
        response = self.client.post(reverse("api-signup"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["non_field_errors"][0]),
            "password must be 8 charecter or greather.",
        )

    def test_create_user_view_invalid_password_match(self):
        data = {
            "username": "test",
            "email": "test@gmail.com",
            "birth_date": "2000-03-01",
            "password": "Test111@",
            "password2": "Mistake111@",
        }
        response = self.client.post(reverse("api-signup"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["password"][0]), "Password do not match.")

    def test_create_user_view_invalid_data(self):
        data = {
            "username": "",
            "email": "",
            "birth_date": "",
            "password": "",
            "password2": "",
        }
        response = self.client.post(reverse("api-signup"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["username"][0]), "This field may not be blank."
        )
        self.assertEqual(str(response.data["email"][0]), "This field may not be blank.")
        self.assertEqual(
            str(response.data["birth_date"][0]),
            "Date has wrong format. Use one of these formats instead: YYYY-MM-DD.",
        )
        self.assertEqual(
            str(response.data["password"][0]), "This field may not be blank."
        )
        self.assertEqual(
            str(response.data["password2"][0]), "This field may not be blank."
        )


class TestGetUpdateUserView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            birth_date="2000-02-03",
            password="Test111@",
        )

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.key}")

    def test_get_user_view_validate_data(self):
        response = self.client.get(reverse("api-user-update"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_view_validate_data(self):
        data = {"username": "change@gmail.com", "email": "change@gmail.com"}
        response = self.client.put(reverse("api-user-update"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_view_invalid_birth_date(self):
        data = {"birth_date": "2023-01-02"}
        response = self.client.put(reverse("api-user-update"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["birth_date"][0]), "You must be at least 18+."
        )


class TestLoginView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            birth_date="2000-03-01",
            password="Test111@",
        )

    def test_login_view_validate_data(self):
        data = {"username": "test", "password": "Test111@"}
        response = self.client.post(reverse("api-login"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_view_invalid_password(self):
        data = {"username": "test", "password": "test"}
        response = self.client.post(reverse("api-login"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data["password"][0]),
            "password must be 8 charecter or greather.",
        )


class TestLogoutView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            birth_date="2000-03-01",
            password="Test111@",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.key}")

    def test_user_logout_view(self):
        response = self.client.delete(reverse("api-logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProfileView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            birth_date="2000-03-01",
            password="Test111@",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.key}")

    def test_profile_view(self):
        response = self.client.get(reverse("api-profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPasswordForgotView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            birth_date="2000-03-01",
            password="Test111@",
        )

    def test_password_forgot_view_validate_data(self):
        data = {"email": "test@gmail.com"}
        response = self.client.post(reverse("api-password-forgot"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data["success"],
            "Your email verified successfully and send change password token to your email.",
        )

    def test_password_forgot_view_invalid_email(self):
        data = {"email": "mistake@gmail.com"}
        response = self.client.post(reverse("api-password-forgot"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        self.assertEqual(data["email"][0], "This email does not exists.")


class TestSetNewPasswordView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            birth_date="2000-02-03",
            password="Test111@",
        )
        self.key = Password_Token.objects.create(user=self.user)
        self.key.created_at = timezone.now()
        self.key.save()

    def test_set_new_password_view_validate_data(self):
        data = {"password1": "New1234%", "password2": "New1234%"}
        response = self.client.post(
            reverse("api-set-new-password", args=[self.key.token]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data["success"],
            "Your password changed successfully. Please login to your account.",
        )

    def test_set_new_password_view_invalid_token(self):
        data = {"password1": "New1111@", "password": "New1111@"}
        response = self.client.post(
            reverse("api-set-new-password", args=[uuid.uuid4()]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        self.assertEqual(
            data["error"], "Please create another token this token is expired."
        )
