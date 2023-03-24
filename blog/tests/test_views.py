from django.test import TestCase, RequestFactory, Client
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.utils.text import slugify
from datetime import datetime

from django.urls import reverse
from django.views import View
from blog.views import (
    SuperuserFormFieldsMixin,
    PostCreateView,
    PostFormInvalidMessageMixin,
    AboutView,
    HomeListView,
    PostCategoryListView,
)

from blog.views import PageTitleViewMixin
from blog.forms import PostForm
from blog.models import Category, Post, Comment


class TestDataMixin:
    """
    Set Up Test Data for Test Classes
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        cls.category = Category.objects.create(
            title="test category", slug=slugify("test category")
        )

        cls.post1 = Post.objects.create(
            title="test post",
            slug="test-post",
            author=cls.user,
            content="This is a test post.",
            country="Namibia",
            featured=True,
            status=1,
            created_on=datetime.now(),
        )

        cls.post2 = Post.objects.create(
            title="test post 2",
            slug="test-post-2",
            author=cls.user,
            content="This is a test post.",
            country="Morroco",
            featured=False,
            status=1,
            created_on=datetime.now(),
        )

        cls.post3 = Post.objects.create(
            title="test post 3",
            slug="test-post-3",
            author=cls.user,
            content="This is a test post.",
            country="Ghana",
            featured=True,
            status=0,
            created_on=datetime.now(),
        )

        cls.post4 = Post.objects.create(
            title="test post 4",
            slug="test-post-4",
            author=cls.user,
            content="This is a test post.",
            country="South Africa",
            featured=True,
            status=1,
            created_on=datetime.now(),
        )

    def get_posts(self):
        return [self.post1, self.post2, self.post3, self.post4]


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


class SuperuserFormFieldsMixinTest(TestDataMixin, TestCase):
    """
    Test cases for SuperuserFormFieldsMixin
    """

    def setUp(self):
        """
        Test Data
        """
        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser(
            username="superuser", password="superpass"
        )
        super().setUp()

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


class PostFormInvalidMessageMixinTest(TestDataMixin, TestCase):
    """
    Test cases for PostFormInvalidMessageMixin
    """

    def setUp(self):
        """
        Test Data
        """
        self.factory = RequestFactory()
        super().setUp()

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


class HomeListViewTest(TestDataMixin, TestCase):
    """
    Test cases for HomeListView
    """

    def setUp(self):
        self.client = Client()
        super().setUp()

    def test_home_list_view_status_code(self):
        """
        Test the status code
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_list_view_template_used(self):
        """
        Test the template
        """
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "index.html")

    def test_home_list_view_queryset(self):
        """
        Test queryset to only display featured true an status 1
        """
        response = self.client.get(reverse("home"))
        queryset = response.context["object_list"]
        self.assertEqual(queryset.count(), 2)

    def test_home_list_view_queryset_order(self):
        """
        Test queryset to only display in order
        """
        response = self.client.get(reverse("home"))
        queryset = response.context["object_list"]
        self.assertEqual(queryset.count(), 2)
        self.assertEqual(queryset[0], self.post4)
        self.assertEqual(queryset[1], self.post1)


class AboutViewTest(TestCase):
    """
    Test cases for AboutView
    """

    def test_about_view_renders_correct_template(self):
        """
        Test the template is rendered
        """
        response = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "about.html")

    def test_about_view_title(self):
        """
        Test the title is setup correcet
        """
        response = self.client.get(reverse("about"))
        self.assertContains(response, "<title>Travel Africa | About</title>")


