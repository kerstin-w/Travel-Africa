from . import views
from django.urls import path


urlpatterns = [
    path("", views.PostFeaturedList.as_view(), name='home'),
]
