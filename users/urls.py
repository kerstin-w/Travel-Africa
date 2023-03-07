from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path("<str:username>/", views.ProfileHomeView.as_view(), name='profile_home'),
]
