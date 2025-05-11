# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils              import extend_schema
from drf_spectacular.utils              import OpenApiParameter
from drf_spectacular.utils              import OpenApiTypes
from rest_framework.fields              import CharField
from rest_framework.fields              import UUIDField
from rest_framework.mixins              import ListModelMixin
from rest_framework.permissions         import IsAuthenticated
from rest_framework.serializers         import Serializer
from rest_framework.viewsets            import GenericViewSet

from ..models.mixins.auth               import ScopedRolesMixin

class ScopeSerializer(Serializer):
    scope_type  = CharField()
    scope_label = CharField()
    scope_uuid  = UUIDField(required=False)
    scope_name  = CharField(required=False)

class ScopeViewSet(ListModelMixin, GenericViewSet):
    """
    List of permission scopes, filterable by scope type. Returns the scope types when no
    query parameter is given and the actual scopes, when `scope_type` is sent.
    """
    permission_classes = [IsAuthenticated]
    serializer_class   = ScopeSerializer
    pagination_class   = None
    filter_backends    = []

    def get_queryset(self):
        """
        Return query set for the selected scope type.
        """
        scope_type = self.request.query_params.get("scope_type", "").lower()

        if not scope_type:
            result = []

            for content_type in ScopedRolesMixin.get_scope_model_content_types():
                result.append({
                    "scope_type":  f"{content_type.app_label}.{content_type.name}".lower(),
                    "scope_label": content_type.name,
                })

            return result
        
        try:
            try:
                content_type = ContentType.objects.get(pk=int(scope_type))
            except ValueError:
                app_label, model = scope_type.split(".", 1)
                content_type = ContentType.objects.get(app_label=app_label, model=model)
        except:
            return []

        if not ScopedRolesMixin.content_type_is_scope(content_type):
            return []
        

        query_set = content_type.get_all_objects_for_this_type().only("id", "name").order_by("name")
        result = []
        
        for scope in query_set.all():
            result.append({
                "scope_type":  f"{content_type.app_label}.{content_type.model}",
                "scope_label": content_type.name,
                "scope_uuid":  scope.id,
                "scope_name":  scope.name if hasattr(scope, "name") else scope.id,
            })
        
        return result

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name        = "scope_type",
                required    = False,
                type        = OpenApiTypes.STR,
                location    = OpenApiParameter.QUERY,
                description = "Get scopes for a scope type (if empty only the types will be returned)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
