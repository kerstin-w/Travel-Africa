from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse

from users.models import Profile


class ProfileHomeViewTestCase(TestCase):
    """
    A class to test the ProfileHomeView
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpass"
        )
        self.profile = get_object_or_404(Profile, user=self.user)

    def test_profile_home_view(self):
        """
        Test Profile Page and context
        """
        self.client.login(username="testuser", password="testpass")
        url = reverse("users:profile_home", args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        self.assertContains(response, self.profile)
        self.assertContains(response, self.user.username)
        self.assertTrue("profile" in response.context)
        self.assertTrue("sum_posts" in response.context)
        self.assertTrue("sum_comments" in response.context)
        self.assertTrue("posts" in response.context)
        self.assertTrue("comments" in response.context)
        self.assertEqual(response.context["profile"], self.profile)
        self.assertEqual(response.context["sum_posts"], 0)
        self.assertEqual(response.context["sum_comments"], 0)
        self.assertEqual(list(response.context["posts"]), [])
        self.assertEqual(list(response.context["comments"]), [])

    def test_profile_home_view_with_unauthenticated_user(self):
        """
        Test Access of unauthenticated user
        """
        url = reverse("users:profile_home", args=[self.user.username])
        response = self.client.get(url)
        login_url = reverse("account_login")
        self.assertRedirects(response, f"{login_url}?next={url}")
