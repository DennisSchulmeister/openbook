# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filterset         import FilterSet
from rest_framework.permissions       import IsAuthenticated
from rest_framework.viewsets          import ModelViewSet

from openbook.drf                     import ModelViewSetMixin
from openbook.drf                     import ModelSerializer

from ..filters.mixins.permission      import PermissionFilterMixin
from ..models.role                    import Role
from ..serializers.permission         import PermissionSerializer
from ..serializers.user               import UserReadField
from ..validators                     import validate_permissions

class RoleListSerializer(ModelSerializer):
    """
    Reduced list of fields for filtering a list of roles.
    """
    created_by  = UserReadField(read_only=True)
    modified_by = UserReadField(read_only=True)

    class Meta:
        model = Role
        fields = (
            "id",
            "scope_type", "scope_uuid",
            "slug",
            "name",
            "priority", "is_active",
            "created_by", "created_at", "modified_by", "modified_at",
        )

class RoleSerializer(ModelSerializer):
    """
    Full list of fields for retrieving a single role.
    """
    permissions = PermissionSerializer()
    created_by  = UserReadField(read_only=True)
    modified_by = UserReadField(read_only=True)

    class Meta:
        model  = Role
        fields = (
            "id",
            "scope_type", "scope_uuid",
            "slug",
            "name", "description", "text_format",
            "priority", "is_active",
            "permissions",
            "created_by", "created_at", "modified_by", "modified_at",
        )

        read_only_fields = (
            "id",
            "created_at", "modified_at",
        )

    def validate(self, attributes):
        """
        Check that only allowed permissions are assigned.
        """
        scope_type  = attributes.get("scope_type", None)
        permissions = attributes.get("permissions", None)

        validate_permissions(scope_type, permissions)
        return attributes

class RoleFilter(PermissionFilterMixin, FilterSet):
    class Meta:
        model  = Role
        fields = RoleListSerializer.Meta.fields

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
