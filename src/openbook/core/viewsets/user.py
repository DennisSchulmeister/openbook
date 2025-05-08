# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from ..drf                      import ModelViewSetMixin, ModelSerializer
from ..models.user              import User

from rest_framework.viewsets    import ModelViewSet
from rest_framework.decorators  import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response    import Response

class UserSerializer(ModelSerializer):
    class Meta:
        model  = User
        fields = ["username", "first_name", "last_name", "is_staff"]

class UserViewSet(ModelViewSetMixin, ModelViewSet):
    """
    Read/write view set to query active users. The serializer makes sure that only
    basic information is returned. Authenticated users only as we don't want the
    world to scrap our user list.
    """
    queryset           = User.objects.filter(is_active = True)
    serializer_class   = UserSerializer
    permission_classes = [IsAuthenticated, *ModelViewSetMixin.permission_classes]

    @action(detail=False, permission_classes=[])
    def current(self, request):
        """
        Return information about the currently logged in user or a sentinel response,
        when the user is not logged in.
        """
        return Response({
            "username":         request.user.username,
            "first_name":       getattr(request.user, "first_name", ""),
            "last_name":        getattr(request.user, "last_name", ""),
            "is_staff":         request.user.is_staff,
            "is_authenticated": request.user.is_authenticated,
        })