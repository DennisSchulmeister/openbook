# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.admin import GroupAdmin

from ..models.user             import Group
from ...admin                  import CustomModelAdmin
from ...admin                  import ImportExportModelResource

class GroupResource(ImportExportModelResource):
    class Meta:
        model = Group

class CustomGroupAdmin(GroupAdmin, CustomModelAdmin):
    """
    Sub-class of Django's Group Admin to allow importing and exporting groups.
    """
    resource_classes = [GroupResource]
