# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework.serializers import ModelSerializer

class SlugSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose models implement one of the slug mixins
    and therefor have a `slug` field.
    """
    class Meta:
        fields = ("slug",)
        read_only_fields = ()
