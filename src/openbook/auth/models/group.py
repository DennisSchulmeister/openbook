# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models import Group
from django.utils.translation   import gettext_lazy as _

class UserGroup(Group):
    """
    Dummy class to move the Group model from `django.contrib.auth` into our own app,
    so that users and groups stand together in the Admin.
    """
    class Meta():
        verbose_name        = _("User Group")
        verbose_name_plural = _("User Groups")