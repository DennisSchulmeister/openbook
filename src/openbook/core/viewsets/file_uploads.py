# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework.viewsets    import ModelViewSet

from ..drf                      import ModelViewSetMixin, ModelSerializer
from ..models.file_uploads      import MediaFile

class MediaFileSerializer(ModelSerializer):
    class Meta:
        model  = MediaFile
        fields = "__all__"

class MediaFileViewSet(ModelViewSetMixin, ModelViewSet):
    """
    Read/write view set to access media files.
    """
    queryset         = MediaFile.objects.all()
    serializer_class = MediaFileSerializer