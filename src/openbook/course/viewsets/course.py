# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from drf_spectacular.utils                  import extend_schema
from rest_framework.viewsets                import ModelViewSet

from openbook.drf                           import AllowAnonymousListViewSetMixin
from openbook.drf                           import ModelViewSetMixin
from openbook.auth.filters.mixins.audit     import CreatedModifiedByFilterMixin
from openbook.auth.filters.mixins.scope     import ScopedRolesFilterMixin
from openbook.auth.serializers.mixins.audit import CreatedModifiedBySerializerMixin
from openbook.auth.serializers.mixins.scope import ScopedRolesSerializerMixin
from openbook.auth.serializers.mixins.scope import ScopedRolesListSerializerMixin
from openbook.core.filters.mixins.slug      import SlugFilterMixin
from openbook.core.filters.mixins.text      import NameDescriptionFilterMixin
from openbook.core.serializers.mixins.slug  import SlugSerializerMixin
from openbook.core.serializers.mixins.text  import NameDescriptionListSerializerMixin
from openbook.core.serializers.mixins.text  import NameDescriptionSerializerMixin
from openbook.core.serializers.mixins.uuid  import UUIDSerializerMixin

from ..models.course                        import Course

class CourseListSerializer(
    UUIDSerializerMixin,
    SlugSerializerMixin,
    NameDescriptionListSerializerMixin,
    ScopedRolesListSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Reduced list of fields for filtering a list of courses.
    """
    class Meta:
        model = Course
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *SlugSerializerMixin.Meta.fields,
            *NameDescriptionListSerializerMixin.Meta.fields,
            "is_template",
            *ScopedRolesListSerializerMixin.Meta.fields,
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )
        read_only_fields = fields

class CourseSerializer(
    UUIDSerializerMixin,
    SlugSerializerMixin,
    NameDescriptionSerializerMixin,
    ScopedRolesSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Full list of fields for retrieving a single course.
    """
    class Meta:
        model  = Course
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *SlugSerializerMixin.Meta.fields,
            *NameDescriptionSerializerMixin.Meta.fields,
            "is_template",
            *ScopedRolesSerializerMixin.Meta.fields,
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )

        read_only_fields = (
            *UUIDSerializerMixin.Meta.read_only_fields,
            *SlugSerializerMixin.Meta.read_only_fields,
            *NameDescriptionSerializerMixin.Meta.read_only_fields,
            *ScopedRolesSerializerMixin.Meta.read_only_fields,
            *CreatedModifiedBySerializerMixin.Meta.read_only_fields,
        )

class CourseFilter(
    SlugFilterMixin,
    NameDescriptionFilterMixin,
    CreatedModifiedByFilterMixin,
    ScopedRolesFilterMixin,
):
    class Meta:
        model  = Course
        fields = {
            **SlugFilterMixin.Meta.fields,
            **NameDescriptionFilterMixin.Meta.fields,
            "is_template": ("exact",),
            **ScopedRolesFilterMixin.Meta.fields,
            **CreatedModifiedByFilterMixin.Meta.fields,
        }

@extend_schema(
    extensions={
        "x-app-name":   "Courses",
        "x-model-name": "Courses",
    }
)
class CourseViewSet(
    AllowAnonymousListViewSetMixin,
    ModelViewSetMixin,
    ModelViewSet,
):
    __doc__ = "Courses"

    queryset         = Course.objects.all()
    filterset_class  = CourseFilter
    search_fields    = ("slug", "name", "description")

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        else:
            return CourseSerializer