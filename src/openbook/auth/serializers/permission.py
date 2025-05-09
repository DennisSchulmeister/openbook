# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#from django.contrib.auth.models import Permission

from django.contrib.auth.models import Permission
from django.core.exceptions     import ValidationError
from django.utils.translation   import gettext_lazy as _
from rest_framework.serializers import CharField
from rest_framework.serializers import SerializerMethodField

from openbook.drf               import ModelSerializer

class PermissionSerializer(ModelSerializer):
    """
    Custom serializer for nested permission objects. Resolved all foreign keys so
    that the actual app label, model name and full permission string are included.
    """
    __doc__ = _("Permissions")

    perm       = SerializerMethodField()    # For reading
    app_label  = CharField(source="content_type.app_label", read_only=True)
    model_name = CharField(source="content_type.model", read_only=True)
    
    class Meta:
        model  = Permission
        fields = ["perm", "app_label", "model_name", "codename", "name"]
    
    def get_perm(self, obj):
        """
        Permission string
        """
        ct = obj.content_type
        return f"{ct.app_label}.{ct.model}_{obj.codename}"

    def to_internal_value(self, data):
        """
        Accepts either a permission string (e.g. "app.model_codename")
        or a full dict with perm field.
        """
        if not isinstance(data, str):
            raise ValidationError("Invalid format: expected a permission string.")
        
        try:
            app_label, rest = data.split(".", 1)
            model_name, codename = rest.split("_", 1)
        except ValueError:
            raise ValidationError("Permission string must be in the format 'app.model_codename'")
        
        try:
            permission = Permission.objects.select_related("content_type").get(
                content_type__app_label=app_label,
                content_type__model=model_name,
                codename=codename,
            )

            return permission
        except Permission.DoesNotExist:
            raise ValidationError(f"Permission '{data}' not found.")