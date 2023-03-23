from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Category, Post, Comment, BucketList, STATUS, Profile


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

    def test_category_title_max_length(self):
        """
        Test maximal length of Title
        """
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field("title").max_length
        # Check maximum length of field
        self.assertEqual(max_length, 30)

    def test_category_slug_max_length(self):
        """
        Test maximal length of Slug
        """
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field("slug").max_length
        # Check maximum length of field
        self.assertEqual(max_length, 30)

    def test_category_title_unique(self):
        """
        Test unique title
        """
        with self.assertRaises(Exception):
            Category.objects.create(
                title="Test Category", slug="test-category-2"
            )

    def test_category_slug_unique(self):
        """
        Test unique slug
        """
        with self.assertRaises(Exception):
            Category.objects.create(
                title="Test Category 2", slug="test-category"
            )

    def test_category_ordering(self):
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

    def test_str_category(self):
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

    def test_post_title_label(self):
        """
        Test the title label
        """
        field_label = self.post._meta.get_field("title").verbose_name
        self.assertEquals(field_label, "title")

    def test_post_max_length(self):
        """
        Test maximal length of Title
        """
        max_length = self.post._meta.get_field("title").max_length
        self.assertEquals(max_length, 100)

    def test_post_title_unique(self):
        """
        Test unique title
        """
        with self.assertRaises(Exception):
            Post.objects.create(title="Test Post", slug="test-category-2")

    def test_post_slug_label(self):
        """
        Test the slug label
        """
        field_label = self.post._meta.get_field("slug").verbose_name
        self.assertEquals(field_label, "slug")

    def test_post_slug_max_length(self):
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

    def test_delete_user_with_posts(self):
        """
        Test deleting User and check if posts from user are deleted as well
        """
        self.user.delete()
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_created_on_label(self):
        """
        Test the created_on label
        """
        field_label = self.post._meta.get_field("created_on").verbose_name
        self.assertEquals(field_label, "created on")

    def test_post_created_on(self):
        """
        Test created_on is automatically set
        """
        self.assertIsNotNone(self.post.created_on)

    def test_post_content_label(self):
        """
        Test the content label
        """
        field_label = self.post._meta.get_field("content").verbose_name
        self.assertEquals(field_label, "content")

    def test_post_content(self):
        """
        Test the content
        """
        self.assertEqual(self.post.content, "This is a test post.")

    def test_post_country_label(self):
        """
        Test the country label
        """
        field_label = self.post._meta.get_field("country").verbose_name
        self.assertEquals(field_label, "country")

    def test_post_country_max_length(self):
        """
        Test maximal length of country
        """
        max_length = self.post._meta.get_field("country").max_length
        self.assertEquals(max_length, 100)

    def test_post_country(self):
        """
        Test the country
        """
        self.assertEqual(self.post.country, "Namibia")

    def test_post_featured_image_label(self):
        """
        Test the featued image label
        """
        field_label = self.post._meta.get_field("featured_image").verbose_name
        self.assertEquals(field_label, "image")

    def test_post_regions_label(self):
        """
        Test the regions label
        """
        field_label = self.post._meta.get_field("regions").verbose_name
        self.assertEquals(field_label, "regions")

    def test_post_regions(self):
        """
        Test the regions
        """
        category = Category.objects.get(id=1)
        self.assertEqual(self.post.regions.count(), 1)
        self.assertEqual(self.post.regions.first(), self.category)

    def test_post_status_label(self):
        """
        Test the status label
        """
        field_label = self.post._meta.get_field("status").verbose_name
        self.assertEquals(field_label, "status")

    def test_post_status_choices(self):
        """
        Test the status choices
        """
        for choice in STATUS:
            self.assertIn(choice[0], [value for value, _ in STATUS])

    def test_post_likes_label(self):
        """
        Test the likes label
        """
        field_label = self.post._meta.get_field("likes").verbose_name
        self.assertEquals(field_label, "likes")

    def test_post_likes(self):
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

    def test_post_featured_label(self):
        """
        Test the featured label
        """
        field_label = self.post._meta.get_field("featured").verbose_name
        self.assertEquals(field_label, "featured")

    def test_post_featured(self):
        # Check default is False
        self.assertFalse(self.post.featured)
        # Check setting to True
        self.post.featured = True
        self.assertTrue(self.post.featured)

    def test_ordering_posts(self):
        """
        Test the ordering of posts
        """
        posts = Post.objects.all()
        self.assertEqual(posts[0], self.new_post)
        self.assertEqual(posts[1], self.post)

    def test_str_post_title(self):
        """
        Test title as string
        """
        self.assertEqual(str(self.post), 'test post')

    def test_post_number_of_likes(self):
        """
        Test number of likes
        """
        likes_count = self.post.likes.count()
        self.assertEqual(self.post.number_of_likes(), likes_count)

    def test_post_get_absolute_url(self):
        """
        Test getting URL for Post
        """
        expected_url = reverse('post_detail', kwargs={'slug': self.post.slug})
        self.assertEqual(self.post.get_absolute_url(), expected_url)


class CommentModelTest(TestCase):
    """
    Test Cases for Comment Model
    """
    def setUp(self):
        """
        Test Data
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.user.save()
        self.profile = get_object_or_404(Profile, user=self.user)
        self.profile.pk = 1
        self.profile.save()
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post',
            country='Botswana',
        )

        self.comment = Comment.objects.create(
            post=self.post,
            name=self.user,
            body='This is a test comment',
        )
        self.new_comment = Comment.objects.create(
            post=self.post,
            name=self.user,
            body='This is another test comment',
        )

    def test_comment_id(self):
        """
        Test comment id
        """
        self.assertIsNotNone(self.comment.id)

    def test_comment_name_label(self):
        """
        Test the name label
        """
        field_label = self.comment._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_comment_name(self):
        """
        Test commenter name
        """
        self.assertEqual(self.comment.name, self.user)

    def test_delete_user_with_comments(self):
        """
        Test deleting User and check if comments from user are deleted as well
        """
        self.assertEqual(self.comment.name, self.user)
        self.user.delete()
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    def test_comment_body_label(self):
        """
        Test the body label
        """
        field_label = self.comment._meta.get_field("body").verbose_name
        self.assertEquals(field_label, "body")

    def test_comment_body_max_length(self):
        """
        Test maximal length of body
        """
        max_length = self.comment._meta.get_field("body").max_length
        self.assertEquals(max_length, 255)

    def test_comment_body_content(self):
        """
        Test content of body
        """
        self.assertEqual(self.comment.body, "This is a test comment")

    def test_comment_created_on_label(self):
        """
        Test the created_on label
        """
        field_label = self.comment._meta.get_field("created_on").verbose_name
        self.assertEquals(field_label, "created on")

    def test_comment_created_on(self):
        """
        Test that date is set automatically
        """
        self.assertIsNotNone(self.comment.created_on)

    def test_comment_approved_label(self):
        """
        Test the approved label
        """
        field_label = self.comment._meta.get_field("approved").verbose_name
        self.assertEquals(field_label, "approved")

    def test_comment_approved_default(self):
        """
        Test approved default is False
        """
        self.assertFalse(self.comment.approved)

    def test_comment_approved_true(self):
        """
        Test setting approved to True
        """
        self.comment.approved = True
        self.assertTrue(self.comment.approved)

    def test_comment_profile_label(self):
        """
        Test the profile label
        """
        field_label = self.comment._meta.get_field("profile").verbose_name
        self.assertEquals(field_label, "profile")

    def test_comment_profile(self):
        """
        Test the profile
        """
        self.assertEqual(self.comment.name.profile, self.profile)

    def test_comments_ordering(self):
        """
        Test the ordering of comments
        """
        comments = Comment.objects.all()
        self.assertEqual(comments[0], self.comment)
        self.assertEqual(comments[1], self.new_comment)

    def test_comment_str(self):
        """
        Test that the str method returns the correct string
        """
        expected_string = f"Comment This is a test comment by {self.user}"
        comment_string = str(self.comment)
        self.assertEqual(comment_string, expected_string)


class BucketListModelTest(TestCase):
    """
    Test Cases for BucketList Model
    """

    def setUp(self):
        """
        Test Data
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.user.save()
        self.bucket_list = BucketList.objects.create(user=self.user)
        self.post1 = Post.objects.create(
            title="Test Post 1",
            slug="test-post-1",
            author=self.user,
            content="This is a test post 1",
            country="Lesotho",
        )
        self.post2 = Post.objects.create(
            title="Test Post 2",
            slug="test-post-2",
            author=self.user,
            content="This is a test post 2",
            country="Kenya",
        )

    def test_bucket_list_user_label(self):
        """
        Test the user label
        """
        field_label = self.bucket_list._meta.get_field("user").verbose_name
        self.assertEquals(field_label, "user")

    def test_bucket_list_user(self):
        """
        Test the user is set
        """
        self.assertEqual(self.bucket_list.user, self.user)
        
    def test_bucket_list_post_label(self):
        """
        Test the post label
        """
        field_label = self.bucket_list._meta.get_field("post").verbose_name
        self.assertEquals(field_label, "post")
    
    def test_bucket_list_post(self):
        """
        Test that the posts
        """
        self.bucket_list.post.add(self.post1)
        self.bucket_list.post.add(self.post2)
        self.assertCountEqual(
            self.bucket_list.post.all(), [self.post1, self.post2]
        )
