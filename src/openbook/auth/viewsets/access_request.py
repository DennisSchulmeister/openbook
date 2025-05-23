# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filters                    import CharFilter
from drf_spectacular.utils                     import extend_schema
from rest_framework.decorators                 import action
from rest_framework.serializers                import CharField
from rest_framework.viewsets                   import ModelViewSet

from openbook.drf                              import ModelViewSetMixin
from openbook.core.serializers.mixins.datetime import DurationSerializerMixin
from openbook.core.serializers.mixins.uuid     import UUIDSerializerMixin

from ..filters.mixins.audit                    import CreatedModifiedByFilterMixin
from ..filters.mixins.scope                    import ScopeFilterMixin
from ..models.access_request                   import AccessRequest
from ..models.role                             import Role
from ..serializers.mixins.audit                import CreatedModifiedBySerializerMixin
from ..serializers.mixins.scope                import ScopeSerializerMixin
from ..serializers.role                        import RoleReadField
from ..serializers.user                        import UserReadField
from ..serializers.user                        import UserWriteField

class AccessRequestListSerializer(
    UUIDSerializerMixin,
    ScopeSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Reduced list of fields for getting a list of access request.
    """
    user = UserReadField(read_only=True)
    role = RoleReadField(read_only=True)

    class Meta:
        model = AccessRequest
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            "role", "user",
            "decision", "decision_date",
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )
        read_only_fields = fields

class AccessRequestSerializer(
    UUIDSerializerMixin,
    ScopeSerializerMixin,
    DurationSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Full list of fields for retrieving a single access request.
    """
    role          = RoleReadField(read_only=True)
    role_slug     = CharField(write_only=True)
    user          = UserReadField(read_only=True)
    user_username = UserWriteField(write_only=True, source="user")

    class Meta:
        model  = AccessRequest
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            "role", "role_slug",
            "user", "user_username",
            "end_date",
            *DurationSerializerMixin.Meta.fields,
            "decision", "decision_date",
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )

        read_only_fields = (
            *UUIDSerializerMixin.Meta.read_only_fields,
            *ScopeSerializerMixin.Meta.read_only_fields,
            *DurationSerializerMixin.Meta.read_only_fields,
            "decision_date",
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

class AccessRequestFilter(
    ScopeFilterMixin,
    CreatedModifiedByFilterMixin
):
    role = CharFilter(method="role_filter")
    user = CharFilter(method="user_filter")

    class Meta:
        model  = AccessRequest
        fields = {
            **ScopeFilterMixin.Meta.fields,
            "role":          (),
            "user":          (),
            "decision":      ("exact",),
            "decision_date": ("exact", "lte", "gte"),
            **CreatedModifiedByFilterMixin.Meta.fields,
        }

    def role_filter(self, queryset, name, value):
        return queryset.filter(role__slug=value)

    def user_filter(self, queryset, name, value):
        return queryset.filter(user__username=value)

@extend_schema(
    extensions={
        "x-app-name":   "User Management",
        "x-model-name": "Access Requests",
    }
)
class AccessRequestViewSet(ModelViewSetMixin, ModelViewSet):
    __doc__ = "Access requests to get a scoped role assigned"

    queryset        = AccessRequest.objects.all()
    filterset_class = AccessRequestFilter
    search_fields   = ("user__username", "role__name", "role__description")

    def get_serializer_class(self):
        if self.action == "list":
            return AccessRequestListSerializer
        else:
            return AccessRequestSerializer

    @extend_schema(
        operation_id = "auth_access_requests_accept",
        request      = None,
        responses    = AccessRequestSerializer,
        summary      = "Accept",
    )
    @action(methods=["post"], detail=True)
    def accept(self, request, pk):
        """
        Accept request.
        """
        access_request = self.get_object()
        access_request.accept()
        return Response(AccessRequestSerializer(instance=access_request).data)

    @extend_schema(
        operation_id = "auth_access_requests_deny",
        request      = None, 
        responses    = AccessRequestSerializer,
        summary      = "Deny",
    )
    @action(methods=["post"], detail=True)
    def deny(self, request, pk):
        """
        Deny request.
        """
        access_request = self.get_object()
        access_request.deny()
        return Response(AccessRequestSerializer(instance=access_request).data)
