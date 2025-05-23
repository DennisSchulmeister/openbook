# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from datetime                             import timezone
from typing                               import TYPE_CHECKING
from django.conf                          import settings
from django.contrib.auth.models           import AbstractUser
from django.db                            import models
from django.utils.translation             import gettext_lazy as _
from django.utils.timezone                import now

from openbook.core.models.mixins.active   import ActiveInactiveMixin
from openbook.core.models.mixins.datetime import ValidityTimeSpanMixin
from openbook.core.models.mixins.uuid     import UUIDMixin
from .mixins.audit                        import CreatedModifiedByMixin
from .mixins.scope                        import ScopeMixin

if TYPE_CHECKING:
    from .access_request    import AccessRequest
    from .enrollment_method import EnrollmentMethod

class RoleAssignment(UUIDMixin, ScopeMixin, ActiveInactiveMixin, ValidityTimeSpanMixin, CreatedModifiedByMixin):
    """
    A role assignment assigns a given role (defined in a given scope) to a user, effectively
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
            models.UniqueConstraint(fields=("scope_type", "scope_uuid", "role", "user"), name="unique_role_assignment"),
        ]

        indexes = [
            models.Index(fields=("scope_type", "scope_uuid", "role", "user")),
            models.Index(fields=("user",)),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.role.name} {ActiveInactiveMixin.__str__(self)}".strip()

    def clean(self):
        """
        Set assignment method to manual, when it is empty. Needed for the Django Admin, because
        this field cannot be set manually.
        """
        if not self.assignment_method:
            self.assignment_method = self.AssignmentMethod.MANUAL

        return super().clean()

    @classmethod
    def enroll(
        cls,
        enrollment:"EnrollmentMethod|AccessRequest",
        user: AbstractUser|None = None,
        passphrase: str|None    = None,
        check_passphrase: bool  = True
    ) -> "RoleAssignment":
        """
        Apply the given enrollment method or access request to a user, effectively adding the role
        assignment. For access requests the user should not be given, as it is already contained
        in the access request object. For enrollment methods it must be given, however.

        Raises a `ValueError` when the passphrase doesn't match or the user is missing.
        """
        from .access_request    import AccessRequest
        from .enrollment_method import EnrollmentMethod

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
    
        try:
            role_assignment = cls.objects.get(
                scope_type  = enrollment.scope_type,
                scope_uuid  = enrollment.scope_uuid,
                role        = enrollment.role,
                user        = user,
            )
        except cls.DoesNotExist:
            role_assignment = cls(
                scope_type        = enrollment.scope_type,
                scope_uuid        = enrollment.scope_uuid,
                role              = enrollment.role,
                user              = user,
                assignment_method = assignment_methods.get(type(enrollment), cls.AssignmentMethod.MANUAL),
                start_date        = now(),
            )

        if enrollment.end_date is not None:
            role_assignment.end_date = enrollment.end_date
        elif enrollment.duration_period and enrollment.duration_value:
            role_assignment.end_date = enrollment.add_duration_to(now())

        role_assignment.save()
        return role_assignment

    @classmethod
    def withdraw(
        cls,
        enrollment:"EnrollmentMethod|AccessRequest",
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
