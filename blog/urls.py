from . import views
from django.urls import path


urlpatterns = [
    path("", views.PostFeaturedList.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
]
