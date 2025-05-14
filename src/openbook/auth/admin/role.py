# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import gettext_lazy as _
from unfold.admin             import TabularInline

from openbook.admin           import CustomModelAdmin
from openbook.admin           import ImportExportModelResource
from .mixins.audit            import audit_fields
from .mixins.audit            import audit_fieldset
from .mixins.auth             import scope_type_filter
from ..forms.role             import RoleForm
from ..models.role            import Role

class RoleResource(ImportExportModelResource):
    class Meta:
        model = Role

class RoleInline(GenericTabularInline, TabularInline):
    model               = Role
    ct_field            = "scope_type"
    ct_fk_field         = "scope_uuid"
    fields              = ("priority", "name", "slug", "is_active", *audit_fields)
    ordering            = ("priority", "name")
    readonly_fields     = (*audit_fields,)
    prepopulated_fields = {"slug": ["name"]}
    show_change_link    = True
    tab                 = True

class RoleAdmin(CustomModelAdmin):
    model               = Role
    form                = RoleForm
    resource_classes    = (RoleResource,)
    list_display        = ("scope_type", "scope_object", "priority", "name", "slug", "is_active", *audit_fields)
    list_display_links  = ("scope_type", "scope_object", "priority", "name", "slug")
    list_filter         = (scope_type_filter, "name", "slug", *audit_fields)
    ordering            = ("scope_type", "scope_uuid", "priority", "name")
    search_fields       = ("name", "slug", "description")
    readonly_fields     = (*audit_fields,)
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
        audit_fieldset,
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
