# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions        import PermissionDenied
from django.core.exceptions        import ValidationError
from django.urls                   import reverse
from django.test                   import TestCase
from rest_framework.test           import APIClient
from unittest.mock                 import patch

from openbook.course.models.course import Course
from ..middleware.current_user     import reset_current_user
from ..models.enrollment_method    import EnrollmentMethod
from ..models.role                 import Role
from ..models.role_assignment      import RoleAssignment
from ..models.user                 import User
from ..utils                       import model_string_for_content_type
from ..utils                       import permission_for_perm_string

class EnrollmentMethod_Test_Mixin:
    def setUp(self):
        super().setUp()
        reset_current_user()

        self.user   = User.objects.create_user(username="new", email="new@test.com", password="password")
        self.owner  = User.objects.create_user(username="owner", email="owner@test.com", password="password")
        self.course = Course.objects.create(name="Test Course 1", slug="test-course1", text_format=Course.TextFormatChoices.MARKDOWN, owner=self.owner)

        self.course.public_permissions.add(
            permission_for_perm_string("openbook_auth.self_enroll"),
        )

        self.role = Role.from_obj(self.course, name="Student", slug="student", priority=0)
        self.role.save()

        self.em_passphrase = EnrollmentMethod.from_obj(self.course, name="self-enrollment with passphrase", role=self.role, passphrase="Correct!")
        self.em_passphrase.save()

        self.em_no_passphrase = EnrollmentMethod.from_obj(self.course, name="self-enrollment", role=self.role)
        self.em_no_passphrase.save()

        self.course_no_self_enroll = Course.objects.create(name="Test Course 2", slug="test-course2", text_format=Course.TextFormatChoices.MARKDOWN, owner=self.owner)
        self.em_course_no_self_enroll = EnrollmentMethod.from_obj(self.course_no_self_enroll, name="self-enrollment", role=self.role)
        self.em_course_no_self_enroll.save()

class EnrollmentMethod_Model_Tests(EnrollmentMethod_Test_Mixin, TestCase):
    """
    Tests for the `EnrollmentMethod` model.
    """
    def test_role_scope(self):
        """
        The assigned role must belong to the same scope.
        """
        wrong_scope = Course.objects.create(name="Other Course", slug="other-course", text_format=Course.TextFormatChoices.MARKDOWN, owner=self.owner)
        wrong_role  = Role.from_obj(wrong_scope, name="Wrong Scope", slug="wrong-scope", priority=0)
        wrong_role.save()

        enrollment_method = EnrollmentMethod.from_obj(self.course, name="wrong-role", role=wrong_role)

        with self.assertRaises(ValidationError):
            enrollment_method.clean()

    def test_enroll_called(self):
        """
        `RoleAssignment.enroll()` should be called when a user self-enrolls.
        """
        with patch.object(RoleAssignment, "enroll") as mock_enroll:
            self.em_no_passphrase.enroll(user=self.user, check_passphrase=False)
            
            mock_enroll.assert_called_once_with(
                enrollment       = self.em_no_passphrase,
                user             = self.user,
                passphrase       = None,
                check_passphrase = False,
                check_permission = False,
            )

    def test_return_role_assignment(self):
        """
        `RoleAssignment` object should be returned when a user self-enrolls.
        """
        result = self.em_no_passphrase.enroll(user=self.user, check_passphrase=False)
        self.assertIsInstance(result, RoleAssignment)
    
    def test_self_enrollment_disabled_permission_denied(self):
        """
        `PermissionDenied` should be raised when public permissions of a scope
        lack the `openbook_auth.self_enroll` permission.
        """
        with self.assertRaises(PermissionDenied):
            self.em_course_no_self_enroll.enroll(user=self.user)

    def test_wrong_passphrase_permission_denied(self):
        """
        `PermissionDenied` should be raised when a wrong passphrase is used.
        """
        with self.assertRaises(PermissionDenied):
            self.em_passphrase.enroll(user=self.user, passphrase="Wrong!")

    def test_skip_passphrase_check(self):
        """
        Wrong passphrase is ignored when `check_passphrase` is `False`.
        """
        self.em_passphrase.enroll(user=self.user, passphrase="Wrong!", check_passphrase=False)

    def test_correct_passphrase(self):
        """
        Correct passphrase creates new role assignment.
        """
        self.assertEqual(RoleAssignment.objects.filter(
            user = self.user,
            role = self.role,
        ).count(), 0)

        self.em_passphrase.enroll(user=self.user, passphrase="Correct!")

        self.assertEqual(RoleAssignment.objects.filter(
            user = self.user,
            role = self.role,
        ).count(), 1)
    
    def test_without_passphrase(self):
        """
        Users can always self-assign when no passphrase is required.
        """
        self.assertEqual(RoleAssignment.objects.filter(
            user = self.user,
            role = self.role,
        ).count(), 0)

        self.em_no_passphrase.enroll(user=self.user)

        self.assertEqual(RoleAssignment.objects.filter(
            user = self.user,
            role = self.role,
        ).count(), 1)

class EnrollmentMethod_ViewSet_Tests(EnrollmentMethod_Test_Mixin, TestCase):
    """
    Tests for the `EnrollmentMethodViewSet` REST API.
    """
    def setUp(self):
        super().setUp()

        self.client = APIClient()
        self.client.login(username="owner", password="password")

        self.url_list                 = reverse("enrollment_method-list")
        self.url_no_passphrase_detail = reverse("enrollment_method-detail", args=[str(self.em_no_passphrase.pk)])
        self.url_no_passphrase_enroll = reverse("enrollment_method-enroll", args=[str(self.em_no_passphrase.pk)])
        self.url_passphrase_detail    = reverse("enrollment_method-detail", args=[str(self.em_passphrase.pk)])
        self.url_passphrase_enroll    = reverse("enrollment_method-enroll", args=[str(self.em_passphrase.pk)])
        self.url_no_self_enroll       = reverse("enrollment_method-enroll", args=[str(self.em_course_no_self_enroll.pk)])
    
    def test_list_requires_auth(self):
        """
        Anonymous users cannot list entries.
        """
        reset_current_user()
        self.client.logout()

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 403)
        
    def test_list(self):
        """
        List should return enrollment methods.
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
        response = self.client.get(self.url_list, {"_search": "passphrase"})
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_sort(self):
        """
        List should support sorting by _sort query param.
        """
        response = self.client.get(self.url_list, {"_sort": "name"})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)

    def test_pagination(self):
        """
        List should support pagination with _page and _page_size.
        """
        response = self.client.get(self.url_list, {"_page": 1, "_page_size": 1})

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data["results"]), 1)

    def test_create(self):
        """
        POST method should create new entry.
        """
        response = self.client.post(self.url_list, {
            "scope_type":    model_string_for_content_type(self.role.scope_type),
            "scope_uuid":    str(self.role.scope_uuid),
            "name":          "Self-Enrollment",
            "role_slug":     "student",
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Self-Enrollment")

    def test_create_requires_auth(self):
        """
        Create should require authentication.
        """
        reset_current_user()
        self.client.logout()

        response = self.client.post(self.url_list, {
            "scope_type":    model_string_for_content_type(self.role.scope_type),
            "scope_uuid":    str(self.role.scope_uuid),
            "name":          "Self-Enrollment",
            "role_slug":     "student",
        })

        self.assertEqual(response.status_code, 403)

    def test_update(self):
        """
        PUT method should update existing entry.
        """
        response = self.client.put(self.url_no_passphrase_detail, {
            "scope_type":    model_string_for_content_type(self.role.scope_type),
            "scope_uuid":    str(self.role.scope_uuid),
            "role_slug":     "student",
            "name":          "Updated Name",
            "is_active":     False,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Updated Name")
        self.assertEqual(response.data["is_active"], False)

    def test_partial_update(self):
        """
        PATCH method should partially update existing entry.
        """
        response = self.client.patch(self.url_no_passphrase_detail, {"name": "Partially Updated"}, format="json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Partially Updated")

    def test_delete(self):
        """
        DELETE method should delete existing entry.
        """
        response = self.client.delete(self.url_no_passphrase_detail)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(EnrollmentMethod.objects.filter(pk=self.em_no_passphrase.pk).exists())

    def test_404_for_nonexistent(self):
        """
        Operations for non-existent object should return 404.
        """
        url = reverse("enrollment_method-detail", args=[999999])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_self_enrollment_no_passphrase(self):
        """
        Self-enrollment with no password required.
        """
        reset_current_user()
        self.client.logout()
        self.client.login(username="new", password="password")

        response = self.client.put(self.url_no_passphrase_enroll)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(RoleAssignment.objects.filter(
            user = self.user,
            role = self.role,
        ).count(), 1)
    
    def test_self_enrollment_correct_passphrase(self):
        """
        Self-enrollment with correct password.
        """
        reset_current_user()
        self.client.logout()
        self.client.login(username="new", password="password")

        response = self.client.put(self.url_passphrase_enroll, {"passphrase": "Correct!"})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(RoleAssignment.objects.filter(
            user = self.user,
            role = self.role,
        ).count(), 1)

    def test_self_enrollment_wrong_passphrase(self):
        """
        Self-enrollment with wrong password not possible.
        """
        reset_current_user()
        self.client.logout()
        self.client.login(username="new", password="password")

        response = self.client.put(self.url_passphrase_enroll, {"passphrase": "Wrong!"})
        self.assertEqual(response.status_code, 403)

        self.assertEqual(RoleAssignment.objects.filter(
            user = self.user,
            role = self.role,
        ).count(), 0)
    
    def test_self_enrollment_disabled_permission_denied(self):
        """
        `PermissionDenied` should be raised when public permissions of a scope
        lack the `openbook_auth.self_enroll` permission.
        """
        reset_current_user()
        self.client.logout()
        self.client.login(username="new", password="password")

        response = self.client.put(self.url_no_self_enroll)
        self.assertEqual(response.status_code, 403)

        self.assertEqual(RoleAssignment.objects.filter(
            user = self.user,
            role = self.role,
        ).count(), 0)