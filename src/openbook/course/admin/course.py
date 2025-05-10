# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation   import gettext_lazy as _
from openbook.admin             import CustomModelAdmin
from openbook.admin             import ImportExportModelResource
from openbook.auth.admin.role   import RoleInline
from openbook.auth.admin.mixins import audit_fields
from openbook.auth.admin.mixins import audit_fieldset
from ..models.course            import Course

class CourseResource(ImportExportModelResource):
    class Meta:
        model = Course

class CourseAdmin(CustomModelAdmin):
    model               = Course
    resource_classes    = (CourseResource,)
    list_display        = ("name", "slug", "is_template", *audit_fields)
    list_display_links  = ("name", "slug")
    list_filter         = ("name", "is_template", *audit_fields)
    search_fields       = ("name", "slug", "description")
    readonly_fields     = (*audit_fields,)
    prepopulated_fields = {"slug": ["name"]}
    inlines             = (RoleInline,)

    fieldsets = (
        (None, {
            "fields": ("name", "slug") # License, Image
        }),
        (_("Course Description"), {
            "classes": ("tab",),
            "fields": ("description", "text_format"), # Description, Text Format, AI Notes
        }),
        audit_fieldset,
    )

    add_fieldsets = (
        (None, {
            "fields": ("name", "slug") # License, Image
        }),
        (_("Course Description"), {
            "classes": ("tab",),
            "fields": ("description", "text_format"), # Description, Text Format, AI Notes
        }),
    )
