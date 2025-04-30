# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf              import settings
from django.db                import models
from django.utils.translation import gettext_lazy as _

from ..utils.models           import UUIDMixin
from ..utils.models           import CreatedModifiedByMixin
from ..utils.models           import UniqueSlugMixin
from ..utils.models           import NonUniqueSlugMixin
from ..utils.models           import NameDescriptionMixin
from ..utils.models           import ValidityTimeSpanMixin

class Organization(models.Model, UUIDMixin, CreatedModifiedByMixin, UniqueSlugMixin, NameDescriptionMixin):
    """
    """
    parent = models.ForeignKey("self", verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True, related_name="children")

    class Meta():
        verbose_name        = _("Organization")
        verbose_name_plural = _("Organizations")

class OrganizationRegistrationMethod(models.Model, UUIDMixin, CreatedModifiedByMixin, NonUniqueSlugMixin, NameDescriptionMixin, ValidityTimeSpanMixin):
    """
    Self-registration method for users to sign-up with an organization.
    """
    # TODO

    class Meta():
        verbose_name        = _("Registration Method")
        verbose_name_plural = _("Registration Methods")

class OrganizationUser(models.Model, UUIDMixin, CreatedModifiedByMixin):
    """
    A single user assigned to an organization with a given registration method.
    """
    # TODO: on_delete, null, blank, related_name
    organization        = models.ForeignKey(Organization)
    user                = models.ForeignKey(settings.AUTH_USER_MODEL)
    registration_method = models.ForeignKey(OrganizationRegistrationMethod)
    manually_assigned   = models.BooleanField(verbose_name=_("Manually Assigned"), help=_("Flag indicating that the user was manually assigned by an organization administrator."))

    class Meta():
        verbose_name        = _("Assigned User")
        verbose_name_plural = _("Assigned Users")