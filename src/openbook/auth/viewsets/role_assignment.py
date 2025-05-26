# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from drf_spectacular.utils                     import extend_schema
from django_filters.filters                    import CharFilter
from rest_framework.serializers                import CharField
from rest_framework.viewsets                   import ModelViewSet

from openbook.drf                              import ModelViewSetMixin
from openbook.core.filters.mixins.active       import ActiveInactiveFilterMixin
from openbook.core.filters.mixins.datetime     import ValidityTimeSpanFilterMixin
from openbook.core.serializers.mixins.active   import ActiveInactiveSerializerMixin
from openbook.core.serializers.mixins.datetime import ValidityTimeSpanSerializerMixin
from openbook.core.serializers.mixins.uuid     import UUIDSerializerMixin

from ..filters.mixins.audit                    import CreatedModifiedByFilterMixin
from ..filters.mixins.scope                    import ScopeFilterMixin
from ..models.role                             import Role
from ..models.role_assignment                  import RoleAssignment
from ..serializers.access_request              import AccessRequestWithoutRoleReadField
from ..serializers.enrollment_method           import EnrollmentMethodWithoutRoleReadField
from ..serializers.mixins.audit                import CreatedModifiedBySerializerMixin
from ..serializers.mixins.scope                import ScopeSerializerMixin
from ..serializers.role                        import RoleReadField
from ..serializers.user                        import UserReadField
from ..serializers.user                        import UserWriteField

class RoleAssignmentListSerializer(
    UUIDSerializerMixin,
    ScopeSerializerMixin,
    ActiveInactiveSerializerMixin,
    ValidityTimeSpanSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Reduced list of fields for getting a list of role assignments.
    """
    user = UserReadField(read_only=True)
    role = RoleReadField(read_only=True)

    class Meta:
        model = RoleAssignment
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            "role", "user",
            *ActiveInactiveSerializerMixin.Meta.fields,
            *ValidityTimeSpanSerializerMixin.Meta.fields,
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )
        read_only_fields = fields

class RoleAssignmentSerializer(
    UUIDSerializerMixin,
    ScopeSerializerMixin,
    ActiveInactiveSerializerMixin,
    ValidityTimeSpanSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Full list of fields for retrieving a single role assignment.
    """
    role              = RoleReadField(read_only=True)
    role_slug         = CharField(write_only=True)
    user              = UserReadField(read_only=True)
    user_username     = UserWriteField(write_only=True, source="user")
    enrollment_method = EnrollmentMethodWithoutRoleReadField(read_only=True)
    access_request    = AccessRequestWithoutRoleReadField(read_only=True)

    class Meta:
        model  = RoleAssignment
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            "role", "role_slug",
            "user", "user_username",
            "assignment_method", "enrollment_method", "access_request",
            *ActiveInactiveSerializerMixin.Meta.fields,
            *ValidityTimeSpanSerializerMixin.Meta.fields,
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )

        read_only_fields = (
            *UUIDSerializerMixin.Meta.read_only_fields,
            *ScopeSerializerMixin.Meta.read_only_fields,
            "assignment_method",
            *ActiveInactiveSerializerMixin.Meta.read_only_fields,
            *ValidityTimeSpanSerializerMixin.Meta.read_only_fields,
            *CreatedModifiedBySerializerMixin.Meta.read_only_fields,
        )

    def validate(self, attributes):        
        if "scope_type"  in attributes \
        and "scope_uuid" in attributes \
        and "role_slug"  in attributes:
            attributes["role"] = Role.objects.get(
                scope_type = attributes["scope_type"],
                scope_uuid = attributes["scope_uuid"],
                slug       = attributes.pop("role_slug"),
            )

        return attributes

class RoleAssignmentFilter(
    ScopeFilterMixin,
    ValidityTimeSpanFilterMixin,
    ActiveInactiveFilterMixin,
    CreatedModifiedByFilterMixin
):
    role = CharFilter(method="role_filter")
    user = CharFilter(method="user_filter")

    class Meta:
        model  = RoleAssignment
        fields = {
            **ScopeFilterMixin.Meta.fields,
            **ValidityTimeSpanFilterMixin.Meta.fields,
            "role": (),
            "user": (),
            **ActiveInactiveFilterMixin.Meta.fields,
            **CreatedModifiedByFilterMixin.Meta.fields,
        }

    def role_filter(self, queryset, name, value):
        return queryset.filter(role__slug=value)

    def user_filter(self, queryset, name, value):
        return queryset.filter(user__username=value)

@extend_schema(
    extensions={
        "x-app-name":   "User Management",
        "x-model-name": "Role Assignments",
    }
)
class RoleAssignmentViewSet(ModelViewSetMixin, ModelViewSet):
    __doc__ = "Users and their roles in a scope"

    queryset        = RoleAssignment.objects.all()
    filterset_class = RoleAssignmentFilter
    ordering        = ("scope_type", "scope_uuid", "user__username", "role__slug")
    search_fields   = (
        "user__username", "user__first_name", "user__last_name", "user__email",
        "role__slug", "role__name", "role__description"
    )

    def get_serializer_class(self):
        if self.action == "list":
            return RoleAssignmentListSerializer
        else:
            return RoleAssignmentSerializer
