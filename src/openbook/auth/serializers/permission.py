# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models import Permission
from drf_spectacular.utils      import extend_schema_field
from rest_flex_fields           import FlexFieldsModelSerializer
from rest_framework.serializers import SerializerMethodField

from ..models.permission        import Permission_T
from ..utils                    import app_label_for_permission
from ..utils                    import app_name_for_permission
from ..utils                    import model_for_permission
from ..utils                    import model_name_for_permission
from ..utils                    import perm_name_for_permission
from ..utils                    import perm_string_for_permission

class PermissionSerializer(FlexFieldsModelSerializer):
    __doc__ = "Permission"

    perm_string        = SerializerMethodField()
    perm_display_name  = SerializerMethodField()
    app                = SerializerMethodField()
    app_display_name   = SerializerMethodField()
    model              = SerializerMethodField()
    model_display_name = SerializerMethodField()

    class Meta:
        model = Permission

        fields = (
            "id",
            "name", "codename",
            "perm_string", "perm_display_name",
            "app", "app_display_name",
            "model", "model_display_name",
        )

        read_only_fields = ("id",)
    
    @extend_schema_field(str)
    def get_perm_string(self, obj: Permission) -> str:
        return perm_string_for_permission(obj)

    @extend_schema_field(str)
    def get_perm_display_name(self, obj: Permission) -> str:
        return perm_name_for_permission(obj)

    @extend_schema_field(str)
    def get_app(self, obj: Permission) -> str:
        return app_label_for_permission(obj)

    @extend_schema_field(str)
    def get_app_display_name(self, obj: Permission) -> str:
        return app_name_for_permission(obj)

    @extend_schema_field(str)
    def get_model(self, obj: Permission) -> str:
        return model_for_permission(obj)

    @extend_schema_field(str)
    def get_model_display_name(self, obj: Permission) -> str:
        return model_name_for_permission(obj)

class PermissionTSerializer(FlexFieldsModelSerializer):
    __doc__ = "Permission Label"

    class Meta:
        model  = Permission_T
        fields = ("id", "language", "parent", "name")
        expandable_fields = {"parent": PermissionSerializer}