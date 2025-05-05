# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf                        import settings
from django.contrib.auth.models         import AbstractUser, Permission
from django.contrib.contenttypes.fields import GenericRelation
from django.db                          import models
from django.utils.translation           import gettext_lazy as _

from ...middleware.current_user         import get_current_user

class RoleBasedObjectPermissionsMixin(models.Model):
    """
    Mixin class for all models that support role-based object permissions. Use this instead of
    `ScopedRolesMixin` for composite models, where the model itself is not the scope for the roles,
    e.g. for course materials where the roles belong to the parent course. Override `get_scope()`
    to return the parent model, which must inherit `ScopedRolesMixin`, instead.
    """
    class Meta:
        abstract = True

    def has_perm(self, user_obj: AbstractUser, perm: str) -> bool:
        """
        Check if the given user has the given permission on the object. This always checks the public
        permissions of the scope and all role assignments, if the user is authenticated. But it can be
        overridden to implement custom checks like "the owner is always authorized".

        Usually `super().has_perm(user_obj, perm)` should still be called, when this method is overridden.
        """
        scope = self.get_scope()
        app_label, codename = perm.split(".")

        if scope.public_permissions.filter(
            content_type__app_label = app_label,
            codename = codename
        ).count() > 0:
            return True
        
        return user_obj.is_authenticated() and scope.role_assignments.filter(
            user = user_obj,
            role__permissions__content_type__app_label = app_label,
            role__permissions__codename = codename
        ).count() > 0
        
    def get_scope(self) -> "ScopedRolesMixin":
        """
        Get the model instance with the role assignments. Usually this is the object itself, but for
        composite models like course materials and courses this should be the parent object (e.g. course).
        In that case this method must be overridden to return the parent object.
        """
        return self

class ScopedRolesMixin(RoleBasedObjectPermissionsMixin):
    """
    Mixin class for models that have scoped roles to grant permissions. Inheriting this mixin allows
    the model to have roles, role assignment, enrollment methods and access requests. This includes the
    `RoleBasedObjectPermissionsMixin`, so that object permissions can be checked on the model.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name = _("Owner"),
        help         = _("The owner always has full permissions"),
        on_delete    = models.SET_DEFAULT,
        default      = "",
        blank        = True,
        null         = True
    )

    roles              = GenericRelation("Role")
    access_requests    = GenericRelation("AccessRequest")
    enrollment_methods = GenericRelation("EnrollmentMethod")
    role_assignments   = GenericRelation("RoleAssignment")

    public_permissions = models.ManyToManyField(
        Permission,
        verbose_name = _("Public Permissions"),
        help         = _("Permissions available to logged-out users and all logged-in users independent of their role"),
        blank        = True,
        related_name = "+",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Automatically populate the `owner` field.
        Care must be taken to call `super().save(*args, **kwargs)` when this method is overridden.
        """
        user = get_current_user()

        if user and user.is_authenticated:
            if not self.pk:
                self.owner = user

        super().save(*args, **kwargs)