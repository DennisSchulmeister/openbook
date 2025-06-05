# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filters   import CharFilter
from django_filters.filterset import FilterSet
from drf_spectacular.utils    import extend_schema
from rest_flex_fields         import FlexFieldsModelSerializer
from rest_framework.viewsets  import ModelViewSet

from openbook.drf             import ModelViewSetMixin
from openbook.drf             import with_flex_fields_parameters
from ..models.file_uploads    import MediaFile

class MediaFileSerializer(FlexFieldsModelSerializer):
    __doc__ = "Media File"

    class Meta:
        model  = MediaFile
        fields = ("content_type", "object_id", "file_name", "file_size", "mime_type", "file_data")

class MediaFileFilter(FilterSet):
    file_name = CharFilter(lookup_expr="icontains")

    class Meta:
        model  = MediaFile
        fields = ("content_type", "object_id", "file_name", "file_size", "mime_type", "file_data")

@extend_schema(
    extensions={
        "x-app-name":   "OpenBook Server",
        "x-model-name": "Media Files",
    }
)
@with_flex_fields_parameters()
class MediaFileViewSet(ModelViewSetMixin, ModelViewSet):
    __doc__ = "Attached Media Files"

    queryset         = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    filterset_class  = MediaFileFilter
    ordering         = ("content_type", "object_id", "file_name", "file_size")
    search_fields    = ("file_name", "mime_type")