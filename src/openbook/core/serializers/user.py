# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework import serializers
from ..             import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.User
        fields = ["username", "first_name", "last_name", "is_staff"]