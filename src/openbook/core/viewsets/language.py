# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filters     import CharFilter
from django_filters.filterset   import FilterSet
from drf_spectacular.utils      import extend_schema
from rest_framework.viewsets    import ReadOnlyModelViewSet
from rest_framework.serializers import ModelSerializer

from openbook.drf               import AllowAnonymousListViewSetMixin
from ..models.language          import Language

class LanguageSerializer(ModelSerializer):
    class Meta:
        model  = Language
        fields = ("language", "name")

class LanguageFilter(FilterSet):
    name = CharFilter(lookup_expr="icontains")

    class Meta:
        model  = Language
        fields = ("name",)

@extend_schema(
    extensions={
        "x-app-name":   "OpenBook Server",
        "x-model-name": "Available Languages",
    }
)
class LanguageViewSet(AllowAnonymousListViewSetMixin, ReadOnlyModelViewSet):
    ___doc__ = "Available Languages"

    queryset           = Language.objects.all()
    serializer_class   = LanguageSerializer
    filterset_class    = LanguageFilter
    ordering           = ("language",)
    search_fields      = ("language", "name")