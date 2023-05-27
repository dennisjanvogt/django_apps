from django.urls import path
from .views import *


urlpatterns = [
    path("", dms_index, name="dms_index"),
]
