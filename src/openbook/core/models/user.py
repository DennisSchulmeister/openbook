# Lernspiel Online: Lecture Game Platform - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation   import gettext_lazy as _

class User(AbstractUser):
    """
    As recommended by the Django documentation, custom auth user model just in
    case we want to extend it later.
    """
    pass

class UserGroup(Group):
    """
    Dummy class to move the Group model from `django.contrib.auth` into our own app,
    so that users and groups stand together in the Admin.
    """
    class Meta():
        verbose_name        = _("User Group")
        verbose_name_plural = _("User Groups")
