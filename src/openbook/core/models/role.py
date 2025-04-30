# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                import models
from django.utils.translation import gettext_lazy as _

from ..utils.models           import UUIDMixin
from ..utils.models           import CreatedModifiedByMixin
from ..utils.models           import NonUniqueSlugMixin
from ..utils.models           import NameDescriptionMixin

class Role(models.Model, UUIDMixin, CreatedModifiedByMixin, NonUniqueSlugMixin, NameDescriptionMixin):
    """
    """
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="roles")
    
    class Meta:
        verbose_name        = _("Role")
        verbose_name_plural = _("Roles")

        constraints = [
            models.UniqueConstraint(fields=["course", "slug"], name="unique_course_slug")
        ]
