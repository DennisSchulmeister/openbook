# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filters                    import CharFilter
from rest_framework.permissions                import IsAuthenticated
from rest_framework.viewsets                   import ModelViewSet

from openbook.drf                              import ModelViewSetMixin
from openbook.core.filters.mixins.active       import ActiveInactiveFilterMixin
from openbook.core.filters.mixins.datetime     import ValidityTimeSpanFilterMixin
from openbook.core.serializers.mixins.active   import ActiveInactiveSerializerMixin
from openbook.core.serializers.mixins.datetime import ValidityTimeSpanSerializerMixin
from openbook.core.serializers.mixins.uuid     import UUIDSerializerMixin

from ..filters.mixins.audit                    import CreatedModifiedByFilterMixin
from ..filters.mixins.scope                    import ScopeFilterMixin
from ..models.role_assignment                  import RoleAssignment
from ..serializers.enrollment_method           import EnrollmentMethodReadField
from ..serializers.mixins.audit                import CreatedModifiedBySerializerMixin
from ..serializers.mixins.scope                import ScopeSerializerMixin
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
    Reduced list of fields for filtering a list of role assignments.
    """
    user = UserReadField(read_only=True)

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
    Full list of fields for retrieving a single role assignments.
    """
    role              = RoleReadField(read_only=True)
    user              = UserReadField(read_only=True)
    user_username     = UserWriteField(write_only=True)
    enrollment_method = EnrollmentMethodReadField(read_only=True)
    access_request    = AccessRequestReadField(read_only=True)

    class Meta:
        model  = RoleAssignment
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            "role", "user", "user_username",
            "assignment_method", "enrollment_method", "access_request",
            *ActiveInactiveSerializerMixin.Meta.fields,
            *ValidityTimeSpanSerializerMixin.Meta.fields,
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )

        read_only_fields = (
            *UUIDSerializerMixin.Meta.read_only_fields,
            *ScopeSerializerMixin.Meta.read_only_fields,
            *ActiveInactiveSerializerMixin.Meta.read_only_fields,
            *ValidityTimeSpanSerializerMixin.Meta.read_only_fields,
            *CreatedModifiedBySerializerMixin.Meta.read_only_fields,
        )

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
            "role": ("exact"),
            "user": ("exact"),
            **ActiveInactiveFilterMixin.Meta.fields,
            **CreatedModifiedByFilterMixin.Meta.fields,
        }

    def role_filter(self, queryset, name, value):
        return queryset.filter(role__slug=value)

    def user_filter(self, queryset, name, value):
        return queryset.filter(user__username=value)

# TODO: Should access be restricted?
class RoleAssignmentViewSet(ModelViewSetMixin, ModelViewSet):
    __doc__ = "Users and their roles in a scope"

    queryset           = RoleAssignment.objects.all()
    permission_classes = (IsAuthenticated, *ModelViewSetMixin.permission_classes)
    filterset_class    = RoleAssignmentFilter
    search_fields      = ("user__username", "role__name", "role__description")

    def get_serializer_class(self):
        if self.action == "list":
            return RoleAssignmentListSerializer
        else:
            return RoleAssignmentSerializer

    def create(self, validated_data):
        validated_data["user"] = validated_data.pop("user_username", None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.pop("user_username", instance.user)
        return super().update(instance, validated_data)
    
    # TODO: Action enroll

    # TODO: Action withdraw