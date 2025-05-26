# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions        import ValidationError
from django.test                   import TestCase
from unittest.mock                 import patch

from openbook.course.models.course import Course
from ..middleware.current_user     import reset_current_user
from ..models.enrollment_method    import EnrollmentMethod
from ..models.role                 import Role
from ..models.role_assignment      import RoleAssignment
from ..models.user                 import User

class EnrollmentMethod_Test_Mixin:
    def setUp(self):
        reset_current_user()

        self.user = User.objects.create_user(username="new", email="new@test.com", password="password")
        self.owner = User.objects.create_user(username="owner", email="owner@test.com", password="password")
        self.course = Course.objects.create(name="Test Course", slug="test-course", text_format=Course.TextFormatChoices.MARKDOWN, owner=self.owner)

        self.role = Role.from_obj(self.course, name="Student", slug="student", priority=0)
        self.role.save()

        self.em_passphrase = EnrollmentMethod.from_obj(self.course, name="self-enrollment", role=self.role, passphrase="Correct!")
        self.em_passphrase.save()

        self.em_no_passphrase = EnrollmentMethod.from_obj(self.course, name="self-enrollment", role=self.role)
        self.em_no_passphrase.save()

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
    
    def test_wrong_passphrase_value_error(self):
        """
        `ValueError` should be raised when a wrong passphrase is used.
        """
        with self.assertRaises(ValueError):
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