# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models           import Permission
from django.db                            import models
from django.contrib.contenttypes.models   import ContentType
from django.utils.translation             import gettext_lazy as _

from openbook.core.models.mixins.uuid     import UUIDMixin

class AllowedRolePermission(UUIDMixin):
    """
    Allowed permission to be used in scoped roles. This is used to restrict the list of available
    permissions when defining roles.
    """
    scope_type  = models.ForeignKey(ContentType, verbose_name=_("Scope Type"), on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, verbose_name=_("Permissions"), blank=True, related_name="scope_types")

    class Meta:
        verbose_name        = _("Allowed Role Permission")
        verbose_name_plural = _("Allowed Role Permissions")

        indexes = [
            models.Index(fields=("scope_type",)),
        ]

    def __str__(self):
        return self.scope_type

    @classmethod
    def get_for_scope_type(cls, scope_type: ContentType) -> "list[AllowedRolePermission]":
        """
        Get a list of allowed permissions for the given scope type.
        """
        return cls.objects.filter(scope_type=scope_type)