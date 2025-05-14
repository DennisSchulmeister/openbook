# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.contenttypes.models   import ContentType
from django_filters.filters               import CharFilter
from rest_framework.viewsets              import ModelViewSet

from openbook.drf                         import ModelViewSetMixin
from openbook.drf                         import ModelSerializer
from openbook.auth.filters.audit          import CreatedModifiedByFilterMixin
from openbook.auth.serializers.permission import PermissionSerializer
from openbook.auth.validators             import validate_permissions
from openbook.auth.serializers.user       import UserReadField
from openbook.auth.serializers.user       import UserWriteField

from ..models.course                      import Course

## TODO: ScopedRolesXXXMixin classes

class CourseListSerializer(ModelSerializer):
    """
    Reduced list of fields for filtering a list of courses.
    """
    created_by  = UserReadField(read_only=True)
    modified_by = UserReadField(read_only=True)
    owner       = UserReadField(read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "slug",
            "name",
            "is_template", "owner",
            "created_by", "created_at", "modified_by", "modified_at",
        )

class CourseSerializer(ModelSerializer):
    """
    Full list of fields for retrieving a single course.
    """
    owner              = UserReadField(read_only=True)
    owner_username     = UserWriteField(write_only=True)

    public_permissions = PermissionSerializer(many=True)
    created_by         = UserReadField(read_only=True)
    modified_by        = UserReadField(read_only=True)

    class Meta:
        model  = Course
        fields = (
            "id",
            "slug",
            "name", "description", "text_format",
            "is_template",
            "owner", "owner_username",
            "public_permissions",
            "created_by", "created_at", "modified_by", "modified_at",
        )

        read_only_fields = (
            "id",
            "created_at", "modified_at",
        )

    def validate(self, attributes):
        """
        Check that only allowed permissions are assigned.
        """
        scope_type = ContentType.objects.get_for_model(self.Meta.model)
        public_permissions = attributes.get("public_permissions", None)

        validate_permissions(scope_type, public_permissions)
        return attributes

class CourseFilter(CreatedModifiedByFilterMixin):
    owner = CharFilter(method="owner_filter")

    class Meta:
        model  = Course
        fields = {
            "id":          ("exact",),
            "slug":        ("exact",),
            "name":        ("exact",),
            "is_template": ("exact",),
            "owner":       ("exact",),
            **CreatedModifiedByFilterMixin.Meta.fields,
        }
        permission_field = "public_permissions"

    def owner_filter(self, queryset, name, value):
        return queryset.filter(owner__username=value)

class CourseViewSet(ModelViewSetMixin, ModelViewSet):
    __doc__ = "Courses"

    queryset         = Course.objects.all()
    filterset_class  = CourseFilter
    search_fields    = ("slug", "name", "description")

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        else:
            return CourseSerializer

    def create(self, validated_data):
        validated_data["owner"] = validated_data.pop("owner_username", None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.owner = validated_data.pop("owner_username", instance.owner)
        return super().update(instance, validated_data)