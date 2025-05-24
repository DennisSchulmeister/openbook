# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.test                   import TestCase
from django.utils                  import timezone
from unittest.mock                 import patch

from openbook.course.models.course import Course
from ..models.access_request       import AccessRequest
from ..models.role                 import Role
from ..models.role_assignment      import RoleAssignment
from ..models.user                 import User

class AccessRequestSaveMethodTests(TestCase):
    """
    Tests for the save method of the AccessRequest model.
    """

    # TODO: Fix course and role creation
    def setUp(self):
        self.user           = User.objects.create_user(username="testuser", email="testuser@example.com", password="password")
        self.course         = Course.objects.create(name="Test Course", description="Test Course Description")
        self.role           = Role.objects.create(name="Test Role", verbose_name="Test Role", scope_type="COURSE", scope_uuid=self.course.uuid, slug="test-role")
        self.access_request = AccessRequest(user=self.user, course=self.course, role=self.role)

    def test_force_pending_decision_when_new_access_request_is_saved(self):
        """
        Should force the decision to be pending when a new AccessRequest is saved.
        """
        self.access_request.save()
        self.assertEqual(self.access_request.decision, AccessRequest.Decision.PENDING)

    def test_set_decision_date_to_none_when_decision_is_pending(self):
        """
        Should set the decision date to None when the decision is pending.
        """
        self.access_request.decision = AccessRequest.Decision.PENDING
        self.access_request.save()
        self.assertIsNone(self.access_request.decision_date)

    def test_set_decision_date_to_now_when_decision_is_changed(self):
        """
        Should set the decision date to the current date and time when the decision is changed.
        """
        self.access_request.save()  # Save to set pk
        old_access_request = AccessRequest.objects.get(pk=self.access_request.pk)
        old_access_request.decision = AccessRequest.Decision.PENDING
        old_access_request.save()

        self.access_request.decision = AccessRequest.Decision.ACCEPTED
        self.access_request.save()

        self.assertIsNotNone(self.access_request.decision_date)
        self.assertIsInstance(self.access_request.decision_date, timezone.datetime)

    def test_enroll_in_role_assignment_when_decision_is_accepted(self):
        """
        Should enroll the user in the role assignment when the decision is accepted.
        """
        with patch.object(RoleAssignment, "enroll") as mock_enroll:
            self.access_request.decision = AccessRequest.Decision.ACCEPTED
            self.access_request.save()
            mock_enroll.assert_called_once_with(enrollment=self.access_request)

    def test_withdraw_from_role_assignment_when_decision_is_denied(self):
        """
        Should withdraw the user from the role assignment when the decision is denied.
        """
        with patch.object(RoleAssignment, "withdraw") as mock_withdraw:
            self.access_request.decision = AccessRequest.Decision.DENIED
            self.access_request.save()
            mock_withdraw.assert_called_once_with(enrollment=self.access_request)