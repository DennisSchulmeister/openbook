# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf                        import settings
from django.contrib.auth.models         import AbstractUser, Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.cache                  import cache
from django.core.exceptions             import ValidationError
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

    def has_obj_perm(self, user_obj: AbstractUser, perm: str) -> bool:
        """
        Check if the given user has the given permission on the object. This always checks the public
        permissions of the scope and all role assignments, if the user is authenticated. But it can be
        overridden to implement custom checks like "the owner is always authorized".

        Usually `super().has_obj_perm(user_obj, perm)` should still be called, when this method is overridden.

        Note, this method is called `has_obj_perm()` instead of `has_perm()` because the Django user model
        already has a method `has_perm()`.
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
        help_text    = _("The owner always has full permissions."),
        on_delete    = models.SET_DEFAULT,
        related_name = "+",
        default      = "",
        blank        = True,
        null         = True
    )

    roles              = GenericRelation("openbook_auth.Role", content_type_field="scope_type", object_id_field="scope_uuid")
    access_requests    = GenericRelation("openbook_auth.AccessRequest", content_type_field="scope_type", object_id_field="scope_uuid")
    enrollment_methods = GenericRelation("openbook_auth.EnrollmentMethod", content_type_field="scope_type", object_id_field="scope_uuid")
    role_assignments   = GenericRelation("openbook_auth.RoleAssignment", content_type_field="scope_type", object_id_field="scope_uuid")

    public_permissions = models.ManyToManyField(
        Permission,
        verbose_name = _("Public Permissions"),
        help_text    = _("Permissions available to logged-out users and all logged-in users independent of their role."),
        blank        = True,
        related_name = "+",
    )

    class Meta:
        abstract = True
    
    @staticmethod
    def content_type_is_scope(content_type: ContentType) -> bool:
        """
        Check whether the given content type implements `ScopedRolesMixin` and therefor acts as
        a permission scope for user roles.
        """
        model = content_type.model_class()
        return not model is None and issubclass(model, ScopedRolesMixin)

    @classmethod
    def get_scope_model_content_types(cls) -> list[ContentType]:
        """
        Get a filtered list of content types (models) that implement the scoped roles mixin and
        therefor act as a permission scope for user roles. Since this is a somewhat expensive
        operation, the result will be cached using the Django cache mechanism.
        """
        cache_key = "openbook_auth:scoped_roles_mixin:scope_models"
        result: list[models.Model] = cache.get(cache_key, [])

        if len(result) > 0:
            return result

        for content_type in ContentType.objects.all():
            if cls.content_type_is_scope(content_type):
                result.append(content_type)
        
        cache.set(cache_key, result)
        return result

    @classmethod
    def get_scope_model_content_type_ids(cls) -> list[int]:
        """
        Get content type ids of models that are permission scopes for user roles.
        """
        result: list[int] = []

        for content_type in cls.get_scope_model_content_types():
            result.append(content_type.pk)
        
        return result

    def save(self, *args, **kwargs):
        """
        Automatically populate the `owner` field.
        Care must be taken to call `super().save(*args, **kwargs)` when this method is overridden.
        """
        user = get_current_user()

        if user and user.is_authenticated:
            if not self.owner:
                self.owner = user

        super().save(*args, **kwargs)

class ScopeMixin(RoleBasedObjectPermissionsMixin):
    """
    Abstract mixin for models that are linked to a scope via a generic relation. The scope will be
    used for role assignments to assign scoped roles to users. This is used internally to add a
    generic relation for the scope to models like `AccessRequest` or `EnrollmentMethod`.
    """
    scope_type   = models.ForeignKey(ContentType, verbose_name=_("Scope Type"), null=True, on_delete=models.CASCADE, related_name = "+")
    scope_uuid   = models.UUIDField(verbose_name=_("Scope UUID"))
    scope_object = GenericForeignKey("scope_type", "scope_uuid")

    class Meta:
        abstract = True

    @classmethod
    def from_obj(cls, other_obj: "ScopeMixin") -> "ScopeMixin":
        """
        Create a new instance from another scope-related model instance, copying over the
        scope reference and optionally the role.
        """
        from ..role import Role
        
        obj = cls()
        obj.scope_type = other_obj.scope_type
        obj.scope_uuid = other_obj.scope_uuid

        if hasattr(obj, "role"):
            if hasattr(other_obj, "role"):
                obj.role = other_obj.role
            elif isinstance(other_obj, Role):
                obj.role = other_obj

        return obj

    def clean(self):
        """
        Validate that role and this object refer to the same scope (if `role` field exists).
        """
        if not hasattr(self, "role") or not self.role:
            return
        
        if not self.scope_type or not self.scope_uuid:
           self.scope_type = self.role.scope_type
           self.scope_uuid = self.role.scope_uuid
        elif self.scope_type != self.role.scope_type or self.scope_uuid != self.role.scope_uuid:
            raise ValidationError(_("The scopes of the role and this object don't match."))

        super().clean()

    def get_scope(self) -> models.Model:
        """
        Access management requires appropriate permissions in the referenced scope.
        """
        return self.scope_object

    def has_obj_perm(self, user_obj: AbstractUser, perm: str) -> bool:
        """
        Object-level permission for all models with a scope reference. If this is a role,
        its priority must be of lower or equal priority than any of the user's roles.
        Otherwise the priority of the referenced role must be of lower or equal priority
        than any of the user's roles.
        """
        principally_allowed = super().has_obj_perm(user_obj, perm)

        if not principally_allowed:
            return False
        
        if ".view_" in perm:
            return True
        
        if hasattr(self, "priority"):
            priority = self.priority
        elif hasattr(self, "role"):
            priority = self.role.priority
        else:
            return False

        return self.get_scope().role_assignments.filter(
            scope_type          = self.scope_type,
            scope_uuid          = self.scope_uuid,
            user                = user_obj,
            role__priority__gte = priority
        ).count() > 0
