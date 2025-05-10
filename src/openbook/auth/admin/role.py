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
from ..models.role            import Role

class RoleResource(ImportExportModelResource):
    class Meta:
        model = Role

class RoleInline(GenericTabularInline, TabularInline):
    model               = Role
    ct_field            = "scope_type"
    ct_fk_field         = "scope_uuid"
    fields              = ("name", "slug", "priority", "is_active", "created_by", "created_at", "modified_by", "modified_at")
    readonly_fields     = ("created_by", "created_at", "modified_by", "modified_at")
    prepopulated_fields = {"slug": ["name"]}
    show_change_link    = True
    tab                 = True

class RoleAdmin(CustomModelAdmin):
    model              = Role
    resource_classes   = (RoleResource,)
#     list_display       = ("id", "domain", "name", "short_name")
#     list_display_links = ("id", "domain")
#     search_fields      = ("domain", "name", "short_name")
# 
#     fieldsets = (
#         (None, {
#             "fields": ("id", "domain", "name", "short_name", "about_url", "brand_color")
#         }),
#     )
