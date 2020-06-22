"""
This file test its associated with all the views used in this project.
Each method included in 'TestViews' tests a specific view. 
The main purpose is to verify if the views have errors or bugs.
For each view, possible errors or bad calls are tested and,
at the same time, correct requests.
"""
# django imports
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        """
        Pre-execute variables to use on the methods
        """
        self.client = Client()
        # users
        self.username = "test-ubi"
        self.password = "password"
        self.username2 = "test-ubi2"
        self.password2 = "password2"
        self.super_username = "test-ubi-super"
        self.super_password = "password-super"
        self.users_list = reverse("users")
        # Auth
        self.login = reverse("login")
        self.regist = reverse("register")
        self.registration = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.registration2 = User.objects.create_user(
            username=self.username2, password=self.password2
        )
        self.regist_superuser = User.objects.create_superuser(
            username=self.super_username, password=self.super_password
        )
        # occurrences
        self.occurence = reverse("occurrences")
        self.occurrences = reverse("occurrences")
        self.occurrences_list = reverse("occurrences-list")

    # Successfull requests
    def test_registration_POST_201(self):
        """
        Method to test successfull regists
        """
        response = self.client.post(
            self.regist,
            {
                "username": "test-user",
                "password": "password-test",
                "email": "example.com",
            },
        )

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data["username"], "test-user")

    def test_login_POST_200(self):
        """
        Method to garantee that a user can login successfully
        """
        response = self.client.post(
            self.login, {"username": self.username, "password": self.password}
        )

        self.assertEquals(response.status_code, 200)

    def test_occurrence_PATCH_200(self):
        """
        Method to garantee that only the superuser can update a specific
        occurrence state with success
        """
        response_login = self.client.post(
            self.login,
            {"username": self.super_username, "password": self.super_password},
        )

        occurrence = self.client.post(
            self.occurence,
            {
                "description": "Evento 10",
                "address": "Tower Bridge, London",
                "category": "INCIDENT",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(occurrence.status_code, 201)

        response_patch = self.client.patch(
            reverse("occurrences-patch", args=[occurrence.data["id"]]),
            {"state": "RESOLVED"},
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_patch.status_code, 200)

    def test_occurrences_GET_UPDATE_DELETE_200(self):
        """
        Method to test three different requests with the same endpoint. Here its tested
        'GET', 'UPDATE' and 'DELETE' request methods of a specific occurrence with success.
        """
        response_login = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        occurrence_response = self.client.post(
            self.occurence,
            {
                "description": "Evento 10",
                "address": "Tower Bridge, London",
                "category": "INCIDENT",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        # GET
        get_occurrence_response = self.client.get(
            reverse(
                "occurrences_get_update_delete", args=[occurrence_response.data["id"]]
            ),
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(get_occurrence_response.status_code, 200)
        self.assertEquals(get_occurrence_response.data["description"], "Evento 10")

        # UPDATE
        update_occurrence_response = self.client.put(
            reverse(
                "occurrences_get_update_delete", args=[occurrence_response.data["id"]]
            ),
            {
                "description": "Evento Praia",
                "address": "Tower Bridge, London",
                "category": "WEATHER_CONDITION",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(update_occurrence_response.status_code, 200)
        self.assertEquals(
            update_occurrence_response.data["description"], "Evento Praia"
        )
        self.assertEquals(
            update_occurrence_response.data["category"], "WEATHER_CONDITION"
        )

        # DELETE
        delete_occurrence_response = self.client.delete(
            reverse(
                "occurrences_get_update_delete", args=[occurrence_response.data["id"]]
            ),
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(delete_occurrence_response.status_code, 200)
        get_occurrence_response = self.client.get(
            reverse(
                "occurrences_get_update_delete", args=[occurrence_response.data["id"]]
            ),
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(get_occurrence_response.status_code, 404)

    def test_occurrence_list_GET_200(self):
        """
        This method its associated with listing all occurrences with or without
        filters successfully.
        """
        response_login = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        self.client.post(
            self.occurence,
            {
                "description": "Evento 10",
                "address": "Tower Bridge, London",
                "category": "INCIDENT",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.client.post(
            self.occurence,
            {
                "description": "Evento 11",
                "address": "Eiffel Tower, France",
                "category": "SPECIAL_EVENT",
                "latitude": "35.922329",
                "longitude": "-2.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        response_occurrences = self.client.get(
            self.occurrences_list,
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_occurrences.status_code, 200)
        self.assertEquals(len(response_occurrences.data), 2)

        # with filters
        # Categories
        response_filter_category_occurrences = self.client.get(
            self.occurrences_list,
            {"category": "SPECIAL_EVENT"},
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_filter_category_occurrences.status_code, 200)
        self.assertEquals(len(response_filter_category_occurrences.data), 1)

        # Author
        author_username = User.objects.get(username=self.username)
        response_filter_author_occurrences = self.client.get(
            self.occurrences_list,
            {"author": author_username},
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_filter_author_occurrences.status_code, 200)
        self.assertEquals(len(response_filter_author_occurrences.data), 2)

        author_username = User.objects.get(username=self.username)
        response_filter_author_occurrences = self.client.get(
            self.occurrences_list,
            {"author": "none"},
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_filter_author_occurrences.status_code, 200)
        self.assertEquals(len(response_filter_author_occurrences.data), 0)

        # Radius
        response_radius_author_occurrences = self.client.get(
            self.occurrences_list,
            {"radius": "100", "latitude": "35.822329", "longitude": "-2.961871"},
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_radius_author_occurrences.status_code, 200)
        self.assertEquals(len(response_radius_author_occurrences.data), 1)

    def test_occurences_own_POST_GET_201_200(self):
        """
        This method contains two differentes request methods of the same
        endpoint. Here its tested the creation of new occurrences and getting
        only the owner occurrences successfully.
        """
        response_login = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        occurence_response = self.client.post(
            self.occurence,
            {
                "description": "Evento 10",
                "address": "Tower Bridge, London",
                "category": "INCIDENT",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(occurence_response.status_code, 201)
        self.assertEquals(occurence_response.data["description"], "Evento 10")

        response_login2 = self.client.post(
            self.login, {"username": self.username2, "password": self.password2},
        )

        self.client.post(
            self.occurence,
            {
                "description": "Evento 11",
                "address": "Eiffel Tower, France",
                "category": "SPECIAL_EVENT",
                "latitude": "35.922329",
                "longitude": "-2.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login2.data["token"]),
        )

        response_own_occurrences = self.client.get(
            self.occurrences,
            HTTP_AUTHORIZATION="JWT {}".format(response_login2.data["token"]),
        )

        self.assertEquals(response_own_occurrences.status_code, 200)
        self.assertEquals(len(response_own_occurrences.data), 1)

    def test_users_GET_200(self):
        """
        In this method its tested getting a specific user with success.
        """
        response_login = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        response_all_user = self.client.get(
            self.users_list,
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        random_user_id = response_all_user.data[1]["id"]
        response_user = self.client.get(
            reverse("users-get", args=[random_user_id]),
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_user.status_code, 200)
        self.assertEquals(response_user.data["id"], random_user_id)

    def test_users_DELETE_200(self):
        """
        This method contains the test of removing a specific user with success
        """
        response_login = self.client.post(
            self.login,
            {"username": self.super_username, "password": self.super_password},
        )

        response_all_user = self.client.get(
            self.users_list,
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        random_user_id = response_all_user.data[1]["id"]
        response_user_delete = self.client.delete(
            reverse("users-delete", args=[random_user_id]),
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_user_delete.status_code, 200)

        response_user = self.client.get(
            reverse("users-get", args=[random_user_id]),
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_user.status_code, 404)

    def test_users_list_GET_200(self):
        """
        In this method all users info is requested and returned with success.
        """
        response_login = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        response_all_user = self.client.get(
            self.users_list,
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_all_user.status_code, 200)
        self.assertEquals(len(response_all_user.data), 2)

    # Error handler test requests
    def test_registration_POST_40x(self):
        """
        This method tests possible errors on registing a new user
        """
        # Duplicate username
        duplicate_username_response = self.client.post(
            self.regist,
            {
                "username": self.username,
                "password": "password-test",
                "email": "example.com",
            },
        )

        self.assertEquals(duplicate_username_response.status_code, 400)

        # Small password
        duplicate_username_response = self.client.post(
            self.regist,
            {"username": "test-xx", "password": "pass", "email": "example.com",},
        )

        self.assertEquals(duplicate_username_response.status_code, 400)

        # Insufficient request data
        insufficient_request_response = self.client.post(
            self.regist, {"username": "test-xx",},
        )

        self.assertEquals(insufficient_request_response.status_code, 400)

    def test_login_POST_40x(self):
        """
        This method tests possible errors during the login request
        """
        # Bad credentials
        bad_user_response = self.client.post(
            self.login, {"username": "baduser", "password": self.password}
        )

        self.assertEquals(bad_user_response.status_code, 400)

        bad_pwd_response = self.client.post(
            self.login, {"username": self.username, "password": "badpass"}
        )

        self.assertEquals(bad_pwd_response.status_code, 400)

        # Insufficient request data
        insufficient_request_response = self.client.post(
            self.login, {"username": self.username}
        )

        self.assertEquals(insufficient_request_response.status_code, 400)

    def test_occurrence_PATCH_40x(self):
        """
        This method tests possible errors on updating a specific occurrence state
        """
        response_login = self.client.post(
            self.login,
            {"username": self.super_username, "password": self.super_password},
        )
        response_login_normal = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        occurrence = self.client.post(
            self.occurence,
            {
                "description": "Evento 10",
                "address": "Tower Bridge, London",
                "category": "INCIDENT",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(occurrence.status_code, 201)

        # Wrong Enum
        wrong_enum_response_patch = self.client.patch(
            reverse("occurrences-patch", args=[occurrence.data["id"]]),
            {"state": "RESOLVEDED"},
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(wrong_enum_response_patch.status_code, 400)

        # Wrong token
        wrong_token_response = self.client.patch(
            reverse("occurrences-patch", args=[occurrence.data["id"]]),
            {},
            content_type="application/json",
            HTTP_AUTHORIZATION="WT {}".format(response_login.data["token"]),
        )

        self.assertEquals(wrong_token_response.status_code, 401)

        # Insufficient permission
        wrong_enum_response_patch = self.client.patch(
            reverse("occurrences-patch", args=[occurrence.data["id"]]),
            {"state": "RESOLVED"},
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login_normal.data["token"]),
        )

        self.assertEquals(wrong_token_response.status_code, 401)

    def test_occurrences_GET_UPDATE_DELETE_40x(self):
        """
        This method tests possible errors on deleting or updating a specific
        occurrence.
        """
        response_login = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        occurrence_response = self.client.post(
            self.occurence,
            {
                "description": "Evento 10",
                "address": "Tower Bridge, London",
                "category": "INCIDENT",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        # GET
        # Wrong args
        wrong_arg_get_occurrence_response = self.client.get(
            reverse("occurrences_get_update_delete", args=[0]),
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(wrong_arg_get_occurrence_response.status_code, 404)

        # UPDATE
        # Wrong args
        update_occurrence_response = self.client.put(
            reverse("occurrences_get_update_delete", args=[0]),
            {
                "description": "Evento Praia",
                "address": "Tower Bridge, London",
                "category": "WEATHER_CONDITION",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(update_occurrence_response.status_code, 404)

        # Wrong request data
        wrong_request_update_occurrence_response = self.client.put(
            reverse(
                "occurrences_get_update_delete", args=[occurrence_response.data["id"]]
            ),
            {
                "description": "Evento Praia",
                "address": "Tower Bridge, London",
                "category": "WEATHER_CONDITIONs",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(wrong_request_update_occurrence_response.status_code, 400)

        wrong_request_update_occurrence_response2 = self.client.put(
            reverse(
                "occurrences_get_update_delete", args=[occurrence_response.data["id"]]
            ),
            {
                "description": "Evento Praia",
                "address": "Tower Bridge, London",
                "category": "WEATHER_CONDITION",
                "latitude": "45.922329",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(wrong_request_update_occurrence_response2.status_code, 400)

        # DELETE
        # Wrong args
        delete_occurrence_response = self.client.delete(
            reverse("occurrences_get_update_delete", args=[0]),
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(delete_occurrence_response.status_code, 404)

    def test_occurrence_list_GET_40x(self):
        """
        This method tests possible errors on getting all occurrences
        """
        response_login = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        self.client.post(
            self.occurence,
            {
                "description": "Evento 10",
                "address": "Tower Bridge, London",
                "category": "INCIDENT",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.client.post(
            self.occurence,
            {
                "description": "Evento 11",
                "address": "Eiffel Tower, France",
                "category": "SPECIAL_EVENT",
                "latitude": "35.922329",
                "longitude": "-2.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        # Wrong token
        wrong_token_response_occurrences = self.client.get(
            self.occurrences_list,
            HTTP_AUTHORIZATION="WT {}".format(response_login.data["token"]),
        )

        self.assertEquals(wrong_token_response_occurrences.status_code, 401)

        # with filters
        # Wrong Categories
        wrong_response_filter_category_occurrences = self.client.get(
            self.occurrences_list,
            {"category": "SPECIAL_EVENTs"},
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(wrong_response_filter_category_occurrences.status_code, 400)

        # Radius
        # Insufficient request data
        insufficient_request_response_radius_author_occurrences = self.client.get(
            self.occurrences_list,
            {"radius": "100", "latitude": "35.822329"},
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(
            insufficient_request_response_radius_author_occurrences.status_code, 400
        )

    def test_occurences_own_POST_GET_40x(self):
        """
        This method tests possible errors on adding or getting an occurrence.
        """
        response_login = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        # Wrong request data
        # Category
        wrong_occurence_response = self.client.post(
            self.occurence,
            {
                "description": "Evento 10",
                "address": "Tower Bridge, London",
                "category": "INCIDENTs",
                "latitude": "45.922329",
                "longitude": "-9.561871",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(wrong_occurence_response.status_code, 400)

        # Insufficient request data
        insufficient_occurence_response = self.client.post(
            self.occurence,
            {
                "description": "Evento 10",
                "address": "Tower Bridge, London",
                "category": "INCIDENT",
                "latitude": "45.922329",
            },
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        insufficient_occurence_response2 = self.client.post(
            self.occurence,
            {"description": "Evento 10", "address": "Tower Bridge, London",},
            content_type="application/json",
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(insufficient_occurence_response.status_code, 400)
        self.assertEquals(insufficient_occurence_response2.status_code, 400)

        # Wrong token
        response_own_occurrences = self.client.get(
            self.occurrences,
            HTTP_AUTHORIZATION="WT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_own_occurrences.status_code, 401)

    def test_users_GET_40x(self):
        """
        This method tests possible errors getting a specific user info
        """
        response_login = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        # Wrong id
        wrong_response_user = self.client.get(
            reverse("users-get", args=[0]),
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(wrong_response_user.status_code, 404)

    def test_users_DELETE_40x(self):
        """
        This method tests possible errors on deleting a specific user
        """
        response_login = self.client.post(
            self.login,
            {"username": self.super_username, "password": self.super_password},
        )

        response_login_normal = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        # Wrong id
        wrong_id_response_user = self.client.delete(
            reverse("users-delete", args=[0]),
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        self.assertEquals(wrong_id_response_user.status_code, 404)

        # Insufficient permissions
        response_all_user = self.client.get(
            self.users_list,
            HTTP_AUTHORIZATION="JWT {}".format(response_login.data["token"]),
        )

        random_user_id = response_all_user.data[1]["id"]
        wrong_response_user_delete = self.client.delete(
            reverse("users-delete", args=[random_user_id]),
            HTTP_AUTHORIZATION="JWT {}".format(response_login_normal.data["token"]),
        )

        self.assertEquals(wrong_response_user_delete.status_code, 401)

    def test_users_list_GET_40x(self):
        """
        This method tests possible errors on getting all users info
        """
        response_login = self.client.post(
            self.login, {"username": self.username, "password": self.password},
        )

        # Wrong token
        response_all_user = self.client.get(
            self.users_list,
            HTTP_AUTHORIZATION="WT {}".format(response_login.data["token"]),
        )

        self.assertEquals(response_all_user.status_code, 401)
