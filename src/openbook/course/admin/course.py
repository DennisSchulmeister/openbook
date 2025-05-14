# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation         import gettext_lazy as _

from openbook.admin                   import CustomModelAdmin
from openbook.admin                   import ImportExportModelResource
from openbook.auth.admin.role         import RoleInline
from openbook.auth.admin.mixins.audit import created_modified_by_fields
from openbook.auth.admin.mixins.audit import created_modified_by_fieldset
from openbook.auth.admin.mixins.auth  import ScopedRolesResourceMixin
from openbook.auth.admin.mixins.auth  import permissions_fieldset
from ..forms.course                   import CourseForm
from ..models.course                  import Course

class CourseResource(ScopedRolesResourceMixin, ImportExportModelResource):
    class Meta:
        model = Course
        fields = (
            "id", "delete",
            "slug", "name",
            "description", "text_format", 
            *ScopedRolesResourceMixin.Meta.fields,
            "is_template"
        )
    
    def dehydrate_is_template(self, obj):
        return "true" if obj.is_template else "false"

class CourseAdmin(CustomModelAdmin):
    model               = Course
    form                = CourseForm
    resource_classes    = (CourseResource,)
    list_display        = ("name", "slug", "is_template", "owner", *created_modified_by_fields)
    list_display_links  = ("name", "slug", "owner")
    list_filter         = ("name", "is_template", "owner", *created_modified_by_fields)
    search_fields       = ("name", "slug", "owner", "description")
    readonly_fields     = (*created_modified_by_fields,)
    prepopulated_fields = {"slug": ["name"]}
    filter_horizontal   = ("public_permissions",)
    inlines             = (RoleInline,)

    fieldsets = (
        (None, {
            "fields": (("name", "slug", "is_template")) # License, Image
        }),
        (_("Description"), {
            "classes": ("tab",),
            "fields": ("description", "text_format"), # Description, Text Format, AI Notes
        }),
        permissions_fieldset,
        created_modified_by_fieldset,
    )

    add_fieldsets = (
        (None, {
            "fields": (("name", "slug", "is_template")) # License, Image
        }),
        (_("Description"), {
            "classes": ("tab",),
            "fields": ("description", "text_format"), # Description, Text Format, AI Notes
        }),
        permissions_fieldset,
    )
