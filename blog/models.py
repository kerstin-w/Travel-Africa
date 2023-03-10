from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse
from .fields import CaseInsensitiveCharField
from users.models import Profile

STATUS = ((0, "Draft"), (1, "Published"))


class Category(models.Model):
    """
    Model for categories
    """
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=100, unique=True, null=False)
    category_image = CloudinaryField('image', default='placeholder')

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Model for posts
    """
    id = models.BigAutoField(primary_key=True)
    title = CaseInsensitiveCharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    created_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    country = models.CharField(max_length=100)
    featured_image = CloudinaryField('image', default='placeholder')
    regions = models.ManyToManyField(Category)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    """
    Model for post comments
    """
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments')
    body = models.TextField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
