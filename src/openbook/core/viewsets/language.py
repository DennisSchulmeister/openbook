# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from ..models.language          import Language

from django.utils.translation   import gettext_lazy as _
from rest_framework.viewsets    import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import ModelSerializer

class LanguageSerializer(ModelSerializer):
    class Meta:
        model  = Language
        fields = ["language", "name"]

class LanguageViewSet(ReadOnlyModelViewSet):
    ___doc__ = _("Available Languages")

    queryset           = Language.objects.all()
    serializer_class   = LanguageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields   = LanguageSerializer.Meta.fields
    search_fields      = ["language", "name"]