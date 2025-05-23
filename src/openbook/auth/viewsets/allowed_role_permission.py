# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from drf_spectacular.utils                   import extend_schema
from rest_framework.viewsets                 import ModelViewSet

from openbook.drf                            import ModelViewSetMixin
from openbook.core.serializers.mixins.uuid   import UUIDSerializerMixin
from ..filters.mixins.scope                  import ScopeTypeFilterMixin
from ..filters.mixins.permission             import PermissionFilterMixin
from ..models.allowed_role_permission        import AllowedRolePermission
from ..serializers.mixins.scope              import ScopeTypeField
from ..serializers.permission                import PermissionReadField
from ..serializers.permission                import PermissionWriteField
from ..models.allowed_role_permission        import AllowedRolePermission

class AllowedRolePermissionSerializer(UUIDSerializerMixin):
    scope_type        = ScopeTypeField()
    permission        = PermissionReadField(read_only=True)
    permission_string = PermissionWriteField(write_only=True, source="permission")

    class Meta:
        model = AllowedRolePermission
        fields = (*UUIDSerializerMixin.Meta.fields, "scope_type", "permission", "permission_string")

class AllowedRolePermissionFilter(ScopeTypeFilterMixin, PermissionFilterMixin):
    class Meta:
        model  = AllowedRolePermission
        fields = {**ScopeTypeFilterMixin.Meta.fields, **PermissionFilterMixin.Meta.fields}
        permissions_field = "permission"

@extend_schema(
    extensions={
        "x-app-name":   "User Management",
        "x-model-name": "Allowed Role Permissions",
    }
)
class AllowedRolePermissionViewSet(ModelViewSetMixin, ModelViewSet):
    __doc__ = "Allowed permissions for the roles of a given scope type"

    queryset         = AllowedRolePermission.objects.all()
    serializer_class = AllowedRolePermissionSerializer
    filterset_class  = AllowedRolePermissionFilter
    search_fields    = (
        "scope_type__app_label", "scope_type__model",
        "permission__codename", "permission__content_type__app_label",
    )
