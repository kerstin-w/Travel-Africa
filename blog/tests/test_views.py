from django.test import TestCase, RequestFactory, Client
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.utils.text import slugify

from django.urls import reverse
from django.views import View
from blog.views import (
    SuperuserFormFieldsMixin,
    PostCreateView,
    PostFormInvalidMessageMixin,
)

from blog.views import PageTitleViewMixin
from blog.forms import PostForm
from blog.models import Category, Post


class TestView(PageTitleViewMixin, TemplateView):
    """
    Test View to test PageTitleViewMixin
    """

    title = "Test Page"
    template_name = "test.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class PageTitleViewMixinTest(TestCase):
    """
    Test cases for PageTitleViewMixin
    """

    def setUp(self):
        """
        Create a request factory instance
        """
        self.factory = RequestFactory()

    def test_page_title(self):
        """
        Test that the title correctly passed
        """
        request = self.factory.get("/")
        view = TestView.as_view()
        response = view(request)
        self.assertEqual(response.context_data["title"], "Test Page")


class SuperuserFormFieldsMixinTest(TestCase):
    """
    Test cases for SuperuserFormFieldsMixin
    """

    def setUp(self):
        """
        Test Data
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.superuser = User.objects.create_superuser(
            username="superuser", password="superpass"
        )

    def test_super_user_can_access_all_form_fields(self):
        """
        Test that the superuser can access all form fields
        """
        self.client.login(username="superuser", password="superpass")
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 200)

        # Check the featured field is in the form
        form = response.context_data["form"]
        self.assertIn("featured", form.fields)

    def test_non_super_user_cannot_access_featured_form_field(self):
        """
        Test that the regular user cannot  access all form fields
        """
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 200)

        # Check the featured field is not in the form
        form = response.context_data["form"]
        self.assertNotIn("featured", form.fields)


class PostFormInvalidMessageMixinTest(TestCase):
    """
    Test cases for PostFormInvalidMessageMixin
    """

    def setUp(self):
        """
        Test Data
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpass",
        )
        self.category = Category.objects.create(title="test category", id=1)

        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            country="Test Country",
            author=self.user,
        )

    def test_form_valid(self):
        """
        Test a valid form input
        """
        form_data = {
            "title": "Test Post Title",
            "content": "This is a test post.",
            "country": "Test Country",
            "regions": [self.category.id],
        }

        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        """
        Test a invalid form input and message response
        """
        form_data = {
            "title": "",
            "content": "",
            "country": "",
            "regions": [self.category.id],
        }
        request = RequestFactory().post("/", data=form_data)
        mixin = PostFormInvalidMessageMixin()
        mixin.request = request
        form = PostForm(data=form_data)
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)

        # Create a mock HttpResponse object
        response = HttpResponse()
        setattr(mixin, "render_to_response", lambda context: response)

        result = mixin.form_invalid(form)
        messages = list(get_messages(request))
        expected_message = (
            "Your post could not be submitted. Please review your inputs!"
        )
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)
        self.assertEqual(result, response)
        self.assertEqual(result.status_code, 200)

    def test_form_existing_title(self):
        """
        Test a invalid form input with existing title and message response
        """

        form_data = {
            "title": "Test Post",
            "content": "This is a new test post.",
            "country": "New Test Country",
            "featured": False,
            "regions": [self.category.id],
        }
        request = RequestFactory().post("/", data=form_data)
        mixin = PostFormInvalidMessageMixin()
        mixin.request = request
        form = PostForm(data=form_data)
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Post with this Title already exists.", form.errors["title"]
        )


class HomeListViewTest(TestCase):
    """
    Test cases for HomeListView
    """

    def setUp(self):
        """
        Test Data
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.user.save()
        self.category = Category.objects.create(
            title="test category", slug=slugify("test category")
        )
        self.category.save()
        self.post1 = Post.objects.create(
            title="test post",
            slug="test-post",
            author=self.user,
            content="This is a test post.",
            country="Namibia",
            featured=True,
        )
        self.post2 = Post.objects.create(
            title="test post 2",
            slug="test-post-2",
            author=self.user,
            content="This is a test post.",
            country="Morroco",
            featured=False,
        )
        self.post3 = Post.objects.create(
            title="test post 3",
            slug="test-post-3",
            author=self.user,
            content="This is a test post.",
            country="Ghana",
            featured=True,
        )

    def test_home_list_view_status_code(self):
        """
        Test the status code
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
