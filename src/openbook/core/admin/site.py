# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation import gettext_lazy as _
from import_export.admin      import ImportExportModelAdmin
from unfold.admin             import ModelAdmin

from ..models.site            import Site
from ...admin                 import ImportExportModelResource

class SiteResource(ImportExportModelResource):
    class Meta:
        model = Site

class SiteAdmin(ModelAdmin, ImportExportModelAdmin):
    model              = Site
    resource_classes   = [SiteResource]
    list_display       = ["id", "domain", "name", "short_name"]
    list_display_links = ["id", "domain"]
    search_fields      = ["domain", "name", "short_name"]

    fieldsets = (
        (None, {
            "fields": ["id", "domain", "name", "short_name", "about_url"]
        }),
    )
