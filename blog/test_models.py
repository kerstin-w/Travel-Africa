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
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field("title").max_length
        # Check maximum length of field
        self.assertEqual(max_length, 30)
