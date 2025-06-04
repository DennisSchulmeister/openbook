# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_flex_fields         import FlexFieldsModelSerializer
from ..models.role_assignment import RoleAssignment

class RoleAssignmentSerializer(FlexFieldsModelSerializer):
    __doc__ = "Role Assignment"

    class Meta:
        model = RoleAssignment

        fields = (
            "id", "scope_type", "scope_uuid",
            "role", "user", "assignment_method",
            "is_active",
        )

        read_only_fields = ("id",)

        expandable_fields = {
            "user": "openbook.auth.serializers.user.UserSerializer",
            "role": "openbook.auth.serializers.role.RoleSerializer",
        }
