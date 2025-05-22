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
from rest_framework.serializers                import SerializerMethodField
from rest_framework.serializers                import ValidationError

from openbook.drf                              import ModelSerializer
from openbook.auth.filters.mixins.audit        import CreatedModifiedByFilterMixin
from openbook.auth.serializers.mixins.audit    import CreatedModifiedBySerializerMixin
from openbook.core.filters.mixins.active       import ActiveInactiveFilterMixin
from openbook.core.filters.mixins.datetime     import ValidityTimeSpanFilterMixin
from openbook.core.serializers.mixins.active   import ActiveInactiveSerializerMixin
from openbook.core.serializers.mixins.datetime import ValidityTimeSpanSerializerMixin
from openbook.core.serializers.mixins.uuid     import UUIDSerializerMixin
from ..models.role_assignment                  import RoleAssignment

# TODO: Correct fields
class RoleAssignmentReadSerializer(
    UUIDSerializerMixin,
    ActiveInactiveSerializerMixin,
):
    """
    Very short overview of only the very most important role assignment fields to be
    embedded in parent models.
    """
    class Meta:
        model = RoleAssignment
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *ActiveInactiveSerializerMixin.Meta.fields,
        )
        read_only_fields = fields

@extend_schema_field(RoleAssignmentReadSerializer)
class RoleAssignmentReadField(Field):
    """
    Serializer field for reading a role assignment.
    """
    def to_internal_value(self, data):
        raise RuntimeError("RoleAssignmentReadField to write data. Use RoleAssignmentWriteField, instead.")

    def to_representation(self, obj):
        return RoleAssignmentReadSerializer(obj).data

@extend_schema_field(ListSerializer(child=RoleAssignmentReadSerializer()))
class RoleAssignmentListReadField(ListField):
    """
    Serializer field for reading multiple role assignments.
    """
    def __init__(self, **kwargs):
        self.child = RoleAssignmentReadField()
        super().__init__(**kwargs)

    def to_representation(self, value):
        return [self.child.to_representation(item) for item in value.all()]
