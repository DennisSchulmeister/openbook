# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models           import AbstractUser
from django.db                            import models
from django.utils.translation             import gettext_lazy as _

from openbook.core.models.mixins.active   import ActiveInactiveMixin
from openbook.core.models.mixins.datetime import DurationMixin
from openbook.core.models.mixins.text     import NameDescriptionMixin
from openbook.core.models.mixins.uuid     import UUIDMixin

from .mixins.audit                        import CreatedModifiedByMixin
from .mixins.auth                         import ScopeMixin

class EnrollmentMethod(UUIDMixin, ScopeMixin, NameDescriptionMixin, ActiveInactiveMixin, DurationMixin, CreatedModifiedByMixin):
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
            models.Index(fields=["scope_type", "scope_uuid", "role"]),
        ]
    
    def __str__(self):
        return f"{self.name} {ActiveInactiveMixin.__str__(self)}".strip()

    def has_obj_perm(self, user_obj: AbstractUser, perm: str) -> bool:
        """
        A user can only add/change/delete enrollment methods with lower or equal priority to his/her own roles.

        **Caveat:** Take care to not reveal the passphrase when enrollment methods are queried or viewed.
        """
        principally_allowed = super().has_obj_perm(user_obj, perm)

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
        from .role_assignment import RoleAssignment
        RoleAssignment.enroll(enrollment=self, user=user, passphrase=passphrase, check_passphrase=check_passphrase)