from django.test import TestCase
from accounts.models import CustomUser, Password_Token


class TestModels(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            birth_date="2000-03-04",
            password="Test1234@",
        )

        self.token = Password_Token.objects.create(user=self.user)

    def test_user_models(self):
        user = CustomUser.objects.get(username="testuser")
        self.assertEqual(user.email, "test@gmail.com")

    def test_token_models(self):
        self.assertEqual(self.token.user, self.user)
