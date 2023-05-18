from django.urls import path

from ..views.api_views import (
    kunde_list_create,
    kunde_retrieve_update_destroy,
    mitarbeiter_list_create,
    mitarbeiter_retrieve_update_destroy,
    schaden_list_create,
    schaden_retrieve_update_destroy,
    versicherungsvertrag_list_create,
    versicherungsvertrag_retrieve_update_destroy,
)


urlpatterns = [
    path(
        "api/mitarbeiter/",
        mitarbeiter_list_create,
        name="mitarbeiter_list_create",
    ),
    path(
        "api/mitarbeiter/<int:pk>/",
        mitarbeiter_retrieve_update_destroy,
        name="mitarbeiter_retrieve_update_destroy",
    ),
    path("api/kunden/", kunde_list_create, name="kunde_list_create"),
    path(
        "api/kunden/<int:pk>/",
        kunde_retrieve_update_destroy,
        name="kunde_retrieve_update_destroy",
    ),
    path(
        "api/vertraege/",
        versicherungsvertrag_list_create,
        name="versicherungsvertrag_list_create",
    ),
    path(
        "api/vertraege/<int:pk>/",
        versicherungsvertrag_retrieve_update_destroy,
        name="versicherungsvertrag_retrieve_update_destroy",
    ),
    path("api/schaeden/", schaden_list_create, name="schaden_list_create"),
    path(
        "api/schaeden/<int:pk>/",
        schaden_retrieve_update_destroy,
        name="schaden_retrieve_update_destroy",
    ),
]
