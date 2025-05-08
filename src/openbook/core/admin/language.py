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

from ..models.language        import Language
from ...admin                 import ImportExportModelResource

class LanguageResource(ImportExportModelResource):
    class Meta:
        model = Language

class LanguageAdmin(ModelAdmin, ImportExportModelAdmin):
    model              = Language
    resource_classes   = [LanguageResource]
    list_display       = ["language", "name"]
    list_display_links = ["language", "name"]
    search_fields      = ["language", "name"]
    fields             = ["language", "name"]
