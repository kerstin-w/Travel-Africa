from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog.models import Post, Category, Comment
from users.models import Profile


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
    list_display = ('user',)
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