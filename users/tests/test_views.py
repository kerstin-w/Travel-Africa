from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from datetime import datetime

from blog.models import Category, Post, Comment
from users.models import Profile
from users.forms import ProfileForm


class BaseProfileTestCase(TestCase):
    """
    A base class for Profile-related test cases.
    """

    def setUp(self):
        """
        Test Data
        """
        User.objects.all().delete()
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password="testpassword",
        )
        try:
            self.profile = self.user.profile
        except Profile.DoesNotExist:
            self.profile = Profile.objects.create(user=self.user)

        self.profile.description = "Test description"
        self.profile.pk = 1
        self.profile.save()
        self.category = Category.objects.create(
            title="test category", slug=slugify("test category")
        )
        self.post1 = Post.objects.create(
            title="test post",
            slug="test-post",
            author=self.user,
            content="This is a test post.",
            country="Namibia",
            regions=self.category,
            featured=True,
            status=1,
            created_on=datetime.now(),
        )

    def login(self):
        self.client.login(username="testuser", password="testpass")

    def get_profile_update_url(self):
        return reverse("users:profile_update", kwargs={"pk": self.profile.pk})


class ProfileHomeViewTest(BaseProfileTestCase, TestCase):
    """
    Test cases for ProfileHome
    """

    def setUp(self):
        """
        Test Data
        """
        super().setUp()
        self.client = Client()
        self.url = reverse(
            "users:profile_home", kwargs={"username": self.user.username}
        )

    def test_profiel_home_view_template(self):
        """
        Test template
        """
        self.login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_profile_home_view_displays_profile_information(self):
        """
        Test profile information
        """
        self.login()
        response = self.client.get(self.url)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.profile.description)

    def test_profile_home_view_contains_user_username(self):
        """
        Test profile information username
        """
        self.login()
        response = self.client.get(self.url)
        self.assertContains(response, self.user.username)

    def test_profile_home_view_anonymous_user(self):
        """
        Test redirect for anonymous user
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_profile_home_view_posts(self):
        """
        Tests posts in profile
        """
        self.login()
        for i in range(1, 11):
            Post.objects.create(
                title=f"new post {i}",
                slug=f"new-post-{i}",
                author=self.user,
                content="This is a test post.",
                country="Namibia",
                regions=self.category,
                featured=True,
                status=1,
                created_on=datetime.now(),
            )
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["posts"]), 11)
        self.assertEqual(response.context["sum_posts"], 11)
        self.assertContains(response, self.post1)
        posts = response.context["posts"]
        self.assertEqual(list(posts), list(posts.order_by("-created_on")))

    def test_profile_home_view_comments(self):
        """
        Tests comments
        """
        self.login()
        response = self.client.get(self.url)

        self.assertEqual(response.context["sum_comments"], 0)

        # Add a comment to post1
        Comment.objects.create(
            post=self.post1,
            name=self.user,
            body="This is a test comment.",
            profile=self.profile,
            approved=True,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.context["sum_posts"], 1)
        self.assertEqual(response.context["sum_comments"], 1)
        posts = response.context["posts"]
        for post in posts:
            self.assertIsNotNone(post.num_comments)
            self.assertGreaterEqual(post.num_comments, 0)
        comments = response.context_data["comments"]
        sorted_comments = sorted(
            comments, key=lambda c: c.created_on, reverse=True
        )
        self.assertEqual(list(comments), sorted_comments)


class ProfileUpdateViewTest(BaseProfileTestCase, TestCase):
    """
    Test cases for ProfileUpdate
    """

    def setUp(self):
        """
        Test Data
        """
        super().setUp()

    def test_get_profile_update_page(self):
        """
        Test Update Page
        """
        self.login()
        response = self.client.get(self.get_profile_update_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_update.html")
        self.assertIsInstance(response.context["form"], ProfileForm)

    def test_update_profile(self):
        """
        Test User updating own Profile
        """
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

    def test_profile_update_form_valid(self):
        """
        Test Form Validation
        """
        self.login()
        data = {
            "username": "newname",
            "email": "testuser@example.com",
            "description": "Updated test description",
        }
        form = ProfileForm(data=data, instance=self.profile)
        self.assertTrue(form.is_valid())
        form.instance.user = self.user
        self.assertEqual(form.cleaned_data["username"], "Newname")

    def test_profile_update_email(self):
        """
        Test email update valid
        """
        form_data = {
            "email": "test@test.com",
            "username": "testname",
        }
        form = ProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        cleaned_email = form.clean_email()
        self.assertEqual(cleaned_email, "test@test.com")

    def test_profile_update_unauthenticated_user_redirected_to_login_page(
        self,
    ):
        """
        Test Access of unauthenticated user
        """
        url = self.get_profile_update_url()
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def test_profile_update_user_cannot_update_profile_of_another_user(self):
        """
        Test Access of different User than Profile
        """
        self.client.login(
            username=self.user1.username, password="testpassword"
        )
        url = self.get_profile_update_url()
        response = self.client.get(url)
        self.assertContains(response, "Something went wrong...")

    def test_profile_update_username_exists(self):
        """
        Test profile update to an existing user name
        """
        self.login()
        form_data = {
            "email": "newemail@example.com",
            "username": "testuser1",
            "description": "test description",
        }
        form = ProfileForm(data=form_data, instance=self.profile, request=None)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Username already taken. Please choose another username.",
            form.errors["__all__"],
        )

    def test_profile_update_email_exists(self):
        """
        Test porfile update to existing email
        """
        self.login()
        form_data = {
            "email": "testuser1@example.com",
            "username": "testuser",
        }

        form = ProfileForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertEqual(
            form.errors["__all__"][0],
            "A user with that email address already exists. Please enter another email.",
        )


class ProfileDeleteViewTest(BaseProfileTestCase, TestCase):
    """
    Test cases for ProfileDelete
    """

    def setUp(self):
        """
        Test Data
        """
        super().setUp()
        self.url = reverse(
            "users:profile_delete",
            kwargs={"username": self.user.username, "pk": self.profile.pk},
        )

    def test_profile_delete(self):
        """
        Test Delete Profile
        """
        self.login()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Profile.objects.filter(pk=self.profile.pk).exists())

    def test_profile_delete_view_redirects_to_login(self):
        """
        Test Access of unauthenticated user
        """
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/accounts/login/?next=/testuser/1/delete/"
        )

    def test_profile_delete_view_success(self):
        """
        Test delete successfully and redirect
        """
        self.login()
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(Profile.objects.filter(pk=self.profile.pk).exists())

    def test_profile_delete_view_not_owner(self):
        """
        Test Access of different User than Profile owner
        """
        user2 = User.objects.create_user(
            username="user2", password="testpass123"
        )
        self.client.login(
            username=self.user1.username, password="testpassword"
        )
        response = self.client.get(
            reverse(
                "users:profile_home", kwargs={"username": self.user.username}
            )
        )
        self.assertNotContains(
            response,
            '<a data-bs-toggle="modal" href="#deleteProfileModal"><i class="fa-solid fa-trash icon"></i></a>',
        )
