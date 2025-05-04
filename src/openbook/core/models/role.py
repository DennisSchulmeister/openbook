# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from datetime                           import timezone
from typing                             import TypeVar, Generic

from django.conf                        import settings
from django.contrib.auth.models         import AbstractBaseUser, Permission
from django.core.exceptions             import ValidationError
from django.db                          import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation           import gettext_lazy as _

from .mixins.active                     import ActiveInactiveMixin
from .mixins.audit                      import CreatedModifiedByMixin
from .mixins.datetime                   import DurationMixin
from .mixins.datetime                   import ValidityTimeSpanMixin
from .mixins.slug                       import NonUniqueSlugMixin
from .mixins.text                       import NameDescriptionMixin
from .mixins.uuid                       import UUIDMixin

class ScopeMixin(models.Model):
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
            raise ValidationError(_("The scopes of the role and this object don't match"))

ScopeMixin_T = TypeVar("ScopeMixin_T", bound="ScopeMixin")

class ScopeQuerySet(models.QuerySet, Generic[ScopeMixin_T]):
    def for_scope(self, obj: models.Model) -> "ScopeQuerySet[ScopeMixin_T]":
        """
        Filter queryset by scope model.
        """
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(scope_type=content_type, scope_uuid=obj.pk)

class ScopeManager(models.Manager, Generic[ScopeMixin_T]):
    def get_queryset(self) -> ScopeQuerySet[ScopeMixin_T]:
        """
        Return a new `ScopeQuerySet`.
        """
        return ScopeQuerySet(self.model, using=self._db)

    def for_scope(self, obj: models.Model) -> ScopeQuerySet[ScopeMixin_T]:
        """
        Return queryset filtered by a given scope model.
        """
        return self.get_queryset().for_scope(obj)

class Role(UUIDMixin, ScopeMixin, CreatedModifiedByMixin, NonUniqueSlugMixin, NameDescriptionMixin, ActiveInactiveMixin):
    """
    Object-based permissions are based on roles that users have in a given context (scope).
    Roles bundle one or more permissions granted to all users assigned to them. For example
    textbooks and courses use roles to restrict who can use them how.

    NOTE: A `GenericRelation` should be added to each model that supports roles.
    """
    permissions = models.ManyToManyField(Permission, verbose_name=_("Permissions"), blank=True)

    objects: ScopeManager["Role"] = ScopeManager()

    class Meta:
        verbose_name        = _("Role")
        verbose_name_plural = _("Roles")

        constraints = [
            models.UniqueConstraint(fields=["scope_type", "scope_uuid", "slug"], name="unique_role_slug")
        ]
    
    def __str__(self):
        return f"{self.name} {ActiveInactiveMixin.__str__(self)}".strip()

class AccessRequest(UUIDMixin, ScopeMixin, CreatedModifiedByMixin, DurationMixin):
    """
    To gain access, users may send access requests to the owners of a given scope. This contains the
    scope and the requested role, so that the request can be converted into a role assignment, if th
    request is granted.

    NOTE: A `GenericRelation` should be added to each model that supports access requests.
    """
    class Decision(models.TextChoices):
        PENDING  = "pending",  _("Decision Pending")
        ACCEPTED = "accepted", _("Accepted")
        DENIED   = "denied",   _("Denied")

    role          = models.ForeignKey("Role", on_delete=models.CASCADE, related_name="access_requests")
    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="access_requests")
    has_end_date  = models.BooleanField(verbose_name=_("Has Enrollment End"), default=False)
    end_date      = models.DateTimeField(verbose_name=_("Enrollment Ends on"), blank=True, null=True)
    decision      = models.CharField(verbose_name=_("Decision"), max_length=10, choices=Decision, default=Decision.PENDING, null=False, blank=False)
    decision_date = models.DateTimeField(verbose_name=_("Decision Date"), blank=True, null=True)

    objects: ScopeManager["AccessRequest"] = ScopeManager()

    class Meta:
        verbose_name        = _("Access Request")
        verbose_name_plural = _("Access Requests")
    
    def __str__(self):
        return f"{self.user.username}: {self.role.name}"

    def accept(self):
        """
        Accept request by setting the decision to accepted, saving the object and creating
        the role assignment.
        """
        self.decision      = self.Decision.ACCEPTED
        self.decision_date = timezone.now()
        self.save()

        RoleAssignment.enroll(enrollment=self)

    def deny(self):
        """
        Deny access request by setting the decision to denied and saving the object.
        """
        self.decision      = self.Decision.DENIED
        self.decision_date = timezone.now()
        self.save()
    
    # TODO: Object-level permission. Need to be scope owner or have permission to change access requests and the user cannot be the own user.
    # Create is always allowed, delete when user is self or user is scope owner or user may delete access requests in the scope

class EnrollmentMethod(UUIDMixin, ScopeMixin, CreatedModifiedByMixin, NameDescriptionMixin, ActiveInactiveMixin, DurationMixin):
    """
    Enrollment methods all users to enroll themselves to get access. Enrollment is always bound to
    a role that will be assigned to the users and can optionally have a limited duration. Also the
    enrollment can be protected with a passphrase, that users must enter.

    NOTE: A `GenericRelation` should be added to each model that supports enrollment methods.
    """
    role         = models.ForeignKey("Role", on_delete=models.CASCADE, related_name="enrollment_methods")
    has_end_date = models.BooleanField(verbose_name=_("Has Enrollment End"), default=False)
    end_date     = models.DateTimeField(verbose_name=_("Enrollment Ends on"), blank=True, null=True)
    passphrase   = models.CharField(verbose_name=_("Passphrase"), max_length=100, null=False, blank=True)

    objects: ScopeManager["EnrollmentMethod"] = ScopeManager()
    
    class Meta:
        verbose_name        = _("Enrollment Method")
        verbose_name_plural = _("Enrollment Methods")
    
    def __str__(self):
        return f"{self.name} {ActiveInactiveMixin.__str__(self)}".strip()

    def enroll(self, user, passphrase=None, check_passphrase=True):
        """
        Enroll the given user, optionally checking the passphrase. Raises a `ValueError` when
        the passphrase doesn't match.
        """
        RoleAssignment.enroll(enrollment=self, user=user, passphrase=passphrase, check_passphrase=check_passphrase)

    # TODO: Object-level permission. Need to be the scope owner or have permission to add/change/delete enrollment methods

class RoleAssignment(UUIDMixin, ScopeMixin, CreatedModifiedByMixin, ActiveInactiveMixin, ValidityTimeSpanMixin):
    """
    Role assignments assign a given role (defined in a given scope) to user, effectively
    granting the object-level permissions associated with them.

    NOTE: A `GenericRelation` should be added to each model that supports roles.
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

    objects: ScopeManager["RoleAssignment"] = ScopeManager()

    class Meta:
        verbose_name        = _("Role Assignment")
        verbose_name_plural = _("Role Assignments")

        constraints = [
            models.UniqueConstraint(fields=["scope_type", "scope_uuid", "role", "user"], name="unique_role_assignment")
        ]

    def __str__(self):
        return f"{self.user.username}: {self.role.name} {ActiveInactiveMixin.__str__(self)}".strip()

    @classmethod
    def enroll(
        cls,
        enrollment:EnrollmentMethod|AccessRequest,
        user: AbstractBaseUser|None = None,
        passphrase: str|None        = None,
        check_passphrase: bool      = True
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
            has_start_date    = True,
            start_date        = timezone.now(),
        )

        if enrollment.end_date:
            role_assignment.has_end_date = True
            role_assignment.end_date     = enrollment.end_date
        elif enrollment.duration_period and enrollment.duration_value:
            role_assignment.has_end_date = True
            role_assignment.end_date     = enrollment.add_duration_to(role_assignment.start_date)

        role_assignment.save()