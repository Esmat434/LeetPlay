from rest_framework.test import APITestCase, APIClient
from accounts.api.serializers import (
    UserSerializer,
    UserUpdateSerializer,
    LoginSerializer,
    CheckEmailExistsSerializer,
    SetNewPasswordSerializer,
)
from accounts.models import CustomUser


class TestUserSerializer(APITestCase):
    def test_user_serialzier_validated_data(self):
        data = {
            "username": "test",
            "email": "test@gmail.com",
            "birth_date": "2000-03-01",
            "password": "Test111@",
            "password2": "Test111@",
        }
        serialzier = UserSerializer(data=data)
        self.assertTrue(serialzier.is_valid())

    # this test check password must match with password2
    def test_user_serializer_invalid_password_matching(self):
        data = {
            "username": "test",
            "email": "test@gmail.com",
            "birth_date": "2000-01-02",
            "password": "Test111@",
            "password2": "Mistake111@",
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    # this test check password must be at least 8 chr and contain a-z/1-9/@%&$!
    def test_user_serializer_invalid_password_validation(self):
        data = {
            "username": "test",
            "email": "test@gmail.com",
            "birth_date": "2000-02-01",
            "password": "Test",
            "password2": "Test",
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_user_serializer_invalid_birth_date(self):
        data = {
            "username": "test",
            "email": "test@gmail.com",
            "birth_date": "2025-02-01",
            "password": "Test111@",
            "password2": "Test111@",
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class TestUserUpdateSerializer(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            birth_date="2000-03-01",
            password="Test111@",
        )
        self.client.login(username="test", password="Test111@")

    def test_user_update_serializer_validated_data(self):
        data = {"username": "test change"}
        serializer = UserUpdateSerializer(self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())

    def test_user_update_serializer_invalid_birth_date(self):
        data = {"birth_date": "2025-01-02"}
        serializer = UserUpdateSerializer(self.user, data=data, partial=True)
        self.assertFalse(serializer.is_valid())


class TestLoginSerializer(APITestCase):
    def test_login_serializer_validate_data(self):
        data = {"username": "test", "password": "Test111@"}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_login_serializer_invalid_password_validation(self):
        data = {"username": "test", "password": "abcdc"}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class TestCheckEmailSerializer(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test",
            email="test@gmail.com",
            birth_date="2000-03-01",
            password="Test111@",
        )

    def test_check_email_serializer_validate_data(self):
        data = {"email": "test@gmail.com"}
        serializer = CheckEmailExistsSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_check_email_serializer_invalid_email(self):
        data = {"email": "one@gmail.com"}
        serializer = CheckEmailExistsSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class TestSetNewPasswordSerializer(APITestCase):
    def test_set_new_password_serializer_validate_data(self):
        data = {"password1": "Test111@", "password2": "Test111@"}
        serializer = SetNewPasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_set_new_password_serializer_invalid_password_match(self):
        data = {"password1": "Test123@", "password2": "Mistake111@"}
        serializer = SetNewPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_set_new_password_serializer_invalid_password_validation(self):
        data = {"password1": "test", "password2": "test"}
        serializer = SetNewPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
