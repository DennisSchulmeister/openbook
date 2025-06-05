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

from ..models.user              import User

@extend_schema_field(str)
class UserField(Field):
    """
    Serializer field to use the username for input and output instead of a user's raw PK.
    """
    default_error_messages = {
        "not_found": _("User '{value}' not found."),
        "invalid":   _("Invalid format: Expected a username string."),
        "required":  _("Username is required"),
    }

    def to_internal_value(self, data):
        if data is None:
            if self.required:
                self.fail("required")
            else:
                return None
            
        if not isinstance(data, str):
            self.fail("invalid")

        try:
            return User.objects.get(username=data)
        except User.DoesNotExist:
            self.fail("not_found", value=data)

    def to_representation(self, obj):
        return obj.username