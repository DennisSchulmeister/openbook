# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation   import gettext_lazy as _
from django_filters.filterset   import FilterSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets    import ModelViewSet

from openbook.drf               import ModelViewSetMixin
from openbook.drf               import ModelSerializer

from ..filters.permission       import PermissionFilterMixin
from ..models.role              import Role
from ..serializers.permission   import PermissionSerializer

class RoleListSerializer(ModelSerializer):
    """
    Reduced list of fields for filtering a list of roles.
    """
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

class RoleRetrieveSerializer(ModelSerializer):
    """
    Full list of fields for retrieving a single role.
    """
    permissions = PermissionSerializer()

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


class RoleWriteSerializer(ModelSerializer):
    """
    Reduced list of fields for creating and updating a role.
    """
    writable_non_pk_m2m_fields = ["permissions"]

    permissions = PermissionSerializer(many=True)

    class Meta:
        model  = Role
        fields = (
            "scope_type", "scope_uuid",
            "slug",
            "name", "description", "text_format",
            "priority", "is_active",
            "permissions",
        )
    
    def to_representation(self, instance):
        return RoleRetrieveSerializer(instance=instance, context=self.context).data

class RoleFilter(PermissionFilterMixin, FilterSet):
    class Meta:
        model  = Role
        fields = RoleListSerializer.Meta.fields

class RoleViewSet(ModelViewSetMixin, ModelViewSet):
    """
    Authenticated users only as we don't want the world to scrap our role list.
    """
    __doc__ = _("User Roles Within a Scope")

    queryset           = Role.objects.all()
    permission_classes = (IsAuthenticated, *ModelViewSetMixin.permission_classes)
    filterset_class    = RoleFilter
    search_fields      = ("slug", "name", "description")

    serializer_classes = {
        "list":           RoleListSerializer,
        "retrieve":       RoleRetrieveSerializer,
        "create":         RoleWriteSerializer,
        "update":         RoleWriteSerializer,
        "partial_update": RoleWriteSerializer,
        "metadata":       RoleWriteSerializer,
        "_default":       RoleListSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return self.serializer_classes["_default"]
    
