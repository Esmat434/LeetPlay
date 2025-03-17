from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class TestAdminSites(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="test", email="test@gmail.com", password="Test111@"
        )
        self.client.force_login(self.admin_user)

    def test_admin_accessible(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