class PostListViewTest(TestDataMixin, TestCase):
    """
    Test cases for PostListView
    """

    def setUp(self):
        """
        Test Data
        """
        self.client = Client()
        for i in range(1, 11):
            Post.objects.create(
                title=f"new post {i}",
                slug=f"new-post-{i}",
                author=self.user,
                content="This is a test post.",
                country="Namibia",
                featured=True,
                status=1,
                created_on=datetime.now(),
            )
        super().setUp()

    def test_post_list_view_status_code(self):
        """
        Test status code
        """
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_context(self):
        """
        Test correct context data
        """
        response = self.client.get(reverse("post_list"))
        posts = response.context["posts"]
        self.assertEqual(len(posts), 8)

    def test_post_list_view_pagination(self):
        """
        Test that paginates the posts
        """
        # test first page results
        response = self.client.get(reverse("post_list") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 8)

        # test second page results
        response = self.client.get(reverse("post_list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 5)

    def test_post_list_view_ordering(self):
        """
        Test order of posts
        """
        response = self.client.get(reverse("post_list"))
        posts = response.context["posts"]
        expected_order = Post.objects.filter(status=1).order_by("-created_on")[
            :8
        ]
        self.assertQuerysetEqual(posts, expected_order, transform=lambda x: x)

    def test_post_list_view_comments_count(self):
        """
        Test view annotates the number of approved comments for each post
        """
        post_comment1 = Post.objects.create(
            title="Post Comment 1",
            content="Content 1",
            slug="post-comment-1",
            author=self.user,
            status=1,
        )
        Comment.objects.create(
            post=post_comment1, name=self.user, body="Comment 1", approved=True
        )
        Comment.objects.create(
            post=post_comment1, name=self.user, body="Comment 2", approved=True
        )
        post_comment2 = Post.objects.create(
            title="Post Comment 2",
            content="Content 2",
            slug="post-comment-2",
            author=self.user,
            status=1,
        )
        Comment.objects.create(
            post=post_comment2,
            name=self.user,
            body="Comment 3",
            approved=False,
        )

        response = self.client.get(reverse("post_list"))
        posts = response.context["posts"]
        self.assertEqual(posts.count(), 8)

        self.assertEqual(posts[0].num_comments, 0)
        self.assertEqual(posts[1].num_comments, 2)


class PostCategoryListViewTest(TestDataMixin, TestCase):
    """
    Test cases for PostCategoryListView
    """

    def setUp(self):
        """
        Test Data
        """
        self.category_url = reverse(
            "post_category", kwargs={"slug": self.category.slug}
        )
        self.response = self.client.get(self.category_url)
        for i in range(1, 11):
            Post.objects.create(
                title=f"new post {i}",
                slug=f"new-post-{i}",
                author=self.user,
                content="This is a test post.",
                country="Namibia",
                featured=True,
                status=1,
                created_on=datetime.now(),
            )
        super().setUp()

    def test_post_category_view_status_code(self):
        """
        Test Status code
        """
        self.assertEqual(self.response.status_code, 200)

    def test_post_category_view_template(self):
        """
        Test template
        """
        self.assertTemplateUsed(self.response, "post_list.html")

    def test_post_category_view_page_title_mixin(self):
        """
        Test inherites PageTitleViewMixin
        """
        self.assertIsInstance(PostCategoryListView(), PageTitleViewMixin)

    def test_post_category_view_queryset(self):
        """
        Test Queryset
        """
        queryset = self.response.context["posts"]
        self.assertCountEqual(
            queryset, Post.objects.filter(status=1, regions=self.category)
        )

    def test_post_category_view_pagination(self):
        """
        Test that paginates the posts in category
        """
        # test first page results
        response = self.client.get(reverse("post_list") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 8)

        # test second page results
        response = self.client.get(reverse("post_list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 5)

    def test_post_category_view_comments_count(self):
        """
        Test view annotates the number of approved comments for each post
        """
        post_comment1 = Post.objects.create(
            title="Post Comment 1",
            content="Content 1",
            slug="post-comment-1",
            author=self.user,
            status=1,
        )
        Comment.objects.create(
            post=post_comment1, name=self.user, body="Comment 1", approved=True
        )
        Comment.objects.create(
            post=post_comment1, name=self.user, body="Comment 2", approved=True
        )
        post_comment2 = Post.objects.create(
            title="Post Comment 2",
            content="Content 2",
            slug="post-comment-2",
            author=self.user,
            status=1,
        )
        Comment.objects.create(
            post=post_comment2,
            name=self.user,
            body="Comment 3",
            approved=False,
        )

        response = self.client.get(reverse("post_list"))
        posts = response.context["posts"]
        self.assertEqual(posts.count(), 8)

        self.assertEqual(posts[0].num_comments, 0)
        self.assertEqual(posts[1].num_comments, 2)


class PostDetailViewTest(TestDataMixin, TestCase):
    """
    Test cases for PostDetailView
    """
    def setUp(self):
        """
        Test Data
        """
        self.client = Client()
        super().setUp()
    
    def test_post_detail_view_url_exists(self):
        """
        Test post url
        """
        url = reverse("post_detail", kwargs={"slug": self.post1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_detail_view_template(self):
        """
        Test template
        """
        url = reverse('post_detail', kwargs={'slug': self.post1.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'post_detail.html')
    
    def test_post_list_view_contains_post(self):
        """
        Test that view contains post
        """
        url = reverse('post_detail', kwargs={'slug': self.post1.slug})
        response = self.client.get(url)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.content)