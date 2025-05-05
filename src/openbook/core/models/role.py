# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from datetime                           import timezone

from django.conf                        import settings
from django.contrib.auth.models         import AbstractUser, Permission
from django.core.exceptions             import ValidationError
from django.db                          import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text                  import format_lazy
from django.utils.translation           import gettext_lazy as _

from .mixins.active                     import ActiveInactiveMixin
from .mixins.audit                      import CreatedModifiedByMixin
from .mixins.auth                       import RoleBasedObjectPermissionsMixin
from .mixins.datetime                   import DurationMixin
from .mixins.datetime                   import ValidityTimeSpanMixin
from .mixins.i18n                       import TranslatableMixin
from .mixins.slug                       import NonUniqueSlugMixin
from .mixins.text                       import NameDescriptionMixin
from .mixins.uuid                       import UUIDMixin
from ..middleware.current_user          import get_current_user

class ScopeMixin(RoleBasedObjectPermissionsMixin):
    """
    Abstract mixin for models that are linked to a scope via a generic relation. The scope will be
    used for role assignments to assign scoped roles to users.
    """
    scope_type   = models.ForeignKey(ContentType, verbose_name=_("Scope Type"), on_delete=models.CASCADE)
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
        if not hasattr(self, "role"):
            return
        
        if not self.role:
            return
    
        if self.scope_type != self.role.scope_type or self.scope_uuid != self.role.scope_uuid:
            raise ValidationError(_("The scopes of the role and this object don't match."))

    def get_scope(self) -> models.Model:
        """
        Access management requires appropriate permissions in the referenced scope.
        """
        return self.scope_object

    def has_perm(self, user_obj: AbstractUser, perm: str) -> bool:
        """
        The referenced role must be of lower or equal priority than any of the user's roles.
        """
        principally_allowed = super().has_perm(user_obj, perm)

        if not principally_allowed:
            return False
        
        if ".view_" in perm:
            return True
        
        priority = self.priority if hasattr(self, "priority") else self.role.priority

        scope = self.get_scope()
        count = scope.role_assignments.filter(user=user_obj, role__priority__gte=priority).count()
        return count > 0

class Role(UUIDMixin, ScopeMixin, CreatedModifiedByMixin, NonUniqueSlugMixin, NameDescriptionMixin, ActiveInactiveMixin):
    """
    Object-based permissions are based on roles that users have in a given context (scope).
    Roles bundle one or more permissions granted to all users assigned to them. For example
    textbooks and courses use roles to restrict who can use them how.
    """
    priority    = models.PositiveSmallIntegerField(verbose_name=_("Priority"), help=_("Low values mean less privileges. Make sure to correctly prioritize the rolls to avoid privilege escalation."))
    permissions = models.ManyToManyField(Permission, verbose_name=_("Permissions"), blank=True, related_name="roles")

    class Meta:
        verbose_name        = _("Role")
        verbose_name_plural = _("Roles")

        constraints = [
            models.UniqueConstraint(fields=["scope_type", "scope_uuid", "slug"], name="unique_scope_slug"),
        ]

        indexes = [
            models.Index(fields=["scope_type", "scope_uuid", "slug"], name="scope_slug_idx"),
        ]
    
    def __str__(self):
        return f"{self.name} {ActiveInactiveMixin.__str__(self)}".strip()
    
    def clean(self):
        """
        Validate that only allowed permissions are assigned to the role.
        """
        allowed_permissions = AllowedRolePermission.objects.filter(scope_type=self.scope_type)

        for permission in self.permissions:
            if not allowed_permissions.contains(permission):
                perm    = f"{permission.content_type.app_label}.{permission.codename}"
                message = format_lazy(_("Permission {perm} is not allowed in role {role}"), perm=perm, role=self.name)
                raise ValidationError(message)

class AccessRequest(UUIDMixin, ScopeMixin, CreatedModifiedByMixin, DurationMixin):
    """
    To gain access, users may send access requests to the owners of a given scope. This contains the
    scope and the requested role, so that the request can be converted into a role assignment, if th
    request is granted.

    NOTE: Take care to exclude `decision` and `decision_date` when creating and modifying objects.
    """
    class Decision(models.TextChoices):
        PENDING  = "pending",  _("Decision Pending")
        ACCEPTED = "accepted", _("Accepted")
        DENIED   = "denied",   _("Denied")

    role          = models.ForeignKey("Role", on_delete=models.CASCADE, related_name="access_requests")
    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="access_requests")
    end_date      = models.DateTimeField(verbose_name=_("Enrollment Ends on"), blank=True, null=True)
    decision      = models.CharField(verbose_name=_("Decision"), max_length=10, choices=Decision, default=Decision.PENDING, null=False, blank=False)
    decision_date = models.DateTimeField(verbose_name=_("Decision Date"), blank=True, null=True)

    class Meta:
        verbose_name        = _("Access Request")
        verbose_name_plural = _("Access Requests")

        indexes = [
            models.Index(fields=["scope_type", "scope_uuid", "role"], name="scope_role_idx"),
            models.Index(fields=["user"], name="user_idx"),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.role.name}"

    def has_perm(self, user_obj: AbstractUser, perm: str) -> bool:
        """
        Always allow to view or delete own access requests, as well as to create new pending requests for
        the own user. Otherwise use inherited object permission, that the target role's priority must be
        lower or equal any priority of the own assigned roles.
        """
        if user_obj == get_current_user():
            if ".delete_" in perm or ".view_" in perm:
                return True
            if ".add_" in perm and self.decision == self.Decision.PENDING:
                return True

        return super().has_perm(user_obj, perm)

    def save(self, *args, **kwargs):
        """
        Force pending decision when a new access request is saved. Also update the role assignments
        accordingly when a decision is made.
        """
        if not self.pk:
            self.decision = self.Decision.PENDING
            self.decision_date = None
        
        match self.decision:
            case self.Decision.ACCEPTED:
                RoleAssignment.enroll(enrollment=self)
            case self.Decision.DENIED:
                RoleAssignment.withdraw(enrollment=self)

        super().save(*args, **kwargs)

    def accept(self):
        """
        Accept request by setting the decision to accepted, saving the object and creating
        the role assignment.
        """
        self.decision      = self.Decision.ACCEPTED
        self.decision_date = timezone.now()
        self.save()

    def deny(self):
        """
        Deny access request by setting the decision to denied and saving the object.
        """
        self.decision      = self.Decision.DENIED
        self.decision_date = timezone.now()
        self.save()

class EnrollmentMethod(UUIDMixin, ScopeMixin, CreatedModifiedByMixin, NameDescriptionMixin, ActiveInactiveMixin, DurationMixin):
    """
    Enrollment methods all users to enroll themselves to get access. Enrollment is always bound to
    a role that will be assigned to the users and can optionally have a limited duration. Also the
    enrollment can be protected with a passphrase, that users must enter.

    NOTE: Take care to not reveal the passphrase when enrollment methods are queried or viewed.
    """
    role       = models.ForeignKey("Role", on_delete=models.CASCADE, related_name="enrollment_methods")
    end_date   = models.DateTimeField(verbose_name=_("Enrollment Ends on"), blank=True, null=True)
    passphrase = models.CharField(verbose_name=_("Passphrase"), max_length=100, null=False, blank=True)

    class Meta:
        verbose_name        = _("Enrollment Method")
        verbose_name_plural = _("Enrollment Methods")

        indexes = [
            models.Index(fields=["scope_type", "scope_uuid", "role"], name="scope_role_idx"),
        ]
    
    def __str__(self):
        return f"{self.name} {ActiveInactiveMixin.__str__(self)}".strip()

    def has_perm(self, user_obj: AbstractUser, perm: str) -> bool:
        """
        A user can only add/change/delete enrollment methods with lower or equal priority to his/her own roles.

        **Caveat:** Take care to not reveal the passphrase when enrollment methods are queried or viewed.
        """
        principally_allowed = super().has_perm(user_obj, perm)

        if not principally_allowed:
            return False
        
        if ".view_" in perm:
            return True

        scope = self.get_scope()
        count = scope.role_assignments.filter(user=user_obj, role__priority__lte=self.role.priority).count()
        return count > 0

    def enroll(self, user, passphrase=None, check_passphrase=True):
        """
        Enroll the given user, optionally checking the passphrase. Raises a `ValueError` when
        the passphrase doesn't match.
        """
        RoleAssignment.enroll(enrollment=self, user=user, passphrase=passphrase, check_passphrase=check_passphrase)

class RoleAssignment(UUIDMixin, ScopeMixin, CreatedModifiedByMixin, ActiveInactiveMixin, ValidityTimeSpanMixin):
    """
    Role assignments assign a given role (defined in a given scope) to user, effectively
    granting the object-level permissions associated with them.
    """
    class AssignmentMethod(models.TextChoices):
        MANUAL          = "manual",          _("Manual Assignment")
        SELF_ENROLLMENT = "self-enrollment", _("Self-Enrollment")
        ACCESS_REQUEST  = "access-request",  _("Access Request")

    role              = models.ForeignKey("Role", on_delete=models.CASCADE, related_name="role_assignments")
    user              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="role_assignments")
    assignment_method = models.CharField(verbose_name=_("Assignment Method"), max_length=20, choices=AssignmentMethod, null=False, blank=False)
    enrollment_method = models.ForeignKey("EnrollmentMethod", on_delete=models.SET_NULL, null=True, related_name="role_assignments")
    access_request    = models.OneToOneField("AccessRequest", on_delete=models.SET_NULL, null=True, related_name="role_assignment")

    class Meta:
        verbose_name        = _("Role Assignment")
        verbose_name_plural = _("Role Assignments")

        constraints = [
            models.UniqueConstraint(fields=["scope_type", "scope_uuid", "role", "user"], name="unique_role_assignment"),
        ]

        indexes = [
            models.Index(fields=["scope_type", "scope_uuid", "role", "user"], name="role_assignment_idx"),
            models.Index(fields=["user"], name="user_idx"),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.role.name} {ActiveInactiveMixin.__str__(self)}".strip()

    @classmethod
    def enroll(
        cls,
        enrollment:EnrollmentMethod|AccessRequest,
        user: AbstractUser|None = None,
        passphrase: str|None    = None,
        check_passphrase: bool  = True
    ) -> None:
        """
        Apply the given enrollment method or access request to a user, effectively adding the role
        assignment. For access requests the user should not be given, as it is already contained
        in the access request object. For enrollment methods it must be given, however.

        Raises a `ValueError` when the passphrase doesn't match or the user is missing.
        """
        if hasattr(enrollment, "passphrase") and check_passphrase:
            if enrollment.passphrase and enrollment.passphrase != passphrase:
                raise ValueError(_("Incorrect passphrase"))
        
        if not user and hasattr(enrollment, "user"):
            user = enrollment.user
        
        if not user:
            raise ValueError(_("User missing"))
    
        assignment_methods = {
            EnrollmentMethod: cls.AssignmentMethod.SELF_ENROLLMENT,
            AccessRequest:    cls.AssignmentMethod.ACCESS_REQUEST,
        }
    
        role_assignment = cls(
            scope_type        = enrollment.scope_type,
            scope_uuid        = enrollment.scope_uuid,
            role              = enrollment.role,
            user              = user,
            assignment_method = assignment_methods.get(type(enrollment), cls.AssignmentMethod.MANUAL),
            start_date        = timezone.now(),
        )

        if enrollment.end_date is not None:
            role_assignment.end_date = enrollment.end_date
        elif enrollment.duration_period and enrollment.duration_value:
            role_assignment.end_date = enrollment.add_duration_to(role_assignment.start_date)

        role_assignment.save()

    @classmethod
    def withdraw(
        cls,
        enrollment:EnrollmentMethod|AccessRequest,
        user: AbstractUser|None = None,
    ) -> None:
        """
        Withdraw role assignment for a given enrollment method or access request. For access requests the
        user should not be given, as it is already contained in the access request object. For enrollment
        methods it must be given, however.

        Raises a `ValueError` when the user is missing.
        """
        if not user and hasattr(enrollment, "user"):
            user = enrollment.user
        
        if not user:
            raise ValueError(_("User missing"))
    
        cls.objects.filter(
            scope_type  = enrollment.scope_type,
            scope_uuid  = enrollment.scope_uuid,
            role        = enrollment.role,
            user        = user,
        ).delete()

class Permission_T(TranslatableMixin):
    """
    Translated permission name.
    """
    parent = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="translations")
    name   = models.CharField(verbose_name=_("Permission Name"), max_length=255, null=False, blank=False)

    class Meta(TranslatableMixin.Meta):
        pass

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
            models.Index(fields=["scope_type"], name="scope_type_idx"),
        ]

    def __str__(self):
        return self.scope_type