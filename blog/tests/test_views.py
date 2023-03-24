from django.test import TestCase, RequestFactory
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import View
from blog.views import SuperuserFormFieldsMixin, PostCreateView

from blog.views import PageTitleViewMixin


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
