# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models         import Permission
from django.utils.translation           import gettext_lazy as _
from import_export                      import fields

from openbook.admin                     import CustomModelAdmin
from openbook.admin                     import ImportExportModelResource
from openbook.core.models.language      import Language
from ..models.permission                import Permission_T

class PermissionTextResource(ImportExportModelResource):
    id        = fields.Field(attribute="id", column_name="id")
    delete    = fields.Field(column_name="delete")
    parent    = fields.Field(attribute="parent")
    language  = fields.Field(attribute="language", column_name="language")
    name      = fields.Field(attribute="name", column_name="name")

    class Meta:
        model  = Permission_T
        fields = ("id", "delete", "parent", "language", "name")
        use_natural_foreign_keys = True

    def dehydrate_delete(self, obj):
        return False
    
    def dehydrate_parent(self, obj):
        return f"{obj.parent.content_type.app_label} {obj.parent.content_type.model} {obj.parent.codename}"
    
    def before_import_row(self, row, **kwargs):
        parent   = row.get("parent")
        language = row.get("language")

        try:
            app_label, model, codename = parent.split(" ")
            row["parent"] = Permission.objects.get_by_natural_key(codename, app_label, model)
        except Permission.DoesNotExist:
            row["parent"] = None
            
        try:
            row["language"] = Language.objects.get(pk=language)
        except Language.DoesNotExist:
            row["language"] = None

class PermissionTextAdmin(CustomModelAdmin):
    model              = Permission_T
    resource_classes   = (PermissionTextResource,)
    list_display       = ("appname", "codename", "perm", "language", "name")
    list_display_links = ("appname", "codename", "perm", "language")
    list_editable      = ("name",)
    search_fields      = ("appname", "codename", "perm", "language", "name")
    readonly_fields    = ("appname", "codename", "perm")

    fieldsets = (
        (None, {
            "fields": ("perm", ("appname", "codename"), ("language", "name"))
        }),
    )

    add_fieldsets = (
        (None, {
            "fields": ("parent", ("language", "name"))
        }),
    )