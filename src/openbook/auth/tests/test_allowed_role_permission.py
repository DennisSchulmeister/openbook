# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions             import ValidationError
from django.test                        import TestCase

from ..models.allowed_role_permission   import AllowedRolePermission
from ..utils                            import permission_for_perm_string
from ..validators                       import validate_permissions
from ..utils                            import content_type_for_model_string

class AllowedRolePermissionTests(TestCase):
    """
    Tests for the `AllowedRolePermission` model.
    """
    def setUp(self):
        self.scope_type = content_type_for_model_string("openbook_course.course")

        AllowedRolePermission.objects.create(
            scope_type = self.scope_type,
            permission = permission_for_perm_string("admin.add_logentry"),
        )

        AllowedRolePermission.objects.create(
            scope_type = self.scope_type,
            permission = permission_for_perm_string("admin.view_logentry"),
        )

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
    