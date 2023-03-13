from . import views
from django.urls import path


urlpatterns = [
    path("", views.PostFeaturedList.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('search/', views.PostSearchResultsView.as_view(), name="search_results"),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('category/<slug:slug>/', views.PostCategoryListView.as_view(), name='post_by_category'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name="post_detail"),
]
