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
from openbook.core.models.mixins.i18n  import TranslatableMixin
from openbook.core.models.mixins.uuid  import UUIDMixin

from ..validators                      import validate_library_name, validate_version_number

class Library(UUIDMixin, CreatedModifiedByMixin):
    """
    Textbooks are basically static HTML pages that embed the OpenBook JavaScript libraries to render
    the user interface and custom components. This works without the server simply by downloading the
    distribution bundle of each library (either manually or with a bundler) and adding the corresponding
    `<script>` and `<link rel="stylesheet">` tags to the main HTML page.

    To make a library available to the server and especially the WYSIWYG editor, it must be "installed"
    on the server. This includes creating a few database entries (of which this is the main one) and
    placing the bundled library code in `MEDIA_DIR/lib/{name of library}`.
    """
    name       = models.CharField(verbose_name=_("Name"), max_length=100, validators=[validate_library_name])
    version    = models.CharField(verbose_name=_("Version"), max_length=50, validators=[validate_version_number])
    author     = models.CharField(verbose_name=_("Author"), max_length=100, blank=True, null=False, default="")
    license    = models.CharField(verbose_name=_("License"), max_length=50, blank=True, null=False, default="")
    website    = models.URLField(verbose_name=_("Website"), help_text=_("Website with documentation"), blank=True, null=False, default="")
    coderepo   = models.URLField(verbose_name=_("Source Code"), help_text=_("Code repository"), blank=True, null=False, default="")
    bugtracker = models.URLField(verbose_name=_("Bug Tracker"), blank=True, null=False, default="")
    required   = models.BooleanField(verbose_name=_("Required"), default=False, help_text=_("Required libraries will always be included in each textbook"))

    class Meta:
        verbose_name        = _("Library")
        verbose_name_plural = _("Libraries")
        constraints         = [models.UniqueConstraint("name", name="unique_name")]

    def __str__(self):
        return self.name

class Library_T(UUIDMixin, TranslatableMixin):
    parent      = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="translations")
    label       = models.CharField(verbose_name=_("Label"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), blank=True)

    class Meta(TranslatableMixin.Meta):
        pass
