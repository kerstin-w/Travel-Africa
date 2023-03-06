from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog.models import Post


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = (
                   'title', 'status', 'created_on', 'author', 'featured'
                   )
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on', 'regions')
    search_fields = ['title', 'content']
    summernote_fields = ('content',)
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(status=True)
