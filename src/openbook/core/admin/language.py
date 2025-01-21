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

class LanguageAdmin(admin.ModelAdmin):
    model              = models.Language
    list_display       = ["language", "name"]
    list_display_links = ["language", "name"]
    search_fields      = ["language", "name"]
    fields             = ["language", "name"]
