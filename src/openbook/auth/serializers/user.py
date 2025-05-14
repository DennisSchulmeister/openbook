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
from rest_framework.serializers import SerializerMethodField

from openbook.drf               import ModelSerializer
from ..models.user              import User

class UserReadSerializer(ModelSerializer):
    """
    Serializer for user objects.
    """
    __doc__ = "User"

    display_name = SerializerMethodField()

    class Meta:
        model    = User
        fields   = ("username", "display_name", "first_name", "last_name", "is_staff")
        filterset_fields = ("username", "first_name", "last_name", "is_staff")
    
    @extend_schema_field(str)
    def get_display_name(self, obj):
        """
        Formatted name.
        """
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        else:
            return obj.username

@extend_schema_field(UserReadSerializer)
class UserReadField(Field):
    """
    Serializer field for reading a user. Use this to output a nice structure with user
    data in your response.
    """
    def to_internal_value(self, data):
        raise RuntimeError("UserReadField to write data. Use UserWriteField, instead.")

    def to_representation(self, obj):
        return UserReadSerializer(obj).data

@extend_schema_field({"description": "Users"})
class UserListReadField(ListField):
    """
    Serializer field for reading multiple users.
    """
    child = UserReadField()

@extend_schema_field({"type": "string", "description": "User name"})
class UserWriteField(Field):
    """
    Serializer field for writing users. Use this to accept a username in the request that
    will be looked up in the database.
    """
    default_error_messages = {
        "not_found": _("User '{value}' not found."),
        "invalid":   _("Invalid format: Expected a username string.")
    }

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail("invalid")

        try:
            return User.objects.get(username=data)
        except User.DoesNotExist:
            self.fail("not_found", value=data)
    
    def to_representation(self, obj):
        raise RuntimeError("UserWriteField used to deserialize data. Use UserReadField, instead.")

@extend_schema_field({"description": "User names"})
class UserWriteListField(ListField):
    """
    Serializer field for writing multiple users.
    """
    child = UserWriteField()
