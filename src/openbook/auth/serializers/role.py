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
from openbook.core.serializers.mixins.slug     import SlugSerializerMixin
from openbook.core.serializers.mixins.text     import NameDescriptionListSerializerMixin
from openbook.core.serializers.mixins.uuid     import UUIDSerializerMixin
from ..models.role                             import Role

class RoleReadSerializer(
    UUIDSerializerMixin,
    SlugSerializerMixin,
    NameDescriptionListSerializerMixin,
    ActiveInactiveSerializerMixin,
):
    """
    Very short overview of only the very most important role fields to be embedded
    in parent models.
    """
    class Meta:
        model = Role
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *SlugSerializerMixin.Meta.fields,
            *NameDescriptionListSerializerMixin.Meta.fields,
            "priority",
            *ActiveInactiveSerializerMixin.Meta.fields,
        )
        read_only_fields = fields

@extend_schema_field(RoleReadSerializer)
class RoleReadField(Field):
    """
    Serializer field for reading a role.
    """
    def to_internal_value(self, data):
        raise RuntimeError("RoleReadField to write data. Use RoleWriteField, instead.")

    def to_representation(self, obj):
        return RoleReadSerializer(obj).data

