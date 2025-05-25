# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions        import PermissionDenied
from django.test                   import TestCase
from django.utils                  import timezone
from unittest.mock                 import patch

from openbook.course.models.course import Course
from ..models.access_request       import AccessRequest
from ..models.role                 import Role
from ..models.role_assignment      import RoleAssignment
from ..models.user                 import User
from ..utils                       import permission_for_perm_string

class TestAccessRequestModel(TestCase):
    """
    Tests for the `AccessRequest` model.
    """
    def setUp(self):
        self.user_new       = User.objects.create_user(username="test-new", email="test-new@example.com", password="password")
        self.user_student   = User.objects.create_user(username="test-student", email="test-student@example.com", password="password")
        self.user_assistant = User.objects.create_user(username="test-assistant", email="test-assistant@example.com", password="password")
        self.course         = Course.objects.create(name="Test Course", slug="test-course", text_format=Course.TextFormatChoices.MARKDOWN)
        self.role_student   = Role.from_obj(self.course, name="Student", slug="student", priority=0)
        self.role_assistant = Role.from_obj(self.course, name="Assistant", slug="assistant", priority=1)
        self.role_teacher   = Role.from_obj(self.course, name="Teacher", slug="teacher", priority=2)

        self.role_student.save()
        self.role_assistant.save()
        self.role_teacher.save()

        permissions = [
            permission_for_perm_string("openbook_auth.add_roleassignment"),
            permission_for_perm_string("openbook_auth.delete_roleassignment"),
        ]

        self.role_assistant.permissions.set(permissions)
        self.role_teacher.permissions.set(permissions)

        RoleAssignment.from_obj(self.course, user=self.user_student, role=self.role_student).save()
        RoleAssignment.from_obj(self.course, user=self.user_assistant, role=self.role_assistant).save()

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