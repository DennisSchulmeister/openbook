# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.admin               import RelatedOnlyFieldListFilter
from django.contrib.auth                import get_user_model
from django.contrib.auth.models         import Permission
from django.utils.translation           import gettext_lazy as _
from import_export.fields               import Field

from openbook.admin                     import ImportExportModelResource
from openbook.auth.utils                import perm_string_for_permission
from openbook.auth.utils                import permission_for_perm_string

scope_type_filter = ("scope_type", RelatedOnlyFieldListFilter)

permissions_fieldset = (_("Permissions"), {
    "classes": ("tab",),
    "fields": ("owner", "public_permissions"),
})

class ScopedRolesResourceMixin(ImportExportModelResource):
    """
    Mixin class for the import/export resource class of models that act as permissions
    scopes for user roles. Handles the import and export of the owner and public permissions.
    Note that the other scope fields (roles, enrollment methods, …) are not handled, because
    they are reverse relations for objects that support import/export themselves.
    """
    public_permissions = Field(column_name="")

    class Meta:
        fields = ("owner", "public_permissions")

    def dehydrate_owner(self, obj):
        """
        Export username instead of numeric PK for owner.
        """
        return obj.owner.username if obj.owner else ""

    def dehydrate_public_permissions(self, obj):
        """
        Export public permissions as white-space separated list of permission strings.
        """
        if not obj.public_permissions:
            return ""

        return " ".join([perm_string_for_permission(permission) for permission in obj.public_permissions.all()])

    def before_import_row(self, row, **kwargs):
        """
        Resolve owner and public permissions before import.
        """
        # Parse public permissions
        public_permissions = row.get("public_permissions") or ""
        row._parsed_permissions = []

        for public_permission in public_permissions.split():
            try:
                permission = permission_for_perm_string(public_permission)
                row._parsed_permissions.append(permission)
            except Permission.DoesNotExist:
                continue
        
        # Resolve owner
        owner = row.get("owner") or ""
        row["owner"] = None

        try:
            if owner:
                User = get_user_model()
                row["owner"] = User.objects.get(username=owner).pk
        except User.DoesNotExist:
            pass

    def after_save_instance(self, instance, row, **kwargs):
        """
        M2M relations can only be saved when the model instance already exists on the database.
        Therefor we cannot simply assign a list of objects to the M2M field in `before_import_row()`,
        as Django refuses direct assignments to M2M properties.
        """
        # Set public permissions M2M now that the row has been saved
        if hasattr(row, "_parsed_permissions"):
            instance.public_permissions.set(row._parsed_permissions)
