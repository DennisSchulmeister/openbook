# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from drf_spectacular.utils      import extend_schema
from drf_spectacular.utils      import extend_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.response    import Response
from rest_framework.viewsets    import ViewSet

from ..models.user              import User
from ..serializers.user         import UserDetailsReadSerializer

class CurrentUserReadSerializer(UserDetailsReadSerializer):
    class Meta:
        model  = User
        fields = (*UserDetailsReadSerializer.Meta.fields, "email", "is_authenticated")

@extend_schema(
    extensions={
        "x-app-name":   "User Management",
        "x-model-name": "Current User",
    }
)
@extend_schema_view(retrieve=extend_schema(exclude=True))
class CurrentUserViewSet(ViewSet):
    """
    GET endpoint to retrieve the user profile of the currently logged-in user. If the
    user is not logged in, a simple response with `is_authenticated = false` is returned.
    """
    __doc__ = "Currently logged-in user"

    permission_classes = [AllowAny]

    def get_view_name(self):
        return "Current User"

    @extend_schema(
        operation_id= "auth_current_user",
        description = "Returns the currently authenticated user or a fallback response.",
        responses   = CurrentUserReadSerializer,
        summary     = "Retrieve",
    )
    def list(self, request):
        if request.user.is_authenticated:
            return Response(CurrentUserReadSerializer(request.user).data)
        else:
            return Response({"is_authenticated": False})

    def retrieve(self, request, pk=None):
        # Disable detail route
        raise NotImplementedError()