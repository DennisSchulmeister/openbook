# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_flex_fields import FlexFieldsModelSerializer
from ..models.role    import Role

class RoleSerializer(FlexFieldsModelSerializer):
    __doc__ = "Role"

    class Meta:
        model = Role

        fields = (
            "id", "scope_type", "scope_uuid", "slug",
            "name", "description", "text_format",
            "priority", "permissions",
            "is_active",
            "created_by", "created_at", "modified_by", "modified_at",
        )

        read_only_fields = (
            "id",
            "created_by", "created_at", "modified_by", "modified_at",
        )

        expandable_fields = {
            "permissions": ("openbook.auth.serializers.permission.PermissionSerializer", {"many": True}),
        }
