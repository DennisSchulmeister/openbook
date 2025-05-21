# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filterset   import FilterSet
from django_filters.filters     import CharFilter
from rest_framework.viewsets    import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission

from openbook.drf               import ModelViewSetMixin
from ..models.user              import User
from ..models.user_profile      import UserProfile
from ..serializers.user         import UserDetailsReadSerializer
from ..serializers.user         import UserDetailsUpdateSerializer
from ..serializers.user         import UserReadSerializer

class CurrentUserReadSerializer(UserDetailsReadSerializer):
    class Meta:
        model  = User
        fields = (*UserDetailsReadSerializer.Meta.fields, "email", "is_authenticated")

class UserFilter(FilterSet):
    first_name = CharFilter(lookup_expr="icontains")
    last_name  = CharFilter(lookup_expr="icontains")
    
    class Meta:
        model  = User
        fields = ("first_name", "last_name", "is_staff")

class IsSelf(BasePermission):
    """
    Allows access only to the user themself.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj
    
class UserViewSet(ModelViewSetMixin, ModelViewSet):
    """
    Read/write view set to query active users and update/delete the own user profile.
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
        elif self.action in ("update", "partial_update"):
            return UserDetailsUpdateSerializer
        else:
            return UserDetailsReadSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSelf()]
        return super().get_permissions()

    def update(self, instance, validated_data):
        """
        Handle updates for separate `UserProfile` model.
        """
        profile_data = {
            "picture":     validated_data.pop("profile_picture", None),
            "description": validated_data.pop("description", None),
        }

        user = super().update(instance, validated_data)
        profile, _ = getattr(user, "profile", None), False

        if profile is None:
            profile, _ = UserProfile.objects.get_or_create(user=user)

        if profile_data["picture"] is not None:
            profile.picture = profile_data["picture"]
        if profile_data["description"] is not None:
            profile.description = profile_data["description"]

        profile.save()
        return user