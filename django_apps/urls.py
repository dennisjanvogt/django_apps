from django import views
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("organisation/", include("organisation.urls.urls")),
    path("", include("index.urls")),
]
