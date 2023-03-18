from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog.models import Post, Category, Comment, BucketList
from users.models import Profile
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.conf import settings


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Add fields for Post in admin panel
    """
    list_display = (
                   'title',
                   'status',
                   'created_on',
                   'author',
                   'featured'
                   )
    prepopulated_fields = {
        'slug': ('title',),
        }
    list_filter = ('status', 'created_on', 'regions')
    search_fields = ['title', 'content']
    summernote_fields = ('content',)
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(status=True)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Add fields for Category in admin panel
    """
    list_display = ['title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Add fields for the profile in the admin panel
    """
    list_display = ('user', 'created_on')
    search_fields = ['user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Add fields for comments in admin panel
    """
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        for comment in queryset:
            if comment.approved:
                print(comment.post.author.username)
                post_author_email = comment.post.author.email
                subject = 'A new comment on your Post!'
                message = render_to_string('comment_notification_email.html')
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
    list_display = ('user', 'added_on',)
    list_filter = ('user', 'added_on',)
    search_fields = ('user__username',)
    filter_horizontal = ('post',)
