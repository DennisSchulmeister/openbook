# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models    import Permission
from django.test                   import TestCase
from django.urls                   import reverse
from rest_framework.test           import APIClient

from openbook.core.models.language import Language
from ..models.permission           import Permission_T
from ..models.user                 import User
from ..middleware.current_user     import reset_current_user

class PermissionT_ViewSet_Tests(TestCase):
    """
    Tests for the `PermissionTViewSet` REST API.
    """
    def setUp(self):
        view_perm = Permission.objects.get(codename="view_permission_t")
        self.user = User.objects.create_user(username="username", password="password", email="user@test.com")
        self.user.user_permissions.add(view_perm)

        self.permission = Permission.objects.first()
        self.language = Language.objects.create(language="en", name="English")
        self.translated_permission = Permission_T.objects.create(parent=self.permission, language=self.language, name="Test Permission Name")

        self.client = APIClient()
        self.client.login(username="username", password="password")

        self.list_url   = reverse("permission-list")
        self.detail_url = reverse("permission-detail", args=[self.translated_permission.id])
        
    def test_list(self):
        """
        List should return allowed translated permissions.
        """
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIsInstance(response.data["results"], list)

    def test_search(self):
        """
        List should support search by _search query param.
        """
        response = self.client.get(self.list_url, {"_search": "Test Permission Name"})
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_sort(self):
        """
        List should support sorting by _sort query param.
        """
        response = self.client.get(self.list_url, {"_sort": "name"})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

    def test_pagination(self):
        """
        List should support pagination with _page and _page_size.
        """
        response = self.client.get(self.list_url, {"_page": 1, "_page_size": 1})

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data["results"]), 1)

    def test_create_not_allowed(self):
        """
        POST method to create new entry is not allowed.
        """
        response = self.client.post(self.list_url, {
            "parent":   self.permission.id,
            "name":     "Another Name",
            "language": "de",
        })

        self.assertEqual(response.status_code, 405)

    def test_update_not_allowed(self):
        """
        PUT method to update an existing entry is not allowed.
        """
        response = self.client.put(self.detail_url, {
            "name":     "Updated Name",
            "language": "en",
            "parent":   self.permission.id,
        }
        )
        self.assertEqual(response.status_code, 405)

    def test_partial_update_not_allowed(self):
        """
        PATCH method to partially update an existing entry is not allowed.
        """
        response = self.client.patch(self.detail_url, {"name": "Partially Updated"}, format="json")
        self.assertEqual(response.status_code, 405)

    def test_delete_not_allowed(self):
        """
        DELETE method to delete an existing entry is not allowed.d
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 405)

    def test_anonymous_list_not_allowed(self):
        """
        Anonymous users cannot list entries.
        """
        # Remove all permissions
        reset_current_user()
        self.client.logout()

        response = self.client.post(self.list_url, {"parent": self.permission.id, "name": "X", "language": "en"})
        self.assertEqual(response.status_code, 403)

    def test_404_for_nonexistent(self):
        """
        Operations for non-existent object should return 404.
        """
        url = reverse("permission-detail", args=[999999])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)