# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models         import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions             import ValidationError
from django.test                        import TestCase
from rest_framework.test                import APIClient
from rest_framework.reverse             import reverse

from openbook.test                      import ModelViewSetTestMixin
from ..middleware.current_user          import reset_current_user
from ..models.allowed_role_permission   import AllowedRolePermission
from ..models.user                      import User
from ..utils                            import permission_for_perm_string
from ..validators                       import validate_permissions
from ..utils                            import content_type_for_model_string

class AllowedRolePermission_Test_Mixin:
    def setUp(self):
        super().setUp()
        reset_current_user()
        
        self.scope_type = content_type_for_model_string("openbook_course.course")

        AllowedRolePermission.objects.create(
            scope_type = self.scope_type,
            permission = permission_for_perm_string("admin.add_logentry"),
        )

        AllowedRolePermission.objects.create(
            scope_type = self.scope_type,
            permission = permission_for_perm_string("admin.view_logentry"),
        )

class AllowedRolePermission_Model_Tests(AllowedRolePermission_Test_Mixin, TestCase):
    """
    Tests for the `AllowedRolePermission` model.
    """
    def test_validate_permissions(self):
        """
        Validation must only whitelisted permissions for roles or scopes.

        NOTE: Calling `add()` or `set()` on a relationship field automatically saves the relationship.
        Validation must therefor be handled by higher levels, which is why only the implementation of
        it is tested here.
        """
        allowed = [
            permission_for_perm_string("admin.add_logentry"),
            permission_for_perm_string("admin.view_logentry"),
        ]

        disallowed = [
            permission_for_perm_string("admin.change_logentry"),
        ]

        validate_permissions(self.scope_type, allowed)

        with self.assertRaises(ValidationError):
            validate_permissions(self.scope_type, disallowed)
    
class AllowedRolePermission_ViewSet_Tests(AllowedRolePermission_Test_Mixin, TestCase):
    """
    Tests for the `AllowedRolePermissionViewSet` REST API.
    """
    def setUp(self):
        super().setUp()

        self.client = APIClient()

        self.user = User.objects.create_user(username="test", password="password")
        self.client.login(username="test", password="password")

        content_type = ContentType.objects.get_for_model(AllowedRolePermission)
        perms = Permission.objects.filter(content_type=content_type)
        self.user.user_permissions.set(perms)

        self.url_list = reverse("allowed_role_permission-list")

    def test_list(self):
        """
        List should return allowed role permissions.
        """
        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertGreaterEqual(response.data["count"], 2)

    def test_search(self):
        """
        List should support search by _search query param.
        """
        response = self.client.get(self.url_list, {"_search": "logentry"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertTrue(any("logentry" in str(r) for r in response.data["results"]))

    def test_sort(self):
        """
        List should support sorting by _sort query param.
        """
        response = self.client.get(self.url_list, {"_sort": "-permission"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

    def test_pagination(self):
        """
        List should support pagination with _page and _page_size.
        """
        response = self.client.get(self.url_list, {"_page": 1, "_page_size": 1})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_not_allowed(self):
        """
        POST method to create new entry is not allowed.
        """
        perm = Permission.objects.get(codename="add_logentry")

        response = self.client.post(self.url_list, {
            "scope_type": self.scope_type.pk,
            "permission": perm.pk,
        })

        self.assertEqual(response.status_code, 405)

    def test_update_not_allowed(self):
        """
        PUT method to update an existing entry is not allowed.
        """
        obj  = AllowedRolePermission.objects.first()
        perm = Permission.objects.get(codename="view_logentry")
        url  = reverse("allowed_role_permission-detail", args=[obj.pk])

        response = self.client.put(url, {
            "scope_type": self.scope_type.pk,
            "permission": perm.pk,
        })

        self.assertEqual(response.status_code, 405)

    def test_partial_update_not_allowed(self):
        """
        PATCH method to partially update an existing entry is not allowed.
        """
        obj  = AllowedRolePermission.objects.first()
        perm = Permission.objects.get(codename="view_logentry")
        url  = reverse("allowed_role_permission-detail", args=[obj.pk])

        response = self.client.patch(url, {"permission": perm.pk}, format="json")
        self.assertEqual(response.status_code, 405)

    def test_delete_not_allowed(self):
        """
        DELETE method to delete an existing entry is not allowed.d
        """
        obj = AllowedRolePermission.objects.first()
        url = reverse("allowed_role_permission-detail", args=[obj.pk])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 405)

    def test_anonymous_list_allowed(self):
        """
        Anonymous users can list entries.
        """
        reset_current_user()
        self.client.logout()

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)

    def test_404_for_nonexistent(self):
        """
        Operations on non-existing objects should return 404.
        """
        url = reverse("allowed_role_permission-detail", args=[999999])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)