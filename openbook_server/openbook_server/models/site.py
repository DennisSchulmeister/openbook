# OpenBook Studio: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                import models
from django.utils.translation import gettext_lazy as _
from ..utils.models           import calc_file_path

class Site(models.Model):
    """
    Extended version of Django's built-in Site model that additionally allows to
    set a few theme parameters.
    """
    # Basic site data
    id     = models.PositiveIntegerField(verbose_name=_("Id"), primary_key=True, editable=True)
    domain = models.CharField(verbose_name=_("Domain Name"), max_length=100)
    name   = models.CharField(verbose_name=_("Display Name"), max_length=255)

    # Icon
    def _calc_file_path(self, filename):
        return calc_file_path(self._meta, self.id, filename)

    favicon = models.FileField(verbose_name=_("Website Icon"), upload_to=_calc_file_path)

    # Theming values
    header_bg   = models.CharField(verbose_name=_("Header Background"), max_length=100, default="#234769")
    header_fg   = models.CharField(verbose_name=_("Header Foreground"), max_length=100, default="white")
    header_link = models.CharField(verbose_name=_("Header Link Color"), max_length=20, default="crimson")

    main_bg   = models.CharField(verbose_name=_("Main Background"), max_length=100, default="white")
    main_fg   = models.CharField(verbose_name=_("Main Foreground"), max_length=100, default="rgb(10, 10, 10)")
    main_link = models.CharField(verbose_name=_("Main Link Color"), max_length=20, default="crimson")

    footer_bg   = models.CharField(verbose_name=_("Footer Background"), max_length=100, default="rgb(25, 25, 25)")
    footer_fg   = models.CharField(verbose_name=_("Footer Foreground"), max_length=100, default="lightgrey")
    footer_link = models.CharField(verbose_name=_("Footer Link Color"), max_length=20, default="lightgrey")

    # Django meta information
    class Meta:
        verbose_name        = _("Website")
        verbose_name_plural = _("Websites")

    def __str__(self):
        return self.name
