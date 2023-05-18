from django.urls import path
from . import patterns
from ..views.views import home

urlpatterns = [
    path("", home, name="home"),
] + patterns


""" [
    # Dashboard
    path(
        "dashboard/vertragsuebersicht/",
        dashboard_vertragsuebersicht,
        name="dashboard_vertragsuebersicht",
    ),
    path(
        "dashboard/schadensuebersicht/",
        dashboard_schadensuebersicht,
        name="dashboard_schadensuebersicht",
    ),
]
 """
