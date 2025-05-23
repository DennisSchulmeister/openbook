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
from ..models.access_request                   import AccessRequest
from .role                                     import RoleReadField
from .user                                     import UserReadField

class AccessRequestWithoutRoleReadSerializer(UUIDSerializerMixin):
    """
    Very short overview of only the very most important access request fields to be
    embedded in parent models (without role because it is identical with the parent).
    """
    user = UserReadField(read_only=True)

    class Meta:
        model = AccessRequest
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            "user", "role", "decision", "decision_date", "created_at",
        )
        read_only_fields = fields

class AccessRequestWithRoleReadSerializer(UUIDSerializerMixin):
    """
    Very short overview of only the very most important access request fields to be
    embedded in parent models (including role).
    """
    user = UserReadField(read_only=True)
    role = RoleReadField(read_only=True)

    class Meta:
        model = AccessRequest
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            "user", "role", "decision", "decision_date", "created_at",
        )
        read_only_fields = fields

@extend_schema_field(AccessRequestWithoutRoleReadSerializer)
class AccessRequestWithoutRoleReadField(Field):
    """
    Serializer field for reading an access request (without role).
    """
    def to_internal_value(self, data):
        raise RuntimeError("AccessRequestWithoutRoleReadField to write data, which is not supported.")

    def to_representation(self, obj):
        return AccessRequestWithoutRoleReadSerializer(obj).data
    
@extend_schema_field(AccessRequestWithRoleReadSerializer)
class AccessRequestWithRoleReadField(Field):
    """
    Serializer field for reading an access request (with role).
    """
    def to_internal_value(self, data):
        raise RuntimeError("AccessRequestWithRoleReadField to write data, which is not supported.")

    def to_representation(self, obj):
        return AccessRequestWithRoleReadSerializer(obj).data
