# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib                       import admin
from django.contrib.auth.models           import Permission
from django.db                            import models
from django.utils.translation             import gettext_lazy as _

from openbook.core.models.mixins.i18n     import TranslatableMixin
    
class Permission_T(TranslatableMixin):
    """
    Translated permission name.
    """
    parent = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="translations")
    name   = models.CharField(verbose_name=_("Translated Name"), max_length=255, null=False, blank=False)

    class Meta(TranslatableMixin.Meta):
        verbose_name        = _("Translated Permission")
        verbose_name_plural = _("Translated Permissions")
    
    @admin.display(description=_("Application"))
    def appname(self, obj=None):
        if not self.parent:
            return ""
    
        model = self.parent.content_type.model_class()
        return model._meta.app_config.verbose_name or self.parent.content_type.app_label
    
    @admin.display(description=_("Permission"))
    def codename(self, obj=None):
        if not self.parent:
            return ""
    
        return self.parent.name

    @admin.display(description=_("Code"))
    def perm(self, obj=None):
        if not self.parent:
            return ""
        
        return f"{self.parent.content_type.app_label}.{self.parent.codename}"