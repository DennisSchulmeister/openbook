# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models import AbstractUser
from django.db                  import models
from django.utils.translation   import gettext_lazy as _

from ..role                     import RoleAssignment

class RoleBasedObjectPermissionsMixin(models.Model):
    """
    Mixin class for all models that support role-based object permissions.
    """
    def has_perm(self, user_obj: AbstractUser, perm: str) -> bool:
        """
        Check if the given user has the given permission on the object. By default this checks all role
        assignments of the user to find a role with the permission. But it can be overridden to implement
        custom checks like "the owner is always authorized". Then the inherited method should still be
        called, if the custom check fails.
        """
        scope = self.get_scope()
        app_label, codename = perm.split(".")
        
        return RoleAssignment.objects.for_scope(scope).filter(
            user = user_obj,
            role__permissions__content_type__app_label = app_label,
            role__permissions__codename = codename
        ).count() > 0
        
    def get_scope(self) -> models.Model:
        """
        Get the model instance with the role assignments. Usually this is the object itself, but for
        composite models like course materials and courses this should be the parent object (e.g. course).
        In that case this method must be overridden to return the parent object.
        """
        return self