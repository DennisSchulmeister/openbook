# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers         import ModelSerializer

from openbook.auth.validators           import validate_permissions
from ..user                             import UserReadField
from ..user                             import UserWriteField
from ..permission                       import PermissionListReadField
from ..permission                       import PermissionListWriteField

class ScopedRolesListSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose model implement the `ScopedRolesMixin` and as such
    act as permission scope for user roles. List serializer, which only adds the `owner` field.
    """
    owner = UserReadField(read_only=True)

    class Meta:
        fields = ("owner",)

class ScopedRolesSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose model implement the `ScopedRolesMixin` and as such
    act as permission scope for user roles. Default serializer, that adds all scope fields.
    """
    owner                     = UserReadField(read_only=True)
    owner_username            = UserWriteField(write_only=True)
    public_permissions        = PermissionListReadField(read_only=True)
    public_permission_strings = PermissionListWriteField(write_only=True)

    class Meta:
        fields = (
            "owner", "owner_username",
            "public_permissions", "public_permission_strings",
        )

        read_only_fields = ()

    def validate(self, attributes):
        """
        Check that only allowed permissions are assigned.
        """
        scope_type = ContentType.objects.get_for_model(self.Meta.model)
        public_permissions = attributes.get("public_permissions", None)

        validate_permissions(scope_type, public_permissions)
        return attributes