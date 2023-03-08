from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path("<str:username>/", views.ProfileHomeView.as_view(), name='profile_home'),
    path("<str:username>/<int:pk>/delete/", views.ProfileDeleteView.as_view(), name='profile_delete'),
    path('profile/<int:pk>/update', views.ProfileUpdateView.as_view(), name='profile_update'),
]
