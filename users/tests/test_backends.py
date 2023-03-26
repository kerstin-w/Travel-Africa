from django.test import TestCase
from django.contrib.auth import get_user_model
from users.backends import CaseInsensitiveModelBackend

UserModel = get_user_model()


class CaseInsensitiveModelBackendTest(TestCase):
    """
    Test Case for CaseInsensitiveModelBackend
    """

    def setUp(self):
        """
        Test Data
        """
        self.backend = CaseInsensitiveModelBackend()

    def test_authenticate_with_username_case_insensitive(self):
        """
        Test authenticate with a lowercase username
        """
        user = UserModel.objects.create_user(
            username="TeStUsEr", password="test_password"
        )
        authenticated_user = self.backend.authenticate(
            request=None, username="testuser", password="test_password"
        )
        self.assertEqual(user, authenticated_user)

    def test_authenticate_with_password_case_sensitive(self):
        """
        Test authenticate with a lowercase password
        """
        user = UserModel.objects.create_user(
            username="testuser", password="TeStPaSsWoRd"
        )
        authenticated_user = self.backend.authenticate(
            request=None, username="testuser", password="testpassword"
        )
        self.assertIsNone(authenticated_user)

    def test_authenticate_with_non_existing_user(self):
        """
        Test not existing user
        """
        authenticated_user = self.backend.authenticate(
            request=None, username="nonexistinguser", password="test_password"
        )
        self.assertIsNone(authenticated_user)
