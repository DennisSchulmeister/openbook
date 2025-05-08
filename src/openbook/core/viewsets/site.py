# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from ..models.site              import Site

from django.utils.translation   import gettext_lazy as _
from drf_spectacular.utils      import extend_schema
from drf_spectacular.utils      import inline_serializer
from rest_framework.viewsets    import ReadOnlyModelViewSet
from rest_framework.decorators  import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response    import Response
from rest_framework.serializers import CharField
from rest_framework.serializers import ModelSerializer

class SiteSerializer(ModelSerializer):
    class Meta:
        model  = Site
        fields = ["id", "domain", "name", "short_name", "about_url", "brand_color"]

class SiteViewSet(ReadOnlyModelViewSet):
    """
    Read-only view set to access basic site information and the API health.
    """
    __doc__ = _("General Website Settings")

    queryset           = Site.objects.all()
    serializer_class   = SiteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields   = ["id", "domain"]
    search_fields      = ["domain", "name", "short_name"]
    
    @extend_schema(
        responses = inline_serializer(name="health-response", fields={
            "status": CharField(help_text=_("Status of the API server"))
        }),
    )
    @action(detail=False)
    def health(self, request):
        """
        Return a simple health status that the API is up and running.
        """
        return Response({"status": "GOOD"})
