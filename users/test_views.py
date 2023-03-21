from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from users.models import Profile
from users.forms import ProfileForm


class BaseProfileTestCase(TestCase):
    """
    A base class for Profile-related test cases.
    """

    def setUp(self):
        User.objects.all().delete()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.profile = get_object_or_404(Profile, user=self.user)

    def login(self):
        self.client.login(username='testuser', password='testpass')

    def get_profile_update_url(self):
        return reverse('users:profile_update', kwargs={'pk': self.profile.pk})


class ProfileHomeViewTestCase(BaseProfileTestCase):

    def test_profile_home_view(self):
        """
        Test Profile Page and context
        """
        self.login()
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
