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
