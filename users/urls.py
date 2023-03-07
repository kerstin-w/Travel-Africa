from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path("<str:username>/", views.ProfileHomeView.as_view(), name='profile_home'),
    path('profile/<int:pk>/update', views.ProfileUpdateView.as_view(), name='profile_update'),
]
