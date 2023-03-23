from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category

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
        category = Category(title="Test Category", slug="test-category-2")
        with self.assertRaises(Exception):
            category.save()
    
    def test_slug_unique(self):
        """
        Test unique slug
        """
        category = Category(title="Test Category 2", slug="test-category")
        with self.assertRaises(Exception):
            category.save()
