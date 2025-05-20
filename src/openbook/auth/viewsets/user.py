# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filterset   import FilterSet
from django_filters.filters     import CharFilter
from drf_spectacular.utils      import extend_schema
from rest_framework.viewsets    import ModelViewSet
from rest_framework.decorators  import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response    import Response
from rest_framework.serializers import BooleanField

from openbook.drf               import ModelViewSetMixin
from ..models.user              import User
from ..models.user_profile      import UserProfile
from ..serializers.user         import UserDetailsReadSerializer
from ..serializers.user         import UserDetailsUpdateSerializer
from ..serializers.user         import UserReadSerializer

class CurrentUserReadSerializer(UserDetailsReadSerializer):
    is_authenticated = BooleanField(help_text="Logged-in User")

class UserFilter(FilterSet):
    first_name = CharFilter(lookup_expr="icontains")
    last_name  = CharFilter(lookup_expr="icontains")
    
    class Meta:
        model  = User
        fields = ("first_name", "last_name", "is_staff")

class UserViewSet(ModelViewSetMixin, ModelViewSet):
    """
    Read/write view set to query active users. The serializer makes sure that only
    basic information is returned. Authenticated users only as we don't want the
    world to scrap our user list.
    """
    __doc__ = "User Profiles"

    lookup_field       = "username"
    queryset           = User.objects.filter(is_active = True)
    permission_classes = (IsAuthenticated, *ModelViewSetMixin.permission_classes)
    http_method_names  = ("get", "put", "patch", "delete")  # Post (create) not allowed!
    filterset_class    = UserFilter
    search_fields      = ("username", "first_name", "last_name")

    def get_serializer_class(self):
        if self.action == "list":
            return UserReadSerializer
        else:
            return UserDetailsReadSerializer
        
    @extend_schema(responses=CurrentUserReadSerializer)
    @action(detail=False, permission_classes=[])
    def current(self, request):
        """
        Return information about the currently logged in user or a sentinel response,
        when the user is not logged in.
        """
        profile = getattr(request.user, "profile", None)
        profile_picture = ""

        try:
            if profile:
                profile_picture = profile.picture.url
        except ValueError:
            pass

        # TODO: Simplify?
        return Response({
            "username":         request.user.username,
            "first_name":       getattr(request.user, "first_name", ""),
            "last_name":        getattr(request.user, "last_name", ""),
            "email":            getattr(request.user, "email", ""),
            "is_staff":         request.user.is_staff,
            "is_superuser":     request.user.is_superuser,
            "is_authenticated": request.user.is_authenticated,
            "profile_picture":  profile_picture,
            "description":      profile.description if profile else "",
        })

    # TODO: Better user DRF viewset functionality but make sure only own user can be changed.
    @extend_schema(request=UserDetailsUpdateSerializer, responses=CurrentUserReadSerializer)
    @action(detail=False, url_path="current", methods=["post"], permission_classes=[IsAuthenticated])
    def update_current(self, request):
        """
        Update information for the currently logged in user.
        """
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Update the user fields
        for field in ["first_name", "last_name", "email"]:
            if field in request.data:
                setattr(user, field, request.data[field])

        user.save()

        # Update the user profile fields
        for field in ["profile_picture", "description"]:
            if field in request.data:
                if field == "profile_picture":
                    profile.picture = request.data[field]
                else:
                    setattr(profile, field, request.data[field])

        profile.save()

        # Return updated user data
        return self.current(request)

