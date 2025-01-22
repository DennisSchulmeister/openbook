# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib           import admin
from django.utils.translation import gettext_lazy as _
from ..                       import models

class SiteAdmin(admin.ModelAdmin):
    model              = models.Site
    list_display       = ["id", "domain", "name", "short_name"]
    list_display_links = ["id", "domain"]
    search_fields      = ["domain", "name", "short_name"]

    fieldsets = (
        (None, {
            "fields": ["id", "domain", "name", "short_name", "about_url"]
        }),
    )
