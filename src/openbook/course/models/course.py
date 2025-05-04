# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db                import models
from django.utils.translation import gettext_lazy as _

# from ..utils.models           import UUIDMixin
# from ..utils.models           import CreatedModifiedByMixin
# from ..utils.models           import NonUniqueSlugMixin
# from ..utils.models           import NameDescriptionMixin
# 
# class Course(models.Model, UUIDMixin, CreatedModifiedByMixin, NonUniqueSlugMixin, NameDescriptionMixin):
#     """
#     """
#     organizations = models.ManyToManyField("Organization")
#     is_template   = models.BooleanField(verbose_name=_("Is Template"), help=_("Flag indicating that this course is not used productively but rather is a template for creating similar courses."))
#     # Owner
#     # Default role
#     # Course image
# 
#     class Meta():
#         verbose_name        = _("Course")
#         verbose_name_plural = _("Courses")
# 
# # Course user roles