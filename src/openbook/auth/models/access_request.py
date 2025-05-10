# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from datetime                             import timezone

from django.conf                          import settings
from django.contrib.auth.models           import AbstractUser
from django.db                            import models
from django.utils.translation             import gettext_lazy as _

from openbook.core.models.mixins.datetime import DurationMixin
from openbook.core.models.mixins.uuid     import UUIDMixin

from .mixins.audit                        import CreatedModifiedByMixin
from .mixins.auth                         import ScopeMixin
from ..middleware.current_user            import get_current_user

class AccessRequest(UUIDMixin, ScopeMixin, DurationMixin, CreatedModifiedByMixin):
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
            models.Index(fields=("scope_type", "scope_uuid", "role")),
            models.Index(fields=("user",), name="user_idx"),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.role.name}"

    def has_obj_perm(self, user_obj: AbstractUser, perm: str) -> bool:
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

        return super().has_obj_perm(user_obj, perm)

    def save(self, *args, **kwargs):
        """
        Force pending decision when a new access request is saved. Also update the role assignments
        accordingly when a decision is made.
        """
        from .role_assignment import RoleAssignment
        
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