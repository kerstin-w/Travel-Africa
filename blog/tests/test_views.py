from django.test import TestCase, RequestFactory, Client
from django.views.generic import TemplateView
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.shortcuts import get_object_or_404

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
    PostDetailView,
    BucketListView,
    Error403View,
)

from blog.views import PageTitleViewMixin
from blog.forms import PostForm, CommentForm
from blog.models import Category, Post, Comment, BucketList
from users.models import Profile


class TestDataMixin:
    """
    Set Up Test Data for Test Classes
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        cls.superuser = User.objects.create_superuser(
            username="admin", password="testpass"
        )
        cls.profile = get_object_or_404(Profile, user=cls.user)

        cls.category = Category.objects.create(
            title="test category", slug=slugify("test category")
        )

        cls.post1 = Post.objects.create(
            title="test post",
            slug="test-post",
            author=cls.user,
            content="This is a test post.",
            country="Namibia",
            regions=cls.category,
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
            regions=cls.category,
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
            regions=cls.category,
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
            regions=cls.category,
            featured=True,
            status=1,
            created_on=datetime.now(),
        )
        cls.factory = RequestFactory()

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
        super().setUp()

    def test_form_valid(self):
        """
        Test a valid form input
        """
        form_data = {
            "title": "Test Post Title",
            "content": "This is a test post.",
            "country": "Test Country",
            "regions": self.category,
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
            "regions": self.category,
        }
        request = self.factory.post("/", data=form_data)
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
            "regions": self.category,
        }
        request = self.factory.post("/", data=form_data)
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
        super().setUp()
        self.client = Client()
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
            country="Kenya",
            regions=self.category,
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
            country="Kenya",
            regions=self.category,
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
                regions=self.category,
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
        view = PostCategoryListView()
        view.kwargs = {"slug": self.category.slug}
        expected_queryset = Post.objects.filter(
            status=1, regions=self.category
        )
        queryset = view.get_queryset()
        self.assertQuerysetEqual(
            queryset, expected_queryset, transform=lambda x: x
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
            country="Kenya",
            regions=self.category,
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
            country="Kenya",
            regions=self.category,
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
        self.comment = Comment.objects.create(
            post=self.post1,
            name=self.user,
            body="Test comment",
            profile=self.profile,
            approved=True,
        )
        self.comment2 = Comment.objects.create(
            post=self.post1,
            name=self.user,
            body="Test comment",
            profile=self.profile,
            approved=False,
        )
        self.view = PostDetailView()
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
        url = reverse("post_detail", kwargs={"slug": self.post1.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "post_detail.html")

    def test_post_list_view_contains_post(self):
        """
        Test that view contains post
        """
        url = reverse("post_detail", kwargs={"slug": self.post1.slug})
        response = self.client.get(url)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.content)

    def test_post_list_view_context_object_name(self):
        """
        Test context object name is post
        """
        url = reverse("post_detail", kwargs={"slug": self.post1.slug})
        response = self.client.get(url)
        self.assertEqual(response.context["post"], self.post1)

    def test_post_list_view_context_comments(self):
        """
        Test context object comments
        """
        url = reverse("post_detail", kwargs={"slug": self.post1.slug})
        response = self.client.get(url)
        self.assertEqual(list(response.context["comments"]), [self.comment])

    def test_post_list_view_get_comments(self):
        """
        Test get comments method
        """
        context = {"object": self.post1}
        self.view.object = self.post1
        self.view.get_comments(context)
        self.assertEqual(len(context["comments"]), 1)

    def test_post_list_view_get_liked_status_authenticated(self):
        """
        Test the liked status when user liked post
        """
        self.post1.likes.add(self.user)
        request = self.factory.get(
            reverse("post_detail", args=[self.post1.slug])
        )
        request.user = self.user
        context = {}
        self.view.request = request
        self.view.object = self.post1
        self.view.get_liked_status(context)
        self.assertEqual(context["liked"], True)

    def test_post_list_view_get_liked_status_not_authenticated(self):
        """
        Test the liked status when user is nor registered
        """
        request = self.factory.get(
            reverse("post_detail", args=[self.post1.slug])
        )
        request.user = AnonymousUser()
        context = {}
        self.view.request = request
        self.view.object = self.post1
        self.view.get_liked_status(context)
        self.assertEqual(context["liked"], False)

    def test_post_list_view_get_user_profile_not_authenticated(self):
        """
        Test get user profile when user is nor registered
        """
        request = self.factory.get("/")
        request.user = AnonymousUser()
        response = PostDetailView.as_view()(request, slug=self.post1.slug)
        self.assertEqual(response.status_code, 200)
        view_instance = response.context_data["view"]
        context = response.context_data
        view_instance.object = self.post1
        view_instance.get_user_profile(context)
        self.assertNotIn("profile", context)

    def test_post_list_view_get_user_profile_authenticated_user(self):
        """
        Test get user profile when user is registered
        """
        request = self.factory.get("/")
        request.user = self.user
        self.view = PostDetailView()
        self.view.setup(request, slug=self.post1.slug)
        response = self.view.get(request, slug=self.post1.slug)
        self.assertEqual(response.status_code, 200)
        context = response.context_data
        self.view.object = self.post1
        self.view.get_user_profile(context)
        self.assertIn("profile", context)
        self.assertEqual(context["profile"], self.user.profile)

    def test_post_list_view_comment_submission_success(self):
        """
        Test submission of comment
        """
        self.client.login(username="testuser", password="testpass")
        form_data = {
            "name": self.user.id,
            "body": "Test comment",
        }
        url = reverse("post_detail", kwargs={"slug": self.post1.slug})
        response = self.client.post(url, data=form_data, follow=True)

        comment = Comment.objects.first()
        self.assertEqual(comment.body, form_data["body"])
        self.assertEqual(comment.post, self.post1)
        self.assertEqual(comment.name, self.user)
        self.assertEqual(comment.profile.user, self.profile.user)

        messages = list(response.context.get("messages"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Your comment has been successfully created and is waiting for approval..",
        )

    def test_post_list_comment_submission_redirect(self):
        """
        Test submission redirect
        """
        self.client.login(username="testuser", password="testpass")
        form_data = {
            "name": self.user.id,
            "body": "Test comment",
        }
        url = reverse("post_detail", kwargs={"slug": self.post1.slug})
        response = self.client.post(url, data=form_data, follow=True)

        self.assertRedirects(
            response, reverse("post_detail", kwargs={"slug": self.post1.slug})
        )


class PostCreateViewTest(TestDataMixin, TestCase):
    """
    Test cases for PostCreateView
    """

    def setUp(self):
        """
        Test Data
        """
        self.client.login(username="testuser", password="testpass")
        self.url = reverse("post_create")
        super().setUp()

    def test_post_create_view_user_passes_test(self):
        """
        Test that a logged in user can access create post
        """
        request = self.factory.get(reverse("post_create"))
        request.user = self.user
        response = PostCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post_create_view_user_fails_test(self):
        """
        Test that a not logged in user cannot access create post
        """
        client = Client()
        response = client.get(reverse("post_create"))
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('post_create')}",
        )

    def test_post_create_view_success(self):
        """
        Test valid form submission
        """
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post_create.html")

    def test_post_create_view_invalid_form(self):
        """
        Test invalid form submission
        """
        self.client.login(username="testuser", password="testpass")
        form_data = {}
        response = self.client.post(reverse("post_create"), data=form_data)

        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertContains(response, "This field is required.")


class PostUpdateViewTest(TestDataMixin, TestCase):
    """
    Test cases for PostUpdateView
    """

    def setUp(self):
        """
        Test Data
        """
        self.client = Client()
        self.url = reverse("post_update", kwargs={"slug": self.post1.slug})
        self.login_url = reverse("account_login")
        super().setUp()

    def test_post_update_view_unauthenticated_user(self):
        """
        Test that unauthenticated user cannot access PostUpdateView
        """
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{self.login_url}?next={self.url}",
            status_code=302,
            target_status_code=200,
        )

    def test_post_update_view_authorized_user(self):
        """
        Test that authorized user can access PostUpdateView
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "post_create.html")

    def test_post_update_view_invalid_form_submission(self):
        """
        Test invalid form submission
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "title", "This field is required."
        )
        self.assertFormError(
            response, "form", "content", "This field is required."
        )
        self.assertFormError(
            response, "form", "regions", "This field is required."
        )

    def test_post_update_view_valid_form_submission(self):
        """
        Test valid form submission
        """
        self.client.force_login(self.user)
        new_category = Category.objects.create(
            title="New Category", slug="new-category"
        )
        new_category.save()
        form_data = {
            "title": "Updated Test Post",
            "content": "This is an updated test post.",
            "country": "Namibia",
            "regions": new_category.pk,
        }

        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(
            self.url.format(self.post1.pk), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, form_data["title"].lower())
        self.assertEqual(self.post1.content, form_data["content"])
        self.assertEqual(self.post1.country, form_data["country"])
        self.assertEqual(self.post1.regions.pk, form_data["regions"])
        self.assertEqual(self.post1.author, self.user)
        self.assertEqual(self.post1.status, 0)
        self.assertEqual(self.post1.slug, slugify(form_data["title"]))


class PostDeleteViewTest(TestDataMixin, TestCase):
    """
    Test cases for PostDeleteView
    """

    def setUp(self):
        """
        Test Data
        """
        self.url = reverse("post_delete", kwargs={"slug": self.post1.slug})
        super().setUp()

    def test_post_delete_user_can_delete_own_post(self):
        """
        Test that an author of a post can delete it.
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(title=self.post1).exists())

    def test_post_delete_superuser_can_delete_post(self):
        """
        Test that a superuser can delete any post.
        """
        self.client.force_login(self.superuser)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(title=self.post1).exists())

    def test_post_delete_unauthenticated_user_cannot_delete_post(self):
        """
        Test that an unauthenticated user cannot delete a post.
        """
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title=self.post1).exists())

    def test_post_delete_other_user_cannot_delete_post(self):
        """
        Test that another user cannot delete a post.
        """
        user2 = User.objects.create_user(
            username="testuser2", password="testpass"
        )
        self.client.force_login(user2)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Post.objects.filter(title=self.post1).exists())


class PostSearchResultsViewTest(TestDataMixin, TestCase):
    """
    Test cases for ostSearchResultsView
    """

    def setUp(self):
        """
        Test Data
        """
        self.client = Client()
        self.url = reverse("search_results")
        super().setUp()

    def test_search_view_template(self):
        """
        Test template
        """
        response = self.client.get(self.url, {"q": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search_results.html")

    def test_search_view_country(self):
        """
        Test to search for country
        """
        response = self.client.get(self.url, {"q": "Namibia"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1)

    def test_search_view_title(self):
        """
        Test to search for title
        """
        response = self.client.get(self.url, {"q": "test post"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1)


class PostLikeViewTest(TestDataMixin, TestCase):
    """
    Test cases for PostLikeViewView
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse("post_detail", kwargs={"slug": self.post1.slug})
        self.client.login(username="testuser", password="testpass")
        super().setUp()

    def test_post_liked_status(self):
        """
        Test liked status
        """
        response = self.client.get(
            reverse("post_detail", args=[self.post1.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("liked", response.context)
        self.assertIsInstance(response.context["liked"], bool)
        if self.user in self.post1.likes.all():
            self.assertTrue(response.context["liked"])
        else:
            self.assertFalse(response.context["liked"])

    def test_post_liked_user_can_like_and_unlike_post(self):
        """
        Test that user can like and unlike post
        """
        self.client.force_login(self.user)
        self.assertNotIn(self.user, self.post1.likes.all())

        # Like the post
        response = self.client.post(
            reverse("post_detail", args=[self.post1.slug]) + "like/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user, self.post1.likes.all())

        # Unlike the post
        response = self.client.post(
            reverse("post_detail", args=[self.post1.slug]) + "like/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.user, self.post1.likes.all())


class AddToBucketListViewTest(TestDataMixin, TestCase):
    """
    Test cases for AddToBucketListView
    """

    def setUp(self):
        """
        Test Data
        """
        self.url = reverse("add_to_bucketlist", args=[self.post1.slug])
        super().setUp()

    def test_add_to_bucketlist_view_not_logged_in(self):
        """
        Test redirect if user is not logged in
        """
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={self.url}",
            status_code=302,
            target_status_code=200,
        )

    def test_add_to_bucketlist_view_add_post_to_bucketlist(self):
        """
        Test adding post to bucket list
        """
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(BucketList.objects.filter(post=self.post1).exists())

    def test_add_to_bucketlist_view_response(self):
        """
        Test json response
        """
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"), {"success": True}
        )


class BucketListViewTest(TestDataMixin, TestCase):
    """
    Test cases for BucketListView
    """

    def setUp(self):
        """
        Test Data
        """
        self.bucketlist = BucketList.objects.create(user=self.user)
        self.bucketlist.post.add(self.post1)
        self.url = reverse("bucketlist")
        self.client.login(username="testuser", password="testpass")
        super().setUp()

    def test_bucket_list_get_queryset(self):
        """
        Test query set
        """
        response = self.client.get(self.url)
        view = BucketListView()
        view.request = response.wsgi_request
        queryset = view.get_queryset()
        expected_queryset = BucketList.objects.filter(user=self.user)
        self.assertQuerysetEqual(
            queryset, expected_queryset, transform=lambda x: x
        )

    def test_bucket_list_context_data(self):
        """
        Test context data
        """
        response = self.client.get(self.url)
        context = response.context
        self.assertIn("bucketlist", context)
        self.assertEqual(context["bucketlist"], self.bucketlist)

    def test_bucket_list_remove_post_from_bucketlist(self):
        """
        Test removing post
        """
        post_id = self.post1.id
        response = self.client.post(self.url, {"post_id": post_id})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        self.assertFalse(self.bucketlist.post.filter(id=post_id).exists())

    def test_bucket_list_success_message(self):
        """
        Test success message
        """
        post_id = self.post1.id
        response = self.client.post(self.url, {"post_id": post_id})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "Post successfully removed from your bucket list.",
        )


class CommentDeleteViewTest(TestDataMixin, TestCase):
    """
    Test cases for CommentDeleteView
    """

    def setUp(self):
        """
        Test Data
        """
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpass"
        )
        self.comment6 = Comment.objects.create(
            post=self.post1, name=self.user1, body="Test comment", approved=1
        )
        super().setUp()

    def test_comment_delete_view_comment_author(self):
        """
        Test deleting a comment as comment author
        """
        self.client.login(username="testuser1", password="testpass")
        response = self.client.post(
            reverse("comment_delete", kwargs={"pk": self.comment6.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment6.pk).exists())
        expected_url = reverse(
            "post_detail", kwargs={"slug": self.comment6.post.slug}
        )
        self.assertEqual(response.url, expected_url)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

    def test_comment_delete_view_superuser(self):
        """
        Test deleting a comment as super user
        """
        self.client.login(username="admin", password="testpass")
        response = self.client.post(
            reverse("comment_delete", kwargs={"pk": self.comment6.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment6.pk).exists())

    def test_comment_delete_view_post_author(self):
        """
        Test deleting a comment as post author
        """
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("comment_delete", kwargs={"pk": self.comment6.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.comment6.pk).exists())


class ErrorPageTests(TestDataMixin, TestCase):
    """
    Test Error Pages
    """

    def setUp(self):
        """
        Test Data
        """
        self.client = Client()

    def test_404_page(self):
        """
        Test 404 page
        """
        url = "non-existent-url/"
        response = self.client.get(url)
        self.assertTemplateUsed(response, "errors/404.html")

    def test_403_page(self):
        """
        Test 403 page
        """
        url = reverse("handler403")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "errors/403.html")
