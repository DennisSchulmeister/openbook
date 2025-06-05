# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from drf_spectacular.utils      import extend_schema
from drf_spectacular.utils      import extend_schema_field
from drf_spectacular.utils      import extend_schema_view
from django_filters.filterset   import FilterSet
from django_filters.filters     import BooleanFilter
from django_filters.filters     import CharFilter
from rest_flex_fields           import FlexFieldsModelSerializer
from rest_framework.permissions import AllowAny
from rest_framework.serializers import SerializerMethodField
from rest_framework.response    import Response
from rest_framework.viewsets    import ModelViewSet
from rest_framework.viewsets    import ViewSet

from openbook.drf               import ModelViewSetMixin
from openbook.drf               import with_flex_fields_parameters
from ..models.user              import User
from ..models.user_profile      import UserProfile

class UserProfileSerializer(FlexFieldsModelSerializer):
    __doc__ = "User Profile"

    class Meta:
        model  = UserProfile
        fields = ("user", "description", "picture")

class UserSerializer(FlexFieldsModelSerializer):
    __doc__ = "User"

    full_name = SerializerMethodField()

    class Meta:
        model    = User
        fields   = ("username", "full_name", "first_name", "last_name", "profile")
        filterset_fields = ("first_name", "last_name", "is_staff")
        expandable_fields = {"profile": UserProfileSerializer}
    
    @extend_schema_field(str)
    def get_full_name(self, obj):
        return obj.get_full_name() if hasattr(obj, "get_full_name") else ""

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile")
        instance = super().update(instance, validated_data)
        profile = UserProfile.objects.get_or_create(user=instance)

        if hasattr(profile_data, "description"):
            profile.description = profile_data.description
        
        if hasattr(profile_data, "picture"):
            profile.picture = profile_data.picture
        
        return instance

class CurrentUserSerializer(UserSerializer):
    __doc__ = "Current User"

    class Meta:
        model  = User
        fields = (*UserSerializer.Meta.fields, "email", "is_authenticated")

class UserFilter(FilterSet):
    first_name = CharFilter(lookup_expr="icontains")
    last_name  = CharFilter(lookup_expr="icontains")
    email      = CharFilter(lookup_expr="icontains")
    is_staff   = BooleanFilter()
    
    class Meta:
        model  = User
        fields = ("username", "first_name", "last_name", "email", "is_staff")

@extend_schema(
    extensions={
        "x-app-name":   "User Management",
        "x-model-name": "User Profiles",
    }
)
@with_flex_fields_parameters()
class UserViewSet(ModelViewSetMixin, ModelViewSet):
    """
    Read/write view set to query active users and update/delete the own user profile.
    """
    __doc__ = "Users"

    lookup_field       = "username"
    queryset           = User.objects.filter(is_active = True)
    http_method_names  = ("get", "put", "patch", "delete")  # Post (create) not allowed!
    filterset_class    = UserFilter
    serializer_class   = UserSerializer
    ordering           = ("username",)
    search_fields      = ("username", "first_name", "last_name", "email")

@extend_schema(
    extensions={
        "x-app-name":   "User Management",
        "x-model-name": "Current User",
    }
)
@extend_schema_view(retrieve=extend_schema(exclude=True))
@with_flex_fields_parameters()
class CurrentUserViewSet(ViewSet):
    """
    GET endpoint to retrieve the user profile of the currently logged-in user. If the
    user is not logged in, a simple response with `is_authenticated = false` is returned.
    """
    __doc__ = "Current User"

    permission_classes = [AllowAny]

    def get_view_name(self):
        return "Current User"

    @extend_schema(
        operation_id= "auth_current_user",
        description = "Returns the currently authenticated user or a fallback response.",
        responses   = CurrentUserSerializer,
        summary     = "Retrieve",
    )
    def list(self, request):
        if request.user.is_authenticated:
            return Response(CurrentUserSerializer(request.user).data)
        else:
            return Response({"is_authenticated": False})

    def retrieve(self, request, pk=None):
        # Disable detail route
        raise NotImplementedError()