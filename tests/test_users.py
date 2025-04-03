from django.test import TestCase
from propylon_document_manager.file_versions.models import User

class CustomUserManagerTests(TestCase):
    def test_create_superuser(self):
        # Setup
        email = "admin@example.com"
        password = "supersecurepassword"

        # Action
        superuser = User.objects.create_superuser(email=email, password=password)

        # Assertions
        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(password))

    def test_superuser_requires_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=None, password="supersecurepassword")
