# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_flex_fields import FlexFieldsModelSerializer
from .                import models

class AllowedRolePermissionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model  = models.AllowedRolePermission
        fields = ("id", "scope_type", "permission")
        expandable_fields = {"permission": "openbook.auth.serializers.permission.PermissionSerializer"}