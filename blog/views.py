from django.shortcuts import render
from django.views import generic
from .models import Post

class PostFeaturedList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(
        featured=True, status=1).order_by('-created_on')
    template_name = "index.html"
