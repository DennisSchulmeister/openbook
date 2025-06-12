# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filters        import CharFilter
from django_filters.filterset      import FilterSet
from drf_spectacular.utils         import extend_schema
from rest_framework.serializers    import ModelSerializer
from rest_framework.viewsets       import ModelViewSet

from openbook.drf.flex_serializers import FlexFieldsModelSerializer
from openbook.drf.viewsets         import ModelViewSetMixin
from openbook.drf.viewsets         import with_flex_fields_parameters
from ..filters.mixins.audit        import CreatedModifiedByFilterMixin
from ..models.auth_token           import AuthToken
from ..serializers.user            import UserField

class AuthTokenSerializer(FlexFieldsModelSerializer):
    __doc__ = "Authentication Token"

    user        = UserField()
    created_by  = UserField(read_only=True)
    modified_by = UserField(read_only=True)

    class Meta:
        model = AuthToken

        fields = (
            "id", "user", "token",
            "name", "description", "text_format",
            "is_active", "start_date", "end_date",
            "created_by", "created_at", "modified_by", "modified_at",
        )

        read_only_fields = ("id", "token", "created_at", "modified_at")

        expandable_fields = {
            "user":        "openbook.auth.viewsets.user.UserSerializer",
            "created_by":  "openbook.auth.viewsets.user.UserSerializer",
            "modified_by": "openbook.auth.viewsets.user.UserSerializer",
        }

class AuthTokenUpdateSerializer(ModelSerializer):
    """
    Special serializer to prevent updating the user and token string.
    """
    __doc__ = "Authentication Token"

    user = UserField(read_only=True)

    class Meta:
        model = AuthToken

        fields = (
            "id", "user",
            "name", "description", "text_format",
            "is_active", "start_date", "end_date",
        )

class AuthTokenFilter(CreatedModifiedByFilterMixin, FilterSet):
    user = CharFilter(method="user_filter")

    class Meta:
        model  = AuthToken
        fields = {
            "user":       (),
            "is_active":  ("exact",),
            "start_date": ("exact", "lte", "gte"),
            "end_date":   ("exact", "lte", "gte"),
            **CreatedModifiedByFilterMixin.Meta.fields,
        }

    def user_filter(self, queryset, name, value):
        return queryset.filter(user__username=value)

@extend_schema(
    extensions={
        "x-app-name":   "User Management",
        "x-model-name": "Authentication Tokens",
    }
)
@with_flex_fields_parameters()
class AuthTokenViewSet(ModelViewSetMixin, ModelViewSet):
    """
    Authentication tokens provide an authentication mechanism for remote clients without giving them
    a username and password. This allows human users to grant access (in their name) to other apps,
    though the apps then impersonate these human users. Thus, more importantly this allows to create
    special technical app users for which the access token is the only allowed authentication mechanism.
    """
    queryset        = AuthToken.objects.all()
    filterset_class = AuthTokenFilter
    ordering        = ("user__username", "token")
    search_fields   = ("user__username", "token", "name", "description")

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return AuthTokenUpdateSerializer
        else:
            return AuthTokenSerializer