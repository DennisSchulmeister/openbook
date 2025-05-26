# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions        import ValidationError
from django.core.exceptions        import PermissionDenied
from django.test                   import TestCase
from django.utils                  import timezone
from unittest.mock                 import patch
from rest_framework.test           import APIClient
from rest_framework.reverse        import reverse

from openbook.course.models.course import Course
from ..middleware.current_user     import reset_current_user
from ..models.access_request       import AccessRequest
from ..models.role                 import Role
from ..models.role_assignment      import RoleAssignment
from ..models.user                 import User
from ..utils                       import model_string_for_content_type
from ..utils                       import permission_for_perm_string

class AccessRequest_Test_Mixin:
    def setUp(self):
        reset_current_user()

        self.user_new       = User.objects.create_user(username="new", email="new@test.com", password="password")
        self.user_student   = User.objects.create_user(username="student", email="student@test.com", password="password")
        self.user_assistant = User.objects.create_user(username="assistant", email="assistant@test.com", password="password")
        self.user_owner     = User.objects.create_user(username="owner", email="owner@test.com", password="password")
        self.user_dummy     = User.objects.create_user(username="dummy", email="dummy@test.com", password="password")
        self.course         = Course.objects.create(name="Test Course", slug="test-course", text_format=Course.TextFormatChoices.MARKDOWN, owner=self.user_owner)
        self.role_student   = Role.from_obj(self.course, name="Student", slug="student", priority=0)
        self.role_assistant = Role.from_obj(self.course, name="Assistant", slug="assistant", priority=1)
        self.role_teacher   = Role.from_obj(self.course, name="Teacher", slug="teacher", priority=2)

        self.role_student.save()
        self.role_assistant.save()
        self.role_teacher.save()

        permissions = [
            permission_for_perm_string("openbook_auth.add_accessrequest"),
            permission_for_perm_string("openbook_auth.view_accessrequest"),
            permission_for_perm_string("openbook_auth.change_accessrequest"),
            permission_for_perm_string("openbook_auth.delete_accessrequest"),
            permission_for_perm_string("openbook_auth.add_roleassignment"),
            permission_for_perm_string("openbook_auth.delete_roleassignment"),
        ]

        self.role_assistant.permissions.set(permissions)
        self.role_teacher.permissions.set(permissions)

        self.user_new.user_permissions.set([
            permission_for_perm_string("openbook_auth.add_accessrequest"),
            permission_for_perm_string("openbook_auth.delete_accessrequest"),
        ])

        RoleAssignment.from_obj(self.course, user=self.user_student, role=self.role_student).save()
        RoleAssignment.from_obj(self.course, user=self.user_assistant, role=self.role_assistant).save()

class AccessRequest_Model_Tests(AccessRequest_Test_Mixin, TestCase):
    """
    Tests for the `AccessRequest` model.
    """
    def test_role_scope(self):
        """
        The assigned role must belong to the same scope.
        """
        wrong_scope = Course.objects.create(name="Other Course", slug="other-course", text_format=Course.TextFormatChoices.MARKDOWN)
        wrong_role  = Role.from_obj(wrong_scope, name="Wrong Scope", slug="wrong-scope", priority=0)
        wrong_role.save()

        access_request = AccessRequest.from_obj(self.course, user=self.user_new, role=wrong_role)

        with self.assertRaises(ValidationError):
            access_request.clean()

    def test_new_pending_decision(self):
        """
        Decision should be pending and decision date be `None` when new access request is saved.
        """
        access_request = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)
        access_request.save(check_permission=False)

        self.assertEqual(access_request.decision, AccessRequest.Decision.PENDING)
        self.assertIsNone(access_request.decision_date)

    def test_decision_date_automatically_set_on_accept(self):
        """
        Decision date should be set when access request is accepted.
        """
        access_request = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)
        access_request.save(check_permission=False)

        self.assertIsNone(access_request.decision_date)

        access_request.decision = AccessRequest.Decision.ACCEPTED
        access_request.save(check_permission=False)

        self.assertIsNotNone(access_request.decision_date)
        self.assertIsInstance(access_request.decision_date, timezone.datetime)

    def test_decision_date_automatically_set_on_deny(self):
        """
        Decision date should be set when access request is denied.
        """
        access_request = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)
        access_request.save(check_permission=False)

        self.assertIsNone(access_request.decision_date)

        access_request.decision = AccessRequest.Decision.DENIED
        access_request.save(check_permission=False)

        self.assertIsNotNone(access_request.decision_date)
        self.assertIsInstance(access_request.decision_date, timezone.datetime)

    def test_enroll_on_accept(self):
        """
        `RoleAssignment.enroll()` should be called when access request is accepted.
        """
        with patch.object(RoleAssignment, "enroll") as mock_enroll:
            access_request = AccessRequest.from_obj(self.course,
                user     = self.user_new,
                role     = self.role_student,
                decision = AccessRequest.Decision.ACCEPTED
            )

            access_request.save(check_permission=False)
            mock_enroll.assert_called_once_with(enrollment=access_request, permission_user=None, check_permission=False)

    def test_withdraw_on_deny(self):
        """
        `RoleAssignment.withdraw()` should be called when access request is denied.
        """
        with patch.object(RoleAssignment, "withdraw") as mock_withdraw:
            access_request = AccessRequest.from_obj(self.course,
                user     = self.user_new,
                role     = self.role_student,
                decision = AccessRequest.Decision.DENIED
            )

            access_request.save(check_permission=False)
            mock_withdraw.assert_called_once_with(enrollment=access_request, permission_user=None, check_permission=False)
    
    def test_role_assigned_on_accept(self):
        """
        Role should be assigned when access request is accepted.
        """
        access_request = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)
        access_request.save(check_permission=False)

        with self.assertRaises(RoleAssignment.DoesNotExist):
            RoleAssignment.objects.get(
                user = self.user_new,
                role = self.role_student,
            )

        access_request.accept(check_permission=False)

        self.assertEqual(RoleAssignment.objects.filter(
            user = self.user_new,
            role = self.role_student,
        ).count(), 1)

        self.assertEqual(access_request.decision, AccessRequest.Decision.ACCEPTED)
    
    def test_role_unassigned_on_deny(self):
        """
        Role assignment should be deleted when access request is denied.
        """
        access_request = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)
        access_request.save(check_permission=False)

        with self.assertRaises(RoleAssignment.DoesNotExist):
            RoleAssignment.objects.get(
                user = self.user_new,
                role = self.role_student,
            )

        access_request.deny(check_permission=False)

        self.assertEqual(RoleAssignment.objects.filter(
            user = self.user_new,
            role = self.role_student,
        ).count(), 0)

        self.assertEqual(access_request.decision, AccessRequest.Decision.DENIED)
    
    def test_cannot_decide_higher_priority(self):
        """
        Users cannot decide access request for roles with higher priority than their own.
        """
        access_request = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_teacher)
        access_request.save(check_permission=False)

        with self.assertRaises(PermissionDenied):
            access_request.accept(permission_user=self.user_assistant)

        with self.assertRaises(PermissionDenied):
            access_request.deny(permission_user=self.user_assistant)
    
    def test_can_decide_same_priority(self):
        """
        Users can decide access request for roles with same priority than their own.
        """
        access_request = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_assistant)
        access_request.save(check_permission=False)

        access_request.accept(permission_user=self.user_assistant)
        access_request.deny(permission_user=self.user_assistant)

    def test_can_decide_lower_priority(self):
        """
        Users can decide access request for roles with lower priority than their own.
        """
        access_request = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)
        access_request.save(check_permission=False)

        access_request.accept(permission_user=self.user_assistant)
        access_request.deny(permission_user=self.user_assistant)
    
    def test_accept_permission(self):
        """
        User's role must include "openbook_auth.add_roleassignment" permission to accept access requests.
        """
        # First try without permission
        access_request1 = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)

        access_request2 = AccessRequest.from_obj(self.course,
            user     = self.user_new,
            role     = self.role_student,
            decision = AccessRequest.Decision.ACCEPTED,
        )
        
        with self.assertRaises(PermissionDenied):
            access_request1.accept(permission_user=self.user_student)

        with self.assertRaises(PermissionDenied):
            access_request2.save(permission_user=self.user_student)
        
        # Now add permission and retry
        self.role_student.permissions.set([
            permission_for_perm_string("openbook_auth.add_roleassignment"),
        ])

        access_request3 = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)
        access_request3.accept(permission_user=self.user_student)

        access_request4 = AccessRequest.from_obj(self.course,
            user     = self.user_new,
            role     = self.role_student,
            decision = AccessRequest.Decision.ACCEPTED,
        )

        access_request4.save(permission_user=self.user_student)

    def test_deny_permission(self):
        """
        User's role must include "openbook_auth.delete_roleassignment" permission to deny access requests.
        """
        # First try without permission
        access_request1 = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)        

        access_request2 = AccessRequest.from_obj(self.course,
            user     = self.user_new,
            role     = self.role_student,
            decision = AccessRequest.Decision.DENIED,
        )

        with self.assertRaises(PermissionDenied):
            access_request1.deny(permission_user=self.user_student)


        with self.assertRaises(PermissionDenied):
            access_request2.save(permission_user=self.user_student)
        
        # Now add permission and retry
        self.role_student.permissions.set([
            permission_for_perm_string("openbook_auth.delete_roleassignment"),
        ])

        access_request3 = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)
        access_request3.deny(permission_user=self.user_student)

        access_request4 = AccessRequest.from_obj(self.course,
            user     = self.user_new,
            role     = self.role_student,
            decision = AccessRequest.Decision.DENIED,
        )

        access_request4.save(permission_user=self.user_student)

class AccessRequest_ViewSet_Tests(AccessRequest_Test_Mixin, TestCase):
    """
    Tests for the `AccessRequestViewSet` REST API.
    """
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.list_url = reverse("access_request-list")

        self.access_request = AccessRequest.from_obj(self.course, user=self.user_new, role=self.role_student)
        self.access_request.save(check_permission=False)

        self.detail_url = reverse("access_request-detail", args=[str(self.access_request.pk)])

    def test_list(self):
        """
        List should return access requests for authenticated user with permission.
        """
        self.client.login(username="assistant", password="password")
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_list_requires_auth(self):
        """
        List should require authentication.
        """
        self.client.logout()
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 403)

    def test_retrieve(self):
        """
        Retrieve should return access request details for permitted user.
        """
        self.client.login(username="assistant", password="password")
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.access_request.pk))

    def test_retrieve_requires_permission(self):
        """
        Retrieve requires authenticated user with correct permission.
        """
        # Not logged in
        reset_current_user()
        self.client.logout()

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 403)

        # Logged in as dummy (lacks permission)
        reset_current_user()
        self.client.login(username="dummy", password="password")

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 404)
        self.client.logout()

        # Logged in as assistant (has permission)
        reset_current_user()
        self.client.login(username="assistant", password="password")

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_404_for_nonexistent(self):
        """
        Retrieve should return 404 for non-existent access request.
        """
        self.client.login(username="assistant", password="password")
        url = reverse("access_request-detail", args=["00000000-0000-0000-0000-000000000000"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_create(self):
        """
        Create should allow authenticated user to create access request.
        """
        self.client.login(username="new", password="password")

        response = self.client.post(self.list_url, {
            "scope_type":    model_string_for_content_type(self.role_student.scope_type),
            "scope_uuid":    str(self.role_student.scope_uuid),
            "role_slug":     self.role_student.slug,
            "user_username": self.user_new.username,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"]["username"], self.user_new.username)
        self.assertEqual(response.data["role"]["id"], str(self.role_student.pk))

    def test_create_requires_auth(self):
        """
        Create should require authentication.
        """
        self.client.logout()

        response = self.client.post(self.list_url, {
            "scope_type":    model_string_for_content_type(self.role_student.scope_type),
            "scope_uuid":    str(self.role_student.scope_uuid),
            "role_slug":     self.role_student.slug,
            "user_username": self.user_new.username,
        })

        self.assertEqual(response.status_code, 403)

    def test_update(self):
        """
        Update should allow permitted user to update access request.
        """
        self.client.login(username="assistant", password="password")

        response = self.client.put(self.detail_url, {
            "scope_type":    model_string_for_content_type(self.role_student.scope_type),
            "scope_uuid":    str(self.role_student.scope_uuid),
            "role_slug":     self.role_student.slug,
            "user_username": self.user_new.username,
            "decision":      AccessRequest.Decision.ACCEPTED,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["decision"], AccessRequest.Decision.ACCEPTED)

    def test_partial_update(self):
        """
        Partial update should allow permitted user to update access request.
        """
        self.client.login(username="assistant", password="password")

        response = self.client.patch(self.detail_url, {
            "decision": AccessRequest.Decision.DENIED
        }, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["decision"], AccessRequest.Decision.DENIED)

    def test_delete(self):
        """
        Delete should allow permitted user to delete access request.
        """
        self.client.login(username="new", password="password")
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(AccessRequest.objects.filter(pk=self.access_request.pk).exists())

    def test_permission_denied(self):
        """
        Operations without required permissions should return 403.
        """
        self.client.login(username="student", password="password")

        # Try to accept without permission
        url = reverse("access_request-accept", args=[str(self.access_request.pk)])
        response = self.client.put(url)
        self.assertEqual(response.status_code, 403)

        # Try to deny without permission
        url = reverse("access_request-deny", args=[str(self.access_request.pk)])
        response = self.client.put(url)
        self.assertEqual(response.status_code, 403)

    def test_accept(self):
        """
        Accept should assign role when permitted.
        """
        self.client.login(username="assistant", password="password")

        url = reverse("access_request-accept", args=[str(self.access_request.pk)])
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)

        self.access_request.refresh_from_db()
        self.assertEqual(self.access_request.decision, AccessRequest.Decision.ACCEPTED)

    def test_deny(self):
        """
        Deny should unassign role when permitted.
        """
        self.client.login(username="assistant", password="password")

        url = reverse("access_request-deny", args=[str(self.access_request.pk)])
        response = self.client.put(url)

        self.assertEqual(response.status_code, 200)
        self.access_request.refresh_from_db()
        self.assertEqual(self.access_request.decision, AccessRequest.Decision.DENIED)

    def test_search_and_sort(self):
        """
        List should support search and sort query parameters.
        """
        self.client.login(username="assistant", password="password")
        response = self.client.get(self.list_url + f"?_search={self.user_new.username}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_new.username, str(response.data))

        response = self.client.get(self.list_url + "?_sort=decision")
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        """
        List should support pagination query parameters.
        """
        self.client.login(username="assistant", password="password")

        response = self.client.get(self.list_url + "?_page=1&_page_size=1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)