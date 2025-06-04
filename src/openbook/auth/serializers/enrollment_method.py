# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_flex_fields           import FlexFieldsModelSerializer
from ..models.enrollment_method import EnrollmentMethod

class EnrollmentMethodSerializer(FlexFieldsModelSerializer):
    __doc__ = "Enrollment Method"

    class Meta:
        model = EnrollmentMethod

        fields = (
            "id", "scope_type", "scope_uuid",
            "name", "description", "text_format",
            "role",
            "is_active",
        )

        read_only_fields = ("id",)

        expandable_fields = {
            "role": "openbook.auth.serializers.role.RoleSerializer",
        }
