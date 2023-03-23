from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.contrib.auth.models import User
from .models import Category, Post, STATUS


class CategoryModelTest(TestCase):
    """
    Test Cases for Category Model
    """

    @classmethod
    def setUpTestData(cls):
        """
        Test Data
        """
        Category.objects.create(title="Test Category", slug="test-category")

    def test_title_max_length(self):
        """
        Test maximal length of Title
        """
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field("title").max_length
        # Check maximum length of field
        self.assertEqual(max_length, 30)

    def test_slug_max_length(self):
        """
        Test maximal length of Slug
        """
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field("slug").max_length
        # Check maximum length of field
        self.assertEqual(max_length, 30)

    def test_title_unique(self):
        """
        Test unique title
        """
        with self.assertRaises(Exception):
            Category.objects.create(
                title="Test Category", slug="test-category-2"
            )

    def test_slug_unique(self):
        """
        Test unique slug
        """
        with self.assertRaises(Exception):
            Category.objects.create(
                title="Test Category 2", slug="test-category"
            )

    def test_ordering(self):
        """
        Test ordering of categories
        """
        Category.objects.create(title="B Category", slug="b-category")
        Category.objects.create(title="A Category", slug="a-category")
        Category.objects.create(title="C Category", slug="c-category")

        expected_categories = [
            "A Category",
            "B Category",
            "C Category",
            "Test Category",
        ]
        # Categories in actual order
        actual_categories = [
            category.title for category in Category.objects.all()
        ]
        # Compare actual order with expected order
        self.assertListEqual(actual_categories, expected_categories)

    def test_verbose_name_plural(self):
        """
        Test verbose name
        """
        category = Category.objects.get(id=1)
        verbose_name_plural = category._meta.verbose_name_plural
        self.assertEquals(verbose_name_plural, "Categories")

    def test_str(self):
        """
        Test string title
        """
        category = Category.objects.get(id=1)
        self.assertEqual(str(category), "Test Category")


class PostModelTest(TestCase):
    """
    Test Cases for Post Model
    """

    def setUp(self):
        """
        Test Data
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.user.save()
        self.category = Category.objects.create(title="test category")
        self.category.save()
        self.post = Post.objects.create(
            title="test post",
            slug="test-post",
            author=self.user,
            content="This is a test post.",
            country="Namibia",
            featured_image="test.jpg",
        )
        self.post.regions.add(self.category)
        self.post.save()

        self.new_post = Post.objects.create(
            title='Test Post 2',
            slug='test-post-2',
            author=self.user,
            content='This is a test post 2.',
            country='Kongo',
        )

    def test_title_label(self):
        """
        Test the title label
        """
        field_label = self.post._meta.get_field("title").verbose_name
        self.assertEquals(field_label, "title")

    def test_title_max_length(self):
        """
        Test maximal length of Title
        """
        max_length = self.post._meta.get_field("title").max_length
        self.assertEquals(max_length, 100)

    def test_title_unique(self):
        """
        Test unique title
        """
        with self.assertRaises(Exception):
            Post.objects.create(title="Test Post", slug="test-category-2")

    def test_slug_label(self):
        """
        Test the slug label
        """
        field_label = self.post._meta.get_field("slug").verbose_name
        self.assertEquals(field_label, "slug")

    def test_slug_max_length(self):
        """
        Test maximal length of slug
        """
        max_length = self.post._meta.get_field("slug").max_length
        self.assertEquals(max_length, 100)

    def test_author_label(self):
        """
        Test the author label
        """
        field_label = self.post._meta.get_field("author").verbose_name
        self.assertEquals(field_label, "author")

    def test_post_author(self):
        """
        Test the author
        """
        self.assertEqual(self.post.author, self.user)

    def test_delete_user(self):
        """
        Test deleting User and check if posts from user are deleted as well
        """
        self.user.delete()
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_created_on_label(self):
        """
        Test the created_on label
        """
        field_label = self.post._meta.get_field("created_on").verbose_name
        self.assertEquals(field_label, "created on")

    def test_created_on(self):
        """
        Test created_on is automatically set
        """
        self.assertIsNotNone(self.post.created_on)

    def test_content_label(self):
        """
        Test the content label
        """
        field_label = self.post._meta.get_field("content").verbose_name
        self.assertEquals(field_label, "content")

    def test_content(self):
        """
        Test the content
        """
        self.assertEqual(self.post.content, "This is a test post.")

    def test_country_label(self):
        """
        Test the country label
        """
        field_label = self.post._meta.get_field("country").verbose_name
        self.assertEquals(field_label, "country")

    def test_country_max_length(self):
        """
        Test maximal length of country
        """
        max_length = self.post._meta.get_field("country").max_length
        self.assertEquals(max_length, 100)

    def test_country(self):
        """
        Test the country
        """
        self.assertEqual(self.post.country, "Namibia")

    def test_featured_image_label(self):
        """
        Test the featued image label
        """
        field_label = self.post._meta.get_field("featured_image").verbose_name
        self.assertEquals(field_label, "image")

    def test_regions_label(self):
        """
        Test the regions label
        """
        field_label = self.post._meta.get_field("regions").verbose_name
        self.assertEquals(field_label, "regions")

    def test_regions(self):
        """
        Test the regions
        """
        category = Category.objects.get(id=1)
        self.assertEqual(self.post.regions.count(), 1)
        self.assertEqual(self.post.regions.first(), self.category)

    def test_status_label(self):
        """
        Test the status label
        """
        field_label = self.post._meta.get_field("status").verbose_name
        self.assertEquals(field_label, "status")

    def test_status_choices(self):
        """
        Test the status choices
        """
        for choice in STATUS:
            self.assertIn(choice[0], [value for value, _ in STATUS])

    def test_likes_label(self):
        """
        Test the likes label
        """
        field_label = self.post._meta.get_field("likes").verbose_name
        self.assertEquals(field_label, "likes")

    def test_likes(self):
        """
        Test the likes.
        """
        # Add a like
        self.post.likes.add(self.user)
        self.assertEqual(self.post.likes.count(), 1)
        self.assertEqual(self.post.likes.first().username, "testuser")
        # Remove a like
        self.post.likes.remove(self.user)
        self.assertEqual(self.post.likes.count(), 0)

    def test_featured_label(self):
        """
        Test the featured label
        """
        field_label = self.post._meta.get_field("featured").verbose_name
        self.assertEquals(field_label, "featured")

    def test_featured(self):
        # Check default is False
        self.assertFalse(self.post.featured)
        # Check setting to True
        self.post.featured = True
        self.assertTrue(self.post.featured)

    def test_ordering(self):
        """
        Test the ordering of posts
        """
        posts = Post.objects.all()
        self.assertEqual(posts[0], self.new_post)
        self.assertEqual(posts[1], self.post)

    def test_str(self):
        """
        Test title as string
        """
        self.assertEqual(str(self.post), 'test post')
    
    def test_number_of_likes(self):
        """
        Test number of likes
        """
        likes_count = self.post.likes.count()
        self.assertEqual(self.post.number_of_likes(), likes_count)
