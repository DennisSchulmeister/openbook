# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models import Permission
from django.utils.translation   import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets    import ModelViewSet

from ...drf                     import ModelViewSetMixin, ModelSerializer, ListSerializer
from ...models.role             import Role

# TODO: Use app_label, codename to add permissions when creating new roles
# TODO: Remove created_by, modified_by from create, update, partial_update
class PermissionSerializer(ModelSerializer):
    """
    Included permissions
    """
    class Meta:
        model  = Permission
        fields = ["name", "content_type", "codename"]
        # TODO: Show app_label instead of content_type FK (how??)

# TODO: …list-operation shows not just these fields in OpenAPI??
class RoleListSerializer(ListSerializer):
    class Meta:
        model = Role
        fields = [
            "id",
            "scope_type", "scope_uuid",
            "slug",
            "name",
            "priority", "is_active",
            "created_by", "created_at", "modified_by", "modified_at",
        ]

class RoleSerializer(ModelSerializer):
    permissions = PermissionSerializer()

    class Meta:
        model  = Role
        fields = [
            "id",
            "scope_type", "scope_uuid",
            "slug",
            "name", "description", "text_format",
            "is_active",
            "priority", "permissions",
            "created_by", "created_at", "modified_by", "modified_at",
        ]
        list_serializer_class = RoleListSerializer

class RoleViewSet(ModelViewSetMixin, ModelViewSet):
    """
    Authenticated users only as we don't want the world to scrap our role list.
    """
    __doc__ = _("User Roles Within a Scope")

    queryset           = Role.objects.all()
    serializer_class   = RoleSerializer
    permission_classes = [IsAuthenticated, *ModelViewSetMixin.permission_classes]
    filterset_fields   = RoleListSerializer.Meta.fields
    search_fields      = ["slug", "name", "description"]