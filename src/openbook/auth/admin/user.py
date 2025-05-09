# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from openbook.admin import CustomModelAdmin
from openbook.admin import ImportExportModelResource
from ..models.user  import User

class UserResource(ImportExportModelResource):
    class Meta:
        model = User

class CustomUserAdmin(CustomModelAdmin):
    """
    Sub-class of Django's User Admin to integrate the additional fields of
    Application Users.
    """
    resource_classes = [UserResource]
