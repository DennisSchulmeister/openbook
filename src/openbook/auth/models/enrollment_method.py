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
from typing                               import TYPE_CHECKING

from openbook.core.models.mixins.active   import ActiveInactiveMixin
from openbook.core.models.mixins.datetime import DurationMixin
from openbook.core.models.mixins.text     import NameDescriptionMixin
from openbook.core.models.mixins.uuid     import UUIDMixin

from .mixins.audit                        import CreatedModifiedByMixin
from .mixins.scope                        import ScopeMixin

if TYPE_CHECKING:
    from .role_assignment import RoleAssignment

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
            models.Index(fields=("scope_type", "scope_uuid", "role",)),
        ]
    
    def __str__(self):
        return f"{self.name} {ActiveInactiveMixin.__str__(self)}".strip()

    def enroll(self,
        user: AbstractUser,
        passphrase: str = None,
        check_passphrase: bool = True,
    ) -> "RoleAssignment":
        """
        Enroll the given user, optionally checking the passphrase. Raises a `ValueError` when
        the passphrase doesn't match.
        """
        from .role_assignment import RoleAssignment

        return RoleAssignment.enroll(
            enrollment       = self,
            user             = user,
            passphrase       = passphrase,
            check_passphrase = check_passphrase,
            check_permission = False,    # Cannot check permission before user is enrolled
        )