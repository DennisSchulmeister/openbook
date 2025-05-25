# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db.utils               import IntegrityError
from django.test                   import TestCase

from openbook.course.models.course import Course
from ..models.role                 import Role
from ..models.role_assignment      import RoleAssignment
from ..models.user                 import User

class RoleAssignmentTests(TestCase):
    """
    Tests for the `RoleAssignment` model.

    NOTE: Methods `enroll()` and `withdraw()` require are enrollment method or access request
    as first parameter. They are therefor already tested in the unit tests for these models.
    """
    def setUp(self):
        self.user   = User.objects.create_user(username="test-new", email="test-new@example.com", password="password")
        self.course = Course.objects.create(name="Test Course", slug="test-course", text_format=Course.TextFormatChoices.MARKDOWN)
        self.role   = Role.from_obj(self.course, name="Student", slug="student", priority=0)
        self.role.save()

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