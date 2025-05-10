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
from .mixins                  import audit_fields
from .mixins                  import audit_fieldset
from ..models.role            import Role

class RoleResource(ImportExportModelResource):
    class Meta:
        model = Role

class RoleInline(GenericTabularInline, TabularInline):
    model               = Role
    ct_field            = "scope_type"
    ct_fk_field         = "scope_uuid"
    fields              = ("name", "slug", "priority", "is_active", *audit_fields)
    readonly_fields     = (*audit_fields,)
    prepopulated_fields = {"slug": ["name"]}
    show_change_link    = True
    tab                 = True

class RoleAdmin(CustomModelAdmin):
    model               = Role
    resource_classes    = (RoleResource,)
    list_display        = ("scope_type", "scope_object", "name", "slug", "priority", "is_active", *audit_fields)
    list_display_links  = ("scope_type", "scope_object", "name", "slug")
    list_filter         = ("scope_type", "name", "slug", *audit_fields)
    search_fields       = ("name", "slug", "description")
    readonly_fields     = (*audit_fields,)
    prepopulated_fields = {"slug": ["name"]}

    # TODO: Filter scope_type: https://chatgpt.com/g/g-p-68128762bf848191860962c9aae6c388-openbook-development/c/681f4187-4e28-8007-99b6-7308e6d54c1f

#     fieldsets = (
#         (None, {
#             "fields": ("id", "domain", "name", "short_name", "about_url", "brand_color")
#         }),
#     )
