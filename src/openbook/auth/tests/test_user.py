# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth       import get_user_model
from django.core.exceptions    import ValidationError
from django.test               import TestCase
from django.urls               import reverse
from rest_framework.test       import APIClient

from ..middleware.current_user import reset_current_user
from ..models.user             import User
from ..models.user_profile     import UserProfile

class User_Model_Tests(TestCase):
    """
    Tests for the `User` and `UserProfile` models.
    """
    def test_user_creation_without_email(self):
        """
        The e-mail address should be obligatory when a new user is created.
        """
        # Directly saving without validation works
        User.objects.create_user("test1", password="test1234")

        # Model validation should raise an exception
        with self.assertRaises(ValidationError):
            user = User(username="test2", password="test1234")
            user.full_clean()
            user.save()

    def test_user_profile_created(self):
        """
        Each user should have a user profile, automatically created when a new
        user is created.
        """
        # User profile gets automatically created
        User = get_user_model()
        user = User.objects.create_user("test", password="test1234", email="test@example.com")

        self.assertEqual(
            UserProfile.objects.filter(user=user).count(), 1,
            "User profile was not created when a new user is created."
        )

        # User profile remains untouched after re-saving the user
        user_profile = user.profile
        user_profile.description = "Should not get lost!"

        user.save()

        self.assertIs(
            user_profile, user.profile,
            "User profile was overwritten when the user was saved again."
        )

        self.assertEqual(
            user_profile.description, user.profile.description,
            "User profile description got lost after saving user."
        )

class User_ViewSet_Test(TestCase):
    """
    Tests for the `UserViewSet` REST API.
    """
    def setUp(self):
        reset_current_user()

        self.user1 = User.objects.create_user("user1", password="password", email="user1@test.com")
        self.user2 = User.objects.create_user("user2", password="password", email="user2@test.com")
        self.user3 = User.objects.create_user("user3", password="password", email="user3@test.com")
        self.admin = User.objects.create_user("admin", password="password", email="admin@test.com", is_staff=True, is_superuser=True)

        self.url_list  = reverse("user-list")
        self.url_user1 = reverse("user-detail", args=[str(self.user1.username)])
        self.url_user2 = reverse("user-detail", args=[str(self.user2.username)])
        self.url_user3 = reverse("user-detail", args=[str(self.user3.username)])

        self.client = APIClient()
        self.client.login(username="user1", password="password")

    def test_list_requires_auth(self):
        """
        List should require authentication.
        """
        reset_current_user()
        self.client.logout()

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 403)

    def test_list(self):
        """
        List should return users.
        """
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIsInstance(response.data["results"], list)

    def test_search(self):
        """
        List should support search by _search query param.
        """
        response = self.client.get(self.url_list, {"_search": "1@test"})
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_sort(self):
        """
        List should support sorting by _sort query param.
        """
        response = self.client.get(self.url_list, {"_sort": "username"})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

    def test_pagination(self):
        """
        List should support pagination with _page and _page_size.
        """
        response = self.client.get(self.url_list, {"_page": 1, "_page_size": 1})

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data["results"]), 1)

    def test_create_not_allowed(self):
        """
        POST method to create a new user is not allowed.
        """
        response = self.client.post(self.url_list, {
            "username": "new-user",
            "password": "password",
            "email":    "new-user@test.com",
        })

        self.assertEqual(response.status_code, 405)

    def test_update_own_user(self):
        """
        PUT method should update own user profile.
        """
        response = self.client.put(self.url_user1, {
            "password":        "password",
            "email":           "user1@test.com",
            "description":     "Updated",
            "profile_picture": "",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], "Updated")
    
    def test_update_other_user_forbidden(self):
        """
        PUT method to update another user is not allowed.
        """
        response = self.client.put(self.url_user2, {
            "password":        "password",
            "email":           "user1@test.com",
            "description":     "Updated",
            "profile_picture": "",
        })

        self.assertEqual(response.status_code, 403)

    def test_partial_update_own_user(self):
        """
        PATCH method should partially update own user.
        """
        response = self.client.patch(self.url_user1, {"description": "Partially Updated"}, format="json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["description"], "Partially Updated")
    
    def test_partial_update_other_user_forbidden(self):
        """
        PATCH method to partially update another user is not allowed.
        """
        response = self.client.patch(self.url_user2, {"description": "Partially Updated"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_own_user(self):
        """
        DELETE method should delete own user.
        """
        response = self.client.delete(self.url_user1)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(User.objects.filter(username=self.user1.username).exists())

    def test_delete_other_user_forbidden(self):
        """
        DELETE method to delete another user is not allowed.
        """
        response = self.client.delete(self.url_user2)
        self.assertEqual(response.status_code, 403)

    def test_404_for_nonexistent(self):
        """
        Operations for non-existent object should return 404.
        """
        url = reverse("user-detail", args=["non-existing"])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)