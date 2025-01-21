# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework            import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response   import Response

from . import models
from . import serializers

class LanguageViewSet(viewsets.ModelViewSet):
    """
    Read/write view set to access language codes.
    """
    queryset           = models.Language.objects.all()
    serializer_class   = serializers.LanguageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MediaFileViewSet(viewsets.ModelViewSet):
    """
    Read/write view set to access media files.
    """
    queryset           = models.MediaFile.objects.all()
    serializer_class   = serializers.MediaFileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only view set to access basic site information and the API health.
    """
    queryset         = models.Site.objects.all()
    serializer_class = serializers.MediaFileSerializer

    @action(detail=False, methods=["get"])
    def health(self, request):
        """
        Return a simple health status, that the API is up and running.
        """
        return Response({"status": "GOOD"})

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only view set to query active users. The serializer makes sure that only
    basic information is returned. Authenticated users only as we don't want the
    world to scrap our user list.
    """
    queryset           = models.User.objects.filter(is_active = True)
    serializer_class   = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]