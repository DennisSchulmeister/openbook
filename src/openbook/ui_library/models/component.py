# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                        import models
from django.utils.translation         import gettext_lazy as _
from openbook.core.models.mixins.i18n import TranslatableMixin
from openbook.core.models.mixins.uuid import UUIDMixin
from .library                         import Library

class HTMLComponent(UUIDMixin):
    """
    Most libraries define HTML custom elements to be used in the textbooks. This model makes these
    custom elements known to the WYSIWYG editor. Note that a HTML component can still be used if
    it is not contained in the database. But it won't be possible the add the element to a textbook
    or modify its properties in the WYSIWYG editor.
    """
    library    = models.ForeignKey(Library, verbose_name=_("Library"), on_delete=models.CASCADE)
    htmltag    = models.CharField(verbose_name=_("HTML Tag"), max_length=100)
    definition = models.TextField(verbose_name=_("JSON Definition"), blank=True, null=False, default="")

    class Meta:
        verbose_name        = _("HTML Component")
        verbose_name_plural = _("HTML Components")

class HTMLComponent_T(UUIDMixin, TranslatableMixin):
    parent      = models.ForeignKey(HTMLComponent, on_delete=models.CASCADE, related_name="translations")
    label       = models.CharField(verbose_name=_("Label"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), blank=True)

    class Meta(TranslatableMixin.Meta):
        pass
