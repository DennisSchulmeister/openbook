# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from drf_spectacular.utils      import extend_schema
from django.contrib.auth.models import Permission
from django_filters.filterset   import FilterSet
from django_filters.filters     import CharFilter
from rest_framework.viewsets    import ModelViewSet
from rest_framework.serializers import ModelSerializer

from openbook.drf               import ModelViewSetMixin
from ..models.permission        import Permission_T
from ..serializers.permission   import PermissionReadField
from ..serializers.permission   import PermissionWriteField
from ..utils                    import permission_for_perm_string

class PermissionTSerializer(ModelSerializer):
    permission = PermissionReadField(read_only=True, source="parent")
    permission_string = PermissionWriteField(write_only=True, source="parent")

    class Meta:
        model  = Permission_T
        fields = ("permission", "permission_string", "language", "name")

class PermissionTFilter(FilterSet):
    perm_string = CharFilter(label="Permission String", method="filter_perm_string")
    app         = CharFilter(label="App",   field_name="parent__content_type__app_label", lookup_expr="icontains")
    model       = CharFilter(label="Model", field_name="parent__content_type__model",     lookup_expr="icontains")
    codename    = CharFilter(label="Code",  field_name="parent__codename",                lookup_expr="icontains")
    name        = CharFilter(lookup_expr="icontains")

    class Meta:
        model  = Permission_T
        fields = ("app", "model", "codename", "language", "name")
    
    def filter_perm_string(self, queryset, name, value):
        try:
            permission = permission_for_perm_string(value)
        except Permission.DoesNotExist:
            permission = None

        return queryset.filter(parent=permission) if permission else queryset.none()

@extend_schema(
    extensions={
        "x-app-name":   "User Management",
        "x-model-name": "Translated Permissions",
    }
)
class PermissionTViewSet(ModelViewSetMixin, ModelViewSet):
    """
    Read/write view set to query active users. The serializer makes sure that only
    basic information is returned. Authenticated users only as we don't want the
    world to scrap our user list.
    """
    __doc__ = "User Profiles"

    queryset         = Permission_T.objects.all()
    filterset_class  = PermissionTFilter
    serializer_class = PermissionTSerializer
    ordering         = ("parent__content_type__app_label", "parent__codename", "language__language")
    search_fields    = (
        "parent__content_type__app_label", "parent__codename",
        "language__language", "language__name",
        "name",
    )