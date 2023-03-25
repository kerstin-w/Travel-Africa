"""travelafrica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import urls as user_urls
from django.conf.urls import handler404, handler500
from blog.views import Error403View, Error404View

# Custom Error Page Handlers
handler403 = Error403View.as_view()
handler404 = Error404View.as_view()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("summernote/", include("django_summernote.urls")),
    path("", include("blog.urls"), name="blog-urls"),
    path("accounts/", include("allauth.urls")),
    path("", include(user_urls, namespace="users")),
    # Custom Error Page Handlers
    path("403/", handler403, name="handler403"),
    path("404/", handler404, name="handler404"),
]
