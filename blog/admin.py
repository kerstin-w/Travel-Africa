from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string

from blog.models import BucketList, Category, Comment, Post
from users.models import Profile
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Add fields for Post in admin panel
    """

    list_display = ("title", "status", "created_on", "author", "featured")
    prepopulated_fields = {
        "slug": ("title",),
    }
    list_filter = ("status", "created_on", "regions__title")
    search_fields = ["title", "content"]
    summernote_fields = ("content",)
    actions = ["approve_posts"]

    def approve_posts(self, request, queryset):
        queryset.update(status=True)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Add fields for Category in admin panel
    """

    list_display = ["title"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Add fields for the profile in the admin panel
    """

    list_display = ("user", "created_on")
    search_fields = ["user"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Add fields for comments in admin panel
    """

    list_display = ("name", "body", "post", "created_on", "approved")
    list_filter = ("approved", "created_on")
    search_fields = ("name__username", "body")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        for comment in queryset:
            if comment.approved:
                post_author_email = comment.post.author.email
                subject = "A new comment on your Post!"
                message = render_to_string(
                    "comment_notification_email.txt", {"comment": comment}
                )
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [post_author_email],
                    fail_silently=False,
                )


@admin.register(BucketList)
class BucketListAdmin(admin.ModelAdmin):
    """
    Add fields for Bucket List in admin panel
    """

    list_display = (
        "user",
        "created_on",
    )
    list_filter = (
        "user",
        "created_on",
    )
    search_fields = ("user__username",)
    filter_horizontal = ("post",)
