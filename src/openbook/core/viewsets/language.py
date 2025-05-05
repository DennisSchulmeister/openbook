# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models.language       import Language
from ..serializers.language  import LanguageSerializer

class LanguageViewSet(ReadOnlyModelViewSet):
    """
    Read-only view set to access language codes.
    """
    queryset         = Language.objects.all()
    serializer_class = LanguageSerializer