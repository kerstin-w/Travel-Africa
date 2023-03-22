from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post, Category, Comment, BucketList
from .models import Post


class PostAdminTest(TestCase):
    """
    Test Cases for PostAdmin
    """

    def setUp(self):
        """
        Test Data
        """
        self.user = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="password",
        )
        self.client.login(username="admin", password="password")
        category1 = Category.objects.create(title="Category 1")
        self.post = Post.objects.create(
            title="Test Post",
            content="Lorem ipsum dolor sit amet",
            author=self.user,
        )
        self.post.regions.add(category1)

    def test_approve_posts(self):
        """
        Test Admin approve posts
        """
        response = self.client.post(
            reverse("admin:blog_post_changelist"),
            data={
                "action": "approve_posts",
                "_selected_action": [self.post.id],
            },
        )
        self.assertRedirects(response, reverse("admin:blog_post_changelist"))
        self.post.refresh_from_db()
        self.assertTrue(self.post.status)

    def test_list_display(self):
        """
        Test List Display in Admin Panel
        """
        response = self.client.get(reverse("admin:blog_post_changelist"))
        self.assertContains(response, "Title")
        self.assertContains(response, "Status")
        self.assertContains(response, "Created on")
        self.assertContains(response, "Author")
        self.assertContains(response, "Featured")

    def test_prepopulated_fields(self):
        """
        Test Prepopulated Fields
        """
        response = self.client.get(reverse("admin:blog_post_add"))
        self.assertContains(response, 'name="slug"')

    def test_list_filter(self):
        """
        Test List Filter
        """
        response = self.client.get(reverse("admin:blog_post_changelist"))
        self.assertContains(response, "status")
        self.assertContains(response, "created_on")
        self.assertContains(response, "regions")

    def test_search_fields(self):
        """
        Test Search Field
        """
        response = self.client.get(reverse("admin:blog_post_changelist"))
        self.assertContains(response, 'name="q"')
        response = self.client.get(reverse("admin:blog_post_changelist"), {'q': 'Test Post'})
        self.assertContains(response, 'Test Post')

    def test_summernote_fields(self):
        """
        Test Summernote
        """
        response = self.client.get(reverse("admin:blog_post_add"))
        self.assertContains(response, "content")
        self.assertContains(response, 'class="summernote-div"')


class CategoryAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="password"
        )
        self.client.login(username="admin", password="password")
        Category.objects.create(title="Test Category")

    def test_category_admin_list_display(self):
        """
        Test List Display in Admin Panel
        """
        response = self.client.get(reverse("admin:blog_category_changelist"))
        self.assertContains(response, "title")

    def test_category_admin_search_fields(self):
        """
        Test Search Field
        """
        response = self.client.get(
            reverse("admin:blog_category_changelist"), {"q": "Test"}
        )
        self.assertContains(response, "Test Category")

    def test_category_admin_prepopulated_fields(self):
        """
        Test Prepopulated Fields
        """
        response = self.client.get(reverse("admin:blog_category_add"))
        data = {"title": "Test Category 2", "slug": "test-category-2"}
        expected_slug = "test-category-2"
        response = self.client.post(reverse("admin:blog_category_add"), data)
        self.assertEqual(response.status_code, 302)
        category = Category.objects.get(title="Test Category 2")
        self.assertEqual(category.slug, expected_slug)
