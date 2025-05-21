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
from rest_framework.serializers import ImageField
from rest_framework.serializers import ListField
from rest_framework.serializers import ListSerializer
from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import ValidationError

from openbook.core.validators   import ValidateImage
from openbook.drf               import ModelSerializer
from ..models.user              import User

class UserReadSerializer(ModelSerializer):
    """
    Serializer for user objects for embedding in other serializers via the `UserReadField`.
    Returns enough information to display a list of users but not necessarily all profile data.
    """
    __doc__ = "User (Reduced Data)"

    full_name       = SerializerMethodField()
    profile_picture = SerializerMethodField()

    class Meta:
        model    = User
        fields   = ("username", "full_name", "first_name", "last_name", "is_staff", "is_superuser", "profile_picture")
        filterset_fields = ("first_name", "last_name", "is_staff")
    
    @extend_schema_field(str)
    def get_full_name(self, obj):
        return obj.get_full_name() if hasattr(obj, "get_full_name") else ""
    
    @extend_schema_field(str)
    def get_profile_picture(self, obj):
        """
        URL for profile picture
        """
        try:
            return obj.profile.picture.url if hasattr(obj, "profile") and obj.profile else ""
        except ValueError:
            return ""

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

class UserDetailsReadSerializer(UserReadSerializer):
    """
    Serializer for full user details including all profile data. Not meant for embedding
    in lists but rather for retrieving a single user profile.

    Note: The email is deliberately missing to keep it private. It is only returned by
    the endpoint to query the currently logged in user.
    """
    __doc__ = "User (Full Profile)"

    description = SerializerMethodField()

    class Meta:
        model    = User
        fields   = (*UserReadSerializer.Meta.fields, "description")
        filterset_fields = (*UserReadSerializer.Meta.filterset_fields,)

    def get_description(self, obj):
        """
        Description from user profile
        """
        return obj.profile.description if hasattr(obj, "profile") and obj.profile else ""

class UserDetailsUpdateSerializer(ModelSerializer):
    """
    Serializer for updating own profile information.
    """
    __doc__ = "Update user profile"

    profile_picture = ImageField(required=False, validators=[ValidateImage()])

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "profile_picture", "description")
