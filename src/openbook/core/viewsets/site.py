# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from ..models.site              import Site

from rest_framework.viewsets    import ReadOnlyModelViewSet
from rest_framework.decorators  import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response    import Response
from rest_framework.serializers import ModelSerializer

class SiteSerializer(ModelSerializer):
    class Meta:
        model  = Site
        fields = "__all__"

class SiteViewSet(ReadOnlyModelViewSet):
    """
    Read-only view set to access basic site information and the API health.
    """
    queryset         = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False)
    def health(self, request):
        """
        Return a simple health status that the API is up and running.
        """
        return Response({"status": "GOOD"})