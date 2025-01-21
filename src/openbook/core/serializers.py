# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework import serializers
from .              import models

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.Language
        fields = "__all__"

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.MediaFile
        fields = "__all__"

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.Site
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = models.User
        fields = ["username", "first_name", "last_name", "is_staff"]