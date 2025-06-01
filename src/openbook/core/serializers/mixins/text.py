# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from openbook.drf import ModelSerializer

class NameDescriptionListSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose models implement the `NameDescriptionMixin` and therefor
    have a `name` field.
    """
    class Meta:
        fields = ("name",)
        read_only_fields = ()

class NameDescriptionSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose models implement the `NameDescriptionMixin` and therefor
    the `name`, `description` and `text_format` fields.
    """
    class Meta:
        fields = ("name", "description", "text_format")
        read_only_fields = ()
