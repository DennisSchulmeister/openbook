# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation   import gettext_lazy as _
from drf_spectacular.utils      import extend_schema_field
from rest_framework.serializers import Field
from rest_framework.serializers import ListField
from rest_framework.serializers import ListSerializer
from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import ValidationError

from openbook.drf               import ModelSerializer
from ..models.enrollment_method import EnrollmentMethod