# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework.permissions              import IsAuthenticated
from rest_framework.serializers              import ListField
from rest_framework.viewsets                 import ModelViewSet

from openbook.drf                            import ModelViewSetMixin
from openbook.core.filters.mixins.active     import ActiveInactiveFilterMixin
from openbook.core.filters.mixins.slug       import SlugFilterMixin
from openbook.core.filters.mixins.text       import NameDescriptionFilterMixin
from openbook.core.serializers.mixins.active import ActiveInactiveSerializerMixin
from openbook.core.serializers.mixins.slug   import SlugSerializerMixin
from openbook.core.serializers.mixins.text   import NameDescriptionListSerializerMixin
from openbook.core.serializers.mixins.text   import NameDescriptionSerializerMixin
from openbook.core.serializers.mixins.uuid   import UUIDSerializerMixin

from ..filters.mixins.audit                  import CreatedModifiedByFilterMixin
from ..filters.mixins.scope                  import ScopeFilterMixin
from ..models.role                           import Role
from ..serializers.mixins.audit              import CreatedModifiedBySerializerMixin
from ..serializers.mixins.scope              import ScopeSerializerMixin
from ..serializers.permission                import PermissionReadField
from ..serializers.permission                import PermissionWriteField
from ..validators                            import validate_permissions

class RoleListSerializer(
    UUIDSerializerMixin,
    ScopeSerializerMixin,
    SlugSerializerMixin,
    NameDescriptionListSerializerMixin,
    ActiveInactiveSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Reduced list of fields for filtering a list of roles.
    """
    class Meta:
        model = Role
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *SlugSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            *NameDescriptionListSerializerMixin.Meta.fields,
            *ActiveInactiveSerializerMixin.Meta.fields,
            "priority",
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )
        read_only_fields = fields

class RoleSerializer(
    UUIDSerializerMixin,
    ScopeSerializerMixin,
    SlugSerializerMixin,
    NameDescriptionSerializerMixin,
    ActiveInactiveSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Full list of fields for retrieving a single role.
    """
    permissions        = ListField(child=PermissionReadField(), read_only=True)
    permission_strings = ListField(child=PermissionWriteField(), write_only=True, source="permissions")

    class Meta:
        model  = Role
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *SlugSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            *NameDescriptionSerializerMixin.Meta.fields,
            *ActiveInactiveSerializerMixin.Meta.fields,
            "priority", "permissions", "permission_strings",
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )

        read_only_fields = (
            *UUIDSerializerMixin.Meta.read_only_fields,
            *SlugSerializerMixin.Meta.read_only_fields,
            *ScopeSerializerMixin.Meta.read_only_fields,
            *NameDescriptionSerializerMixin.Meta.read_only_fields,
            *ActiveInactiveSerializerMixin.Meta.read_only_fields,
            *CreatedModifiedBySerializerMixin.Meta.read_only_fields,
        )

    def validate(self, attributes):
        """
        Check that only allowed permissions are assigned.
        """
        scope_type  = attributes.get("scope_type", None)
        permissions = attributes.get("permissions", None)

        validate_permissions(scope_type, permissions)
        return attributes

class RoleFilter(
    SlugFilterMixin,
    ScopeFilterMixin,
    NameDescriptionFilterMixin,
    ActiveInactiveFilterMixin,
    CreatedModifiedByFilterMixin
):
    class Meta:
        model  = Role
        fields = {
            **SlugFilterMixin.Meta.fields,
            **ScopeFilterMixin.Meta.fields,
            **NameDescriptionFilterMixin.Meta.fields,
            "priority":   ("exact", "lte", "gte"),
            **ActiveInactiveFilterMixin.Meta.fields,
            **CreatedModifiedByFilterMixin.Meta.fields,
        }

# TODO: Should access be restricted?
class RoleViewSet(ModelViewSetMixin, ModelViewSet):
    """
    Authenticated users only as we don't want the world to scrap our role list.
    """
    __doc__ = "User Roles Within a Scope"

    queryset           = Role.objects.all()
    permission_classes = (IsAuthenticated, *ModelViewSetMixin.permission_classes)
    filterset_class    = RoleFilter
    search_fields      = ("slug", "name", "description")

    def get_serializer_class(self):
        if self.action == "list":
            return RoleListSerializer
        else:
            return RoleSerializer