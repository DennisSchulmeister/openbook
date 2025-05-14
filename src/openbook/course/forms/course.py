# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation        import gettext_lazy as _
from openbook.auth.forms.mixins.auth import ScopedRolesFormMixin
from ..models.course                 import Course

class CourseForm(ScopedRolesFormMixin):
    class Meta:
        model  = Course
        fields = "__all__"
