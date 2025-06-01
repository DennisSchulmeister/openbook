# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation                  import gettext_lazy as _
from drf_spectacular.utils                     import extend_schema_field
from rest_framework.serializers                import Field
from rest_framework.serializers                import ListField
from rest_framework.serializers                import ListSerializer

from openbook.core.serializers.mixins.active   import ActiveInactiveSerializerMixin
from openbook.core.serializers.mixins.uuid     import UUIDSerializerMixin
from .role                                     import RoleReadField
from .user                                     import UserReadField
from ..models.role_assignment                  import RoleAssignment

class RoleAssignmentReadSerializer(
    UUIDSerializerMixin,
    ActiveInactiveSerializerMixin,
):
    """
    Very short overview of only the very most important role assignment fields to be
    embedded in parent models.
    """
    role = RoleReadField(read_only=True)
    user = UserReadField(read_only=True)

    class Meta:
        model = RoleAssignment
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            "role", "user", "assignment_method",
            *ActiveInactiveSerializerMixin.Meta.fields,
        )
        read_only_fields = fields
