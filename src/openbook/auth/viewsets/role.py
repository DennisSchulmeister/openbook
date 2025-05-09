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
from rest_framework.serializers import CharField
from rest_framework.serializers import SerializerMethodField
from rest_framework.viewsets    import ModelViewSet

from openbook.drf               import ModelViewSetMixin
from openbook.drf               import ModelSerializer
from openbook.drf               import ListSerializer

from ..models.role              import Role

# TODO: Use app_label, codename to add permissions when creating new roles.
# TODO: Remove created_by, modified_by from create, update, partial_update.
# TODO: Move PermissionSerializer into shared code file.
# https://chatgpt.com/g/g-p-68128762bf848191860962c9aae6c388-openbook-development/c/681db450-d960-8007-afa9-c5dbbd0bc8ff
class PermissionSerializer(ModelSerializer):
    """
    Included permissions
    """
    perm       = SerializerMethodField()
    app_label  = CharField(source="content_type.app_label", read_only=True)
    model_name = CharField(source="content_type.model", read_only=True)

    def get_perm(self, obj):
        ct = obj.content_type
        return f"{ct.app_label}.{ct.model}_{obj.codename}"
    
    class Meta:
        model  = Permission
        fields = ["perm", "app_label", "model_name", "codename", "name"]

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