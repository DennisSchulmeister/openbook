# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                         import models
from django.utils.translation          import gettext_lazy as _

from openbook.auth.models.mixins.audit import CreatedModifiedByMixin
from openbook.core.models.mixins.uuid  import UUIDMixin

from .library                          import Library

class Publication(UUIDMixin, CreatedModifiedByMixin):
    """
    To allow upgrading the installed libraries without modifying the server installation and also
    to allow 3rd-parties to provide additional libraries the server provides a "library repository"
    similar in spirit to PyPi or npmjs. But here the OpenBook server is both server and client.
    As a server it can publish libraries and other installations can download and install as a client.
    Additionally clients can retrieve version upgrades from the publishing server.

    This model defines which of the installed libraries are published by the server. The central
    `https://openbook.studio` installation publishes the core libraries. Other installations should
    therefore only publish their own self-developed libraries.
    """
    library = models.ForeignKey(Library, verbose_name=_("Library"), on_delete=models.CASCADE)
    publish = models.BooleanField(verbose_name=_("Publish"), help_text=_("Allow other installations to download the library from this server."))

    class Meta:
        verbose_name        = _("Published Library")
        verbose_name_plural = _("Published Libraries")
