# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions        import ValidationError
from django.db.utils               import IntegrityError
from django.test                   import TestCase
from django.urls                   import reverse
from rest_framework.test           import APIClient

from openbook.course.models.course import Course
from ..middleware.current_user     import reset_current_user
from ..models.role                 import Role
from ..models.role_assignment      import RoleAssignment
from ..models.user                 import User

class RoleAssignment_Test_Mixin:
    def setUp(self):
        reset_current_user()

        self.user   = User.objects.create_user(username="test-new", email="test-new@example.com", password="password")
        self.course = Course.objects.create(name="Test Course", slug="test-course", text_format=Course.TextFormatChoices.MARKDOWN)
        self.role   = Role.from_obj(self.course, name="Student", slug="student", priority=0)
        self.role.save()

class RoleAssignment_Model_Tests(RoleAssignment_Test_Mixin):
    """
    Tests for the `RoleAssignment` model.

    NOTE: Methods `enroll()` and `withdraw()` require are enrollment method or access request
    as first parameter. They are therefor already tested in the unit tests for these models.
    """
    def test_role_scope(self):
        """
        The assigned role must belong to the same scope.
        """
        wrong_scope = Course.objects.create(name="Other Course", slug="other-course", text_format=Course.TextFormatChoices.MARKDOWN)
        wrong_role  = Role.from_obj(wrong_scope, name="Wrong Scope", slug="wrong-scope", priority=0)
        wrong_role.save()

        role_assignment = RoleAssignment.from_obj(self.course,
            user              = self.user,
            role              = wrong_role,
            assignment_method = RoleAssignment.AssignmentMethod.MANUAL
        )

        with self.assertRaises(ValidationError):
            role_assignment.clean()

    def test_cannot_assign_twice(self):
        """
        The same role cannot be applied to the same user twice.
        """
        RoleAssignment.from_obj(self.course,
            user              = self.user,
            role              = self.role,
            assignment_method = RoleAssignment.AssignmentMethod.MANUAL
        ).save()

        with self.assertRaises(IntegrityError):
            RoleAssignment.from_obj(self.course,
                user              = self.user,
                role              = self.role,
                assignment_method = RoleAssignment.AssignmentMethod.MANUAL
            ).save()

class RoleAssignment_ViewSet_Tests(RoleAssignment_Test_Mixin):
    """
    Tests for the `RoleAssignmentViewSet` REST API.
    """
    pass