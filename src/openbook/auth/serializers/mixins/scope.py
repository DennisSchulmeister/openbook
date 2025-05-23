# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation           import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils              import extend_schema_field
from rest_framework.serializers         import Field
from rest_framework.serializers         import ListField
from rest_framework.serializers         import ListSerializer
from rest_framework.serializers         import ModelSerializer
from rest_framework.serializers         import ValidationError

from ..access_request                   import AccessRequestWithRoleReadField
from ..enrollment_method                import EnrollmentMethodWithRoleReadField
from ..user                             import UserReadField
from ..user                             import UserWriteField
from ..permission                       import PermissionReadField
from ..permission                       import PermissionWriteField
from ..role_assignment                  import RoleAssignmentReadField
from ...utils                           import content_type_for_model_string
from ...utils                           import model_string_for_content_type
from ...validators                      import validate_scope_type
from ...validators                      import validate_permissions

class ScopedRolesListSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose models implement the `ScopedRolesMixin` and as such
    act as permission scope for user roles. List serializer, which only adds the `owner` field.
    """
    owner = UserReadField(read_only=True)

    class Meta:
        fields = ("owner",)

class ScopedRolesSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose models implement the `ScopedRolesMixin` and as such
    act as permission scope for user roles. Default serializer, that adds all scope fields.
    """
    owner                     = UserReadField(read_only=True)
    owner_username            = UserWriteField(write_only=True, source="owner")
    public_permissions        = ListField(child=PermissionReadField(), read_only=True)
    public_permission_strings = ListField(child=PermissionWriteField(), write_only=True, source="public_permissions")
    role_assignments          = ListField(child=RoleAssignmentReadField(), read_only=True)
    enrollment_methods        = ListField(child=EnrollmentMethodWithRoleReadField(), read_only=True)
    access_requests           = ListField(child=AccessRequestWithRoleReadField(), read_only=True)

    class Meta:
        fields = (
            "owner", "owner_username",
            "public_permissions", "public_permission_strings",
            "role_assignments", "enrollment_methods", "access_requests",
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

@extend_schema_field(str)
class ScopeTypeField(Field):
    """
    Serializer field for the scope_type. Uses the fully-qualified model name instead
    of the PK for input and output.
    """
    default_error_messages = {
        "not_found": _("Scope type '{value}' not found."),
        "invalid":   _("Invalid format: Expected a scope type string.")
    }

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail("invalid")

        try:
            return content_type_for_model_string(data)
        except ContentType.DoesNotExist:
            self.fail("not_found", value=data)

    def to_representation(self, obj):
        return model_string_for_content_type(obj)
        
class ScopeSerializerMixin(ModelSerializer):
    """
    Mixin class for model serializers whose models implement the `ScopeMixin` and as such have
    the fields `scope_type` and `scope_uuid`.
    """
    scope_type = ScopeTypeField()

    class Meta:
        fields = ("scope_type", "scope_uuid")
        read_only_fields = ()
    
    def validate(self, attributes):
        """
        Check that only valid scope types are assigned, whose model class implements
        the `ScopedRolesMixin`.
        """
        scope_type = attributes.get("scope_type", None)
        validate_scope_type(scope_type)
        return attributes