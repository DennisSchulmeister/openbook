# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from openbook.drf import ModelSerializer

class UUIDSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose models implement the `UUIDMixin` and therefor
    have a `id` field of type uuid.
    """
    class Meta:
        fields = ("id",)
        read_only_fields = ("id",)
