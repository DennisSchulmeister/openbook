# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets  import ModelViewSet

from openbook.drf             import ModelViewSetMixin
from openbook.drf             import ModelSerializer
from openbook.drf             import ListSerializer
from ..models.file_uploads    import MediaFile

class MediaFileListSerializer(ListSerializer):
    class Meta:
        model  = MediaFile
        fields = ["content_type", "object_id", "file_name", "file_size", "mime_type"]

class MediaFileSerializer(ModelSerializer):
    class Meta:
        model  = MediaFile
        fields = ["content_type", "object_id", "file_name", "file_size", "mime_type", "file_data"]
        list_serializer_class = MediaFileListSerializer

class MediaFileViewSet(ModelViewSetMixin, ModelViewSet):
    __doc__ = _("Attached Media Files")

    queryset         = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    filterset_fields = MediaFileListSerializer.Meta.fields
    search_fields    = ["file_name"]