# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.admin              import display
from django.db                         import models
from django.utils.translation          import gettext_lazy as _

from openbook.auth.models.mixins.audit import CreatedModifiedByMixin
from ..validators                      import validate_library_name_part
from ..validators                      import validate_version_number
from .mixins.file                      import FileUploadMixin
from .mixins.i18n                      import TranslatableMixin
from .mixins.text                      import NameDescriptionMixin
from .mixins.uuid                      import UUIDMixin

class HTMLLibrary(UUIDMixin, CreatedModifiedByMixin):
    """
    Textbooks are basically static HTML pages that embed the OpenBook JavaScript libraries to render
    custom components (web components). Those web components might in turn communicate with the server
    if necessary, but usually are working stand-alone. For this the distribution bundle needs to be
    loaded via the corresponding `<script>` and `<link rel="stylesheet">` tags.

    To make a library available to the server and especially the WYSIWYG editor, it must be "installed"
    on the server. This includes creating a few database entries (of which this is the main one) and
    placing the bundled library code in the directory `MEDIA_DIR/lib/{organization}/{library}/{version}`.
    """
    organization = models.CharField(verbose_name=_("Organization"), max_length=100, validators=[validate_library_name_part])
    name         = models.CharField(verbose_name=_("Name"), max_length=100, validators=[validate_library_name_part])
    author       = models.CharField(verbose_name=_("Author"), max_length=100, blank=True, default="")
    license      = models.CharField(verbose_name=_("License"), max_length=50, blank=True, default="")
    website      = models.URLField(verbose_name=_("Website"), blank=True, default="")
    coderepo     = models.URLField(verbose_name=_("Code Repository"), blank=True, default="")
    bugtracker   = models.URLField(verbose_name=_("Bug Tracker"), blank=True, default="")
    
    published = models.BooleanField(
        verbose_name = _("Published"),
        default      = True,
        help_text    = _("Allow other installations to download the library from this server"),
    )

    class Meta:
        verbose_name        = _("HTML Library")
        verbose_name_plural = _("HTML Libraries")
        constraints         = [models.UniqueConstraint(fields=("organization", "name"), name="unique_library_name")]

    def __str__(self):
        return self.name
    
    @display(description=_("Fully Qualified Name"))
    def fqn(self):
        return f"@{self.organization}/{self.name}"

class HTMLLibraryText(UUIDMixin, TranslatableMixin):
    parent            = models.ForeignKey(HTMLLibrary, on_delete=models.CASCADE, related_name="translations")
    short_description = models.CharField(verbose_name=_("Short Description"), max_length=255)

    class Meta(TranslatableMixin.Meta):
        verbose_name        = _("HTML Library: Translated Text")
        verbose_name_plural = _("HTML Library: Translated Texts")

class HTMLLibraryVersion(UUIDMixin, FileUploadMixin):
    parent       = models.ForeignKey(HTMLLibrary, on_delete=models.CASCADE, related_name="versions")
    version      = models.CharField(verbose_name=_("Version"), max_length=50, validators=[validate_version_number])
    dependencies = models.JSONField(verbose_name=_("Dependencies"), null=True, blank=True, default=None)
    frontend_url = models.CharField(verbose_name=_("Frontend URL"), blank=True)

    class Meta:
        verbose_name        = _("HTML Library: Version")
        verbose_name_plural = _("HTML Library: Versions")
        constraints         = [models.UniqueConstraint(fields=("parent", "version"), name="unique_library_version")]
        ordering            = ["parent", "-version"]

    def __str__(self):
        return f"{self.version}"
    
    def save(self, *args, **kwargs):
        """
        Populate frontend url when the model is saved.
        """
        self.frontend_url = f"lib/@{self.parent.organization}/{self.parent.name}/{self.version}"
        super().save(*args, **kwargs)
    
    def calc_file_path_hook(self, filename):
        return f"lib/@{self.parent.organization}_{self.parent.name}_{self.version}.zip"