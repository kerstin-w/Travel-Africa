from . import views
from django.urls import path


urlpatterns = [
    path("", views.PostFeaturedList.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name="post_detail"),
]
