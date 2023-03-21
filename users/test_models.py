from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Profile

class TestProfileModel(TestCase):
    """
    A class to test the Profile model
    """
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.test_user = User.objects.create_user(
            'testuser', 'testuser@test.com', 'testpass'
        )

    def test_profile_str(self):
        """
        Test Profile string method
        """
        profile = get_object_or_404(Profile, user=self.test_user)
        self.assertEqual(str(profile), "testuser")
