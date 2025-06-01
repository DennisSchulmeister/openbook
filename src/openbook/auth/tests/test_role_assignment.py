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

from openbook.course.models.course import Course
from openbook.test                 import ModelViewSetTestMixin
from ..middleware.current_user     import reset_current_user
from ..models.role                 import Role
from ..models.role_assignment      import RoleAssignment
from ..models.user                 import User
from ..utils                       import model_string_for_content_type

class RoleAssignment_Test_Mixin:
    def setUp(self):
        super().setUp()

        self.user            = User.objects.create_user(username="test-new", email="test-new@example.com", password="password")
        self.course          = Course.objects.create(name="Test Course", slug="test-course")
        self.role_student    = Role.from_obj(self.course, name="Student", slug="student", priority=0)
        self.role_assistant  = Role.from_obj(self.course, name="Assistant", slug="assistant", priority=1)
        self.role_teacher    = Role.from_obj(self.course, name="Teacher", slug="teacher", priority=2)

        self.role_student.save()
        self.role_assistant.save()
        self.role_teacher.save()

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

        role_assignment = RoleAssignment.from_obj(self.course, user=self.user, role=wrong_role)

        with self.assertRaises(ValidationError):
            role_assignment.clean()

    def test_cannot_assign_twice(self):
        """
        The same role cannot be applied to the same user twice.
        """
        RoleAssignment.from_obj(self.course, user=self.user, role=self.role_student).save()

        with self.assertRaises(IntegrityError):
            RoleAssignment.from_obj(self.course, user=self.user, role=self.role_student).save()

class RoleAssignment_ViewSet_Tests(ModelViewSetTestMixin, RoleAssignment_Test_Mixin, TestCase):
    """
    Tests for the `RoleAssignmentViewSet` REST API.
    """
    base_name     = "role_assignment"
    model         = RoleAssignment
    search_string = "test-new"
    search_count  = 2
    sort_field    = "user__username"

    def setUp(self):
        super().setUp()

        self.ra_student = RoleAssignment.from_obj(self.course, role=self.role_student, user=self.user)
        self.ra_student.save()

        self.ra_assistant = RoleAssignment.from_obj(self.course, role=self.role_assistant, user=self.user)
        self.ra_assistant.save()
    
    def pk_found(self):
        return self.ra_student.id
    
    def get_create_request_data(self):
        return {
            "scope_type":    model_string_for_content_type(self.ra_student.scope_type),
            "scope_uuid":    str(self.ra_student.scope_uuid),
            "role_slug":     "teacher",
            "user_username": "test-new",
        }

    def get_update_request_data(self):
        return {
                "scope_type":    model_string_for_content_type(self.ra_student.scope_type),
                "scope_uuid":    str(self.ra_student.scope_uuid),
                "role_slug":     "teacher",
                "user_username": "test-new",
                "is_active":     False,
                "start_date":    "",
                "end_date":      "",
            }

    operations = {
        "create": {
            "request_data": get_create_request_data,
        },
        "update": {
            "request_data": get_update_request_data,
            "updates": {
                "role":       {"slug": "teacher"},
                "user":       {"username": "test-new"},
                "is_active":  False,
                "start_date": None,
                "end_date":   None,
            }
        },
        "partial_update": {
            "request_data": {"is_active": False},
            "updates":      {"is_active": False},
        },
    }