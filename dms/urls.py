from django.urls import path
from .views import dms_index


urlpatterns = [
    path("", dms_index, name="dms_index"),
]
