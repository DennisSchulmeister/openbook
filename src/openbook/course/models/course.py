# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                   import models
from django.utils.translation    import gettext_lazy as _

from openbook.auth.models.mixins import CreatedModifiedByMixin
from openbook.auth.models.mixins import ScopedRolesMixin
from openbook.core.models.mixins import UUIDMixin
from openbook.core.models.mixins import NonUniqueSlugMixin
from openbook.core.models.mixins import NameDescriptionMixin

class Course(UUIDMixin, NonUniqueSlugMixin, NameDescriptionMixin, ScopedRolesMixin, CreatedModifiedByMixin):
    """
    Courses support the teachers in the execution of the teaching by bringing together teachers,
    students, textbooks and other one-off materials.
    """
    # License (via new model in core)
    # Image
    # AI Notes (new mixin)
    # Learning Target Taxonomy
    # Activity Taxonomy
    is_template = models.BooleanField(
        verbose_name = _("Is Template"),
        help_text    = _("Flag indicating that this course is not used productively but rather is a template for creating similar courses."),
        default      = False,
    )

    class Meta():
        verbose_name        = _("Course")
        verbose_name_plural = _("Courses")