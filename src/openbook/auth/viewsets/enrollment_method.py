# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filters                    import CharFilter
from drf_spectacular.utils                     import extend_schema
from drf_spectacular.utils                     import inline_serializer
from rest_framework.decorators                 import action
from rest_framework.serializers                import BooleanField
from rest_framework.serializers                import CharField
from rest_framework.viewsets                   import ModelViewSet

from openbook.drf                              import ModelViewSetMixin
from openbook.core.filters.mixins.active       import ActiveInactiveFilterMixin
from openbook.core.filters.mixins.text         import NameDescriptionFilterMixin
from openbook.core.serializers.mixins.active   import ActiveInactiveSerializerMixin
from openbook.core.serializers.mixins.datetime import DurationSerializerMixin
from openbook.core.serializers.mixins.text     import NameDescriptionListSerializerMixin
from openbook.core.serializers.mixins.text     import NameDescriptionSerializerMixin
from openbook.core.serializers.mixins.uuid     import UUIDSerializerMixin

from ..filters.mixins.audit                    import CreatedModifiedByFilterMixin
from ..filters.mixins.scope                    import ScopeFilterMixin
from ..models.enrollment_method                import EnrollmentMethod
from ..models.role                             import Role
from ..serializers.mixins.audit                import CreatedModifiedBySerializerMixin
from ..serializers.mixins.scope                import ScopeSerializerMixin
from ..serializers.role_assignment             import RoleAssignmentReadSerializer
from ..serializers.role                        import RoleReadField

class EnrollmentMethodListSerializer(
    UUIDSerializerMixin,
    ScopeSerializerMixin,
    NameDescriptionListSerializerMixin,
    ActiveInactiveSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Reduced list of fields for getting a list of enrollment methods.
    """
    role = RoleReadField(read_only=True)

    class Meta:
        model = EnrollmentMethod
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            "role",
            *NameDescriptionListSerializerMixin.Meta.fields,
            *ActiveInactiveSerializerMixin.Meta.fields,
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )
        read_only_fields = fields

class EnrollmentMethodSerializer(
    UUIDSerializerMixin,
    ScopeSerializerMixin,
    NameDescriptionSerializerMixin,
    ActiveInactiveSerializerMixin,
    DurationSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Full list of fields for retrieving a single enrollment method.
    """
    role      = RoleReadField(read_only=True)
    role_slug = CharField(write_only=True)

    class Meta:
        model = EnrollmentMethod
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            *NameDescriptionSerializerMixin.Meta.fields,
            "role", "role_slug",
            *ActiveInactiveSerializerMixin.Meta.fields,
            *DurationSerializerMixin.Meta.fields,
            "end_date", "passphrase",
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )

        read_only_fields = (
            *UUIDSerializerMixin.Meta.read_only_fields,
            *ScopeSerializerMixin.Meta.read_only_fields,
            *NameDescriptionSerializerMixin.Meta.read_only_fields,
            *ActiveInactiveSerializerMixin.Meta.read_only_fields,
            *DurationSerializerMixin.Meta.read_only_fields,
            *CreatedModifiedBySerializerMixin.Meta.read_only_fields,
        )

    def validate(self, attributes):        
        if "scope_type"  in attributes \
        and "scope_uuid" in attributes \
        and "role_slug"  in attributes:
            attributes["role"] = Role.objects.get(
                scope_type = attributes["scope_type"],
                scope_uuid = attributes["scope_uuid"],
                slug       = attributes["role_slug"],
            )

        return attributes

class EnrollmentMethodFilter(
    ScopeFilterMixin,
    NameDescriptionFilterMixin,
    ActiveInactiveFilterMixin,
    CreatedModifiedByFilterMixin,
):
    role = CharFilter(method="role_filter")

    class Meta:
        model  = EnrollmentMethod
        fields = {
            **ScopeFilterMixin.Meta.fields,
            "role": (),
            **NameDescriptionFilterMixin.Meta.fields,
            **ActiveInactiveFilterMixin.Meta.fields,
            **CreatedModifiedByFilterMixin.Meta.fields,
        }

    def role_filter(self, queryset, name, value):
        return queryset.filter(role__slug=value)
    
@extend_schema(
    extensions={
        "x-app-name":   "User Management",
        "x-model-name": "Enrollment Methods",
    }
)
class EnrollmentMethodViewSet(ModelViewSetMixin, ModelViewSet):
    __doc__ = "Enrollment methods for self-registration"

    queryset        = EnrollmentMethod.objects.all()
    filterset_class = EnrollmentMethodFilter
    search_fields   = ("name", "description", "role__name", "role__description")

    def get_serializer_class(self):
        if self.action == "list":
            return EnrollmentMethodListSerializer
        else:
            return EnrollmentMethodSerializer

    @extend_schema(
        operation_id = "auth_enrollment_method_enroll",
        summary      = "Enroll User",
        responses    = RoleAssignmentReadSerializer,
        request      = inline_serializer(
            name   = "EnrollActionRequestSerializer",
            fields = {
                "user_username":    CharField(required=True),
                "passphrase":       CharField(required=False),
                "check_passphrase": BooleanField(required=False, default=True),
            }
        ),
    )
    @action(detail=True, methods=["post"], url_path="enroll")
    def enroll(self, request, pk=None):
        enrollment_method = self.get_object()
        
        kwargs = {
            "user":             request.data.get("user_username"),
            "passphrase":       request.data.get("passphrase", None),
            "check_passphrase": request.data.get("check_passphrase", True),
        }

        role_assignment = enrollment_method.enroll(**kwargs)
        serializer      = RoleAssignmentReadSerializer(role_assignment)

        return Response(serializer.data)

