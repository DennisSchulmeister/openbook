# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                import models
from django.utils.translation import gettext_lazy as _
from .mixins.i18n             import TranslatableMixin
from .mixins.uuid             import UUIDMixin
from .mixins.text             import NameDescriptionMixin

class HTMLComponent(UUIDMixin):
    """
    Most libraries define HTML custom elements to be used in the textbooks. This model makes these
    custom elements known to the WYSIWYG editor. Note that a HTML component can still be used if
    it is not contained in the database. But it won't be possible the add the element to a textbook
    or modify its properties in the WYSIWYG editor.
    """
    library    = models.ForeignKey("htmllibrary", on_delete=models.CASCADE, related_name="components")
    tag_name   = models.CharField(verbose_name=_("Tag Name"), max_length=100)
    definition = models.JSONField(verbose_name=_("JSON Definition"), blank=True, default=None)

    class Meta:
        verbose_name        = _("HTML Component")
        verbose_name_plural = _("HTML Components")
        constraints         = [models.UniqueConstraint(fields=("library", "tag_name"), name="unique_html_component")]

class HTMLComponentText(UUIDMixin, TranslatableMixin, NameDescriptionMixin):
    parent = models.ForeignKey(HTMLComponent, on_delete=models.CASCADE, related_name="translations")

    class Meta(TranslatableMixin.Meta):
        verbose_name        = _("HTML Component: Translated Text")
        verbose_name_plural = _("HTML Component: Translated Texts")
