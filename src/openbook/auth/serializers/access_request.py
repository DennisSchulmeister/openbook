# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_flex_fields        import FlexFieldsModelSerializer
from ..models.access_request import AccessRequest

class AccessRequestSerializer(FlexFieldsModelSerializer):
    __doc__ = "Access Request"

    class Meta:
        model = AccessRequest

        fields = (
            "id", "scope_type", "scope_uuid",
            "user", "role", "decision", "decision_date", "created_at",
        )

        read_only_fields = ("id", "decision_date", "created_at")

        expandable_fields = {
            "user": "openbook.auth.serializers.user.UserSerializer",
            "role": "openbook.auth.serializers.role.RoleSerializer",
        }
