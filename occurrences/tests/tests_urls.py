"""
This file test its associated with all the urls used in this project.
Each method included in 'TestUrls' tests a specific endpoint (the method
type dependes on the call). The main purpose is to verify if the defined name
of each url its correctly associated with his view.
"""
# django imports
from django.test import SimpleTestCase
from django.urls import reverse, resolve

# occurrences imports
from occurrences import views

# rest_framework_jwt imports
from rest_framework_jwt.views import obtain_jwt_token


class TestUrls(SimpleTestCase):
    def test_login_url_resolves(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func, obtain_jwt_token)

    def test_register_url_resolves(self):
        url = reverse("register")
        self.assertEquals(resolve(url).func, views.user_registration)

    def test_occurrences_patch_url_resolves(self):
        url = reverse("occurrences-patch", args=[3])
        self.assertEquals(resolve(url).func, views.occurrences_patch)

    def test_occurreneces_get_delete_update_url_resolves(self):
        url = reverse("occurrences_get_update_delete", args=[3])
        self.assertEquals(resolve(url).func, views.occurrences_get_update_delete)

    def test_occurrences_list_url_resolves(self):
        url = reverse("occurrences-list")
        self.assertEquals(resolve(url).func, views.occurrence_list_all)

    def test_occurrences_url_resolves(self):
        url = reverse("occurrences")
        self.assertEquals(resolve(url).func, views.occurrence_own_add)

    def test_users_get_url_resolves(self):
        url = reverse("users-get", args=[3])
        self.assertEquals(resolve(url).func, views.users_get)

    def test_users_delete_url_resolves(self):
        url = reverse("users-delete", args=[3])
        self.assertEquals(resolve(url).func, views.user_delete)

    def test_users_url_resolves(self):
        url = reverse("users")
        self.assertEquals(resolve(url).func, views.users_list)