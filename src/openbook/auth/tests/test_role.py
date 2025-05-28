# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions        import ValidationError
from django.db.utils               import IntegrityError
from django.urls                   import reverse
from django.test                   import TestCase
from rest_framework.test           import APIClient

from openbook.course.models.course import Course
from ..middleware.current_user     import reset_current_user
from ..models.role                 import Role
from ..models.role_assignment      import RoleAssignment
from ..models.user                 import User