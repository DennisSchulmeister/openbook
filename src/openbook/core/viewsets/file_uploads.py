# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework.viewsets    import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..drf                      import ImprovedModelViewSet
from ..models.file_uploads      import MediaFile
from ..serializers.file_uploads import MediaFileSerializer

class MediaFileViewSet(ImprovedModelViewSet):
    """
    Read/write view set to access media files.
    """
    queryset         = MediaFile.objects.all()
    serializer_class = MediaFileSerializer