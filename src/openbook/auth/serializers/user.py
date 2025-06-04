# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from drf_spectacular.utils      import extend_schema_field
from rest_flex_fields           import FlexFieldsModelSerializer
from rest_framework.serializers import SerializerMethodField

from ..models.user              import User
from ..models.user_profile      import UserProfile

class UserProfileSerializer(FlexFieldsModelSerializer):
    __doc__ = "User Profile"

    class Meta:
        model  = UserProfile
        fields = ("user", "description", "picture")

class UserSerializer(FlexFieldsModelSerializer):
    __doc__ = "User"

    full_name = SerializerMethodField()

    class Meta:
        model    = User
        fields   = ("username", "full_name", "first_name", "last_name", "profile")
        filterset_fields = ("first_name", "last_name", "is_staff")
        expandable_fields = {"profile": UserProfileSerializer}
    
    @extend_schema_field(str)
    def get_full_name(self, obj):
        return obj.get_full_name() if hasattr(obj, "get_full_name") else ""
    