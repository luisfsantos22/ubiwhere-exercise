"""
This file contains all the endpoints patterns from the views.py file.
They are organized by modules 'Authentication', 'Occurrences' and 'Users'.
Login endpoint its imported by rest_framework-jwt library
"""
# django imports
from django.urls import path

# local imports
from . import views

# rest_framework_jwt imports
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # Authentication
    path("login/", obtain_jwt_token, name="login"),
    path("register/", views.user_registration, name="register"),
    # Occurrences
    path("occurrences-list/", views.occurrence_list_all, name="occurrences-list"),
    path(
        "occurrences-patch/<occurrence_id>",
        views.occurrences_patch,
        name="occurrences-patch",
    ),
    path(
        "occurrences/<occurrence_id>",
        views.occurrences_get_update_delete,
        name="occurrences_get_update_delete",
    ),
    path("occurrences/", views.occurrence_own_add, name="occurrences"),
    # Users
    path("users/<user_id>", views.users_get, name="users-get"),
    path("users-delete/<user_id>", views.user_delete, name="users-delete"),
    path("users/", views.users_list, name="users"),
]
