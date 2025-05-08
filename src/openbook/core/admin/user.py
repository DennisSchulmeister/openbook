# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.admin import UserAdmin
from import_export.admin       import ImportExportModelAdmin
from unfold.admin              import ModelAdmin

from ..models.user             import User
from ...admin                  import ImportExportModelResource

class UserResource(ImportExportModelResource):
    class Meta:
        model = User

class CustomUserAdmin(UserAdmin, ModelAdmin, ImportExportModelAdmin):
    """
    Sub-class of Django's User Admin to integrate the additional fields of
    Application Users.
    """
    resource_classes = [UserResource]
