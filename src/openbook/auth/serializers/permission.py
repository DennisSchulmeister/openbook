# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models import Permission
from django.utils.translation   import gettext_lazy as _
from drf_spectacular.utils      import extend_schema_field
from rest_framework.serializers import Serializer
from rest_framework.serializers import RelatedField
from rest_framework.serializers import CharField

from ..utils                    import app_label_for_permission
from ..utils                    import app_name_for_permission
from ..utils                    import model_for_permission
from ..utils                    import model_name_for_permission
from ..utils                    import perm_name_for_permission
from ..utils                    import perm_string_for_permission
from ..utils                    import permission_for_perm_string

class PermissionReadSerializer(Serializer):
    """
    Serializer for reading permission objects. Returns a custom object structure.
    """
    __doc__ = "Permission"

    perm_string        = CharField()
    perm_display_name  = CharField()
    app                = CharField()
    app_display_name   = CharField()
    model              = CharField()
    model_display_name = CharField()
    codename           = CharField()

    class Meta:
        fields   = ("perm_string", "perm_display_name", "app", "app_display_name", "model", "model_display_name", "codename")
        read_only_fields = fields

    def to_representation(self, obj):
        return {
            "perm_string":        perm_string_for_permission(obj),
            "perm_display_name":  perm_name_for_permission(obj),
            "app":                app_label_for_permission(obj),
            "app_display_name":   app_name_for_permission(obj),
            "model":              model_for_permission(obj),
            "model_display_name": model_name_for_permission(obj),
            "codename":           obj.codename,
        }

@extend_schema_field({
    "type":        "string",
    "description": "Permission string",
    "example":     "app.model_codename"
})
class PermissionWriteField(RelatedField):
    """
    Serializer field for writing permissions. Use this to accept a permission string
    in the request that will be looked up in the database.
    """
    default_error_messages = {
        "not_found": _("Permission '{value}' not found."),
        "invalid":   _("Invalid format: Expected a permission string."),
        "required":  _("Permission string is required."),
    }

    queryset = Permission.objects.all()

    def to_internal_value(self, data):
        if data is None:
            if self.required:
                self.fail("required")
            else:
                return None
            
        if not isinstance(data, str):
            self.fail("invalid")

        try:
            return permission_for_perm_string(data)
        except Permission.DoesNotExist:
            self.fail("not_found", value=data)
    
    def to_representation(self, obj):
        raise RuntimeError("PermissionWriteField used to deserialize data. Use PermissionReadSerializer, instead.")

