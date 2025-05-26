# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models       import Permission
from django.test                      import TestCase
from rest_framework.test              import APIClient
from django.urls                      import reverse

from openbook.core.models.language    import Language
from ..middleware.current_user        import reset_current_user
from ..models.permission              import Permission_T
from ..models.user                    import User

class PermissionT_ViewSet_Tests(TestCase):
    """
    Tests for the `PermissionTViewSet` REST API.
    """

    def setUp(self):
        reset_current_user()

        self.user       = User.objects.create_user(username="user", password="password")
        self.language   = Language.objects.create(language="en", name="English")
        self.permission = Permission.objects.first()
        self.translated_permission = Permission_T.objects.create(parent=self.permission, name="Test Permission Name", language=self.language)

        view_perm = Permission.objects.get(codename="view_permission_t")
        self.user.user_permissions.add(view_perm)

        self.client = APIClient()
        self.client.login(username="user", password="password")

    def test_list_permissions(self):
        """
        Should return a list of translated permissions with correct structure.
        """
        url = reverse("permission-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIsInstance(response.data["results"], list)

    def test_list_permissions_anonymous(self):
        """
        Should allow anonymous users to list translated permissions.
        """
        self.client.logout()

        url = reverse("permission-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIsInstance(response.data["results"], list)

    def test_search_permissions(self):
        """
        Should filter permissions by search query.
        """
        url = reverse("permission-list")
        response = self.client.get(url, {"_search": "Test Perm"})

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_sort_permissions(self):
        """
        Should sort permissions by given field.
        """
        url = reverse("permission-list")
        response = self.client.get(url, {"_sort": "name"})

        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        """
        Should paginate results with _page and _page_size.
        """
        url = reverse("permission-list")
        response = self.client.get(url, {"_page": 1, "_page_size": 1})

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data["results"]), 1)

    def test_update_permission_not_allowed(self):
        """
        Should not allow updating a translated permission (405 Method Not Allowed).
        """
        url = reverse("permission-detail", args=[self.translated_permission.id])

        response = self.client.put(url, {
            "name":     "Updated Name",
            "language": "en",
            "parent":   self.permission.id,
        })

        self.assertEqual(response.status_code, 405)

    def test_partial_update_permission_not_allowed(self):
        """
        Should not allow partial update of a translated permission (405 Method Not Allowed).
        """
        url = reverse("permission-detail", args=[self.translated_permission.id])
        response = self.client.patch(url, {"name": "Partially Updated"}, format="json")

        self.assertEqual(response.status_code, 405)

    def test_delete_permission_not_allowed(self):
        """
        Should not allow deleting a translated permission (405 Method Not Allowed).
        """
        url = reverse("permission-detail", args=[self.translated_permission.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 405)

    def test_create_permission_not_allowed(self):
        """
        Should not allow creating a translated permission (405 Method Not Allowed).
        """
        url = reverse("permission-list")

        response = self.client.post(url, {
            "parent": self.permission.id,
            "name": "Another Name",
            "language": "de",
        })

        self.assertEqual(response.status_code, 405)

    def test_404_for_nonexistent_object(self):
        """
        Should return 404 for non-existent object access.
        """
        url = reverse("permission-detail", args=[999999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)