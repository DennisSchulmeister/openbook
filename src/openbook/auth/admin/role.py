# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation          import gettext_lazy as _
from unfold.admin                      import TabularInline

from openbook.admin                    import CustomModelAdmin
from openbook.admin                    import ImportExportModelResource
from .mixins.audit                     import created_modified_by_fields
from .mixins.audit                     import created_modified_by_fieldset
from .mixins.audit                     import created_modified_by_filter
from .mixins.auth                      import ScopeFormMixin
from .mixins.auth                      import scope_type_filter
from ..models.role                     import Role
from ..validators                      import validate_permissions

# TODO: Import/Export
class RoleResource(ImportExportModelResource):
    class Meta:
        model = Role

class RoleForm(ScopeFormMixin):
    class Meta:
        model  = Role
        fields = "__all__"
    
    class Media:
        js = ScopeFormMixin.Media.js
    
    def clean(self):
        """
        Check that only allowed permissions are assigned.
        """
        cleaned_data = super().clean()
        scope_type  = cleaned_data["scope_type"]
        permissions = cleaned_data["permissions"]
        
        validate_permissions(scope_type, permissions)
        return cleaned_data

class RoleInline(GenericTabularInline, TabularInline):
    model               = Role
    ct_field            = "scope_type"
    ct_fk_field         = "scope_uuid"
    fields              = ("priority", "name", "slug", "is_active", *created_modified_by_fields)
    ordering            = ("priority", "name")
    readonly_fields     = (*created_modified_by_fields,)
    prepopulated_fields = {"slug": ["name"]}
    show_change_link    = True
    tab                 = True

# TODO: Inlines for all role-dependent objects, directly defined here
class RoleAdmin(CustomModelAdmin):
    model               = Role
    form                = RoleForm
    resource_classes    = (RoleResource,)
    list_display        = ("scope_type", "scope_object", "priority", "name", "slug", "is_active", *created_modified_by_fields)
    list_display_links  = ("scope_type", "scope_object", "priority", "name", "slug")
    list_filter         = (scope_type_filter, "name", "slug", *created_modified_by_filter)
    ordering            = ("scope_type", "scope_uuid", "priority", "name")
    search_fields       = ("name", "slug", "description")
    readonly_fields     = (*created_modified_by_fields,)
    prepopulated_fields = {"slug": ["name"]}
    filter_horizontal   = ("permissions",)

    fieldsets = (
        (None, {
            "fields": (("scope_type", "scope_uuid"), ("name", "slug"), ("priority", "is_active")),
        }),
        (_("Description"), {
            "classes": ("tab",),
            "fields": ("description", "text_format"),
        }),
        (_("Permissions"), {
            "classes": ("tab",),
            "fields": ("permissions",),
        }),
        created_modified_by_fieldset,
    )

    add_fieldsets = (
        (None, {
            "fields": (("scope_type", "scope_uuid"), ("name", "slug"), ("priority", "is_active")),
        }),
        (_("Description"), {
            "classes": ("tab",),
            "fields": ("description", "text_format"),
        }),
        (_("Permissions"), {
            "classes": ("tab",),
            "fields": ("permissions",),
        }),
    )
