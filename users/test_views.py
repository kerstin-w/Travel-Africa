from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import Http404
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
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.profile = get_object_or_404(Profile, user=self.user)
        self.profile.pk = 1
        self.profile.save()

    def login(self):
        self.client.login(username="testuser", password="testpass")

    def get_profile_update_url(self):
        return reverse("users:profile_update", kwargs={"pk": self.profile.pk})


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


class ProfileUpdateViewTestCase(BaseProfileTestCase):
    def test_get_profile_update_page(self):
        # Create a user
        self.login()
        # Access the profile update page
        response = self.client.get(self.get_profile_update_url())
        # Assert that the status code is 200
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_update.html")
        self.assertIsInstance(response.context["form"], ProfileForm)

    def test_update_profile(self):
        self.login()
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "description": "Updated test description",
        }
        response = self.client.post(
            self.get_profile_update_url(), data=data, follow=True
        )
        self.assertRedirects(
            response,
            reverse_lazy(
                "users:profile_home", kwargs={"username": self.user.username}
            ),
        )
        self.profile.refresh_from_db()
        self.assertContains(response, "Profile updated successfully")
        self.assertEqual(self.profile.description, "Updated test description")

    def test_form_valid(self):
        self.login()
        data = {
            "user": "testuser",
            "username": "testuser",
            "email": "testuser@example.com",
            "description": "Updated test description",
        }
        form = ProfileForm(data=data, instance=self.profile)
        self.assertTrue(form.is_valid())
        form.instance.user = self.user
    
    def test_unauthenticated_user_redirected_to_login_page(self):
        url = reverse('users:profile_update', kwargs={'pk': self.profile.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f'/accounts/login/?next={url}')
