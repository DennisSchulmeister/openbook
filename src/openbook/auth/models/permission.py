# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models           import Permission
from django.db                            import models
from django.utils.translation             import gettext_lazy as _

from openbook.core.models.mixins.i18n     import TranslatableMixin

class Permission_T(TranslatableMixin):
    """
    Translated permission name.
    """
    parent = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="translations")
    name   = models.CharField(verbose_name=_("Permission Name"), max_length=255, null=False, blank=False)

    class Meta(TranslatableMixin.Meta):
        pass