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
from ..models.user              import User

class UserReadSerializer(ModelSerializer):
    """
    Serializer for user objects.
    """
    __doc__ = "User"

    display_name    = SerializerMethodField()
    profile_picture = SerializerMethodField()
    description     = SerializerMethodField()

    class Meta:
        model    = User
        fields   = ("username", "display_name", "first_name", "last_name", "is_staff", "profile_picture", "description")
        filterset_fields = ("first_name", "last_name", "is_staff")
    
    @extend_schema_field(str)
    def get_display_name(self, obj):
        """
        Formatted name.
        """
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        else:
            return obj.username
    
    @extend_schema_field(str)
    def get_profile_picture(self, obj):
        """
        URL for profile picture
        """
        try:
            return obj.profile.picture.url if obj.profile else ""
        except ValueError:
            return ""

    def get_description(self, obj):
        """
        Description from user profile
        """
        return obj.profile.description if obj.profile else ""

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

@extend_schema_field(ListSerializer(child=UserReadSerializer()))
class UserListReadField(ListField):
    """
    Serializer field for reading multiple users.
    """
    def __init__(self, **kwargs):
        self.child = UserReadField()
        super().__init__(**kwargs)

    def to_representation(self, value):
        return [self.child.to_representation(item) for item in value.all()]

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

@extend_schema_field({
    "type": "array",
    "items": {"type": "string"},
    "description": "List of user names"
})
class UserWriteListField(ListField):
    """
    Serializer field for writing multiple users.
    """
    def __init__(self, **kwargs):
        self.child = UserWriteField()
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise ValidationError(_("Invalid format: Expected a list of username strings."))

        return [self.child.to_internal_value(item) for item in data]
