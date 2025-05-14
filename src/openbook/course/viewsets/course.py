# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework.viewsets                import ModelViewSet

from openbook.drf                           import ModelViewSetMixin
from openbook.auth.filters.mixins.audit     import CreatedModifiedByFilterMixin
from openbook.auth.filters.mixins.auth      import ScopedRolesFilterMixin
from openbook.auth.viewsets.mixins.auth     import ScopedRolesViewSetMixin
from openbook.auth.serializers.mixins.audit import CreatedModifiedBySerializerMixin
from openbook.auth.serializers.mixins.auth  import ScopedRolesSerializerMixin
from openbook.auth.serializers.mixins.auth  import ScopedRolesListSerializerMixin
from openbook.core.filters.mixins.text      import NameDescriptionFilterMixin
from openbook.core.viewsets.mixins.text     import name_description_fields
from openbook.core.viewsets.mixins.text     import name_description_list_fields

from ..models.course                        import Course

class CourseListSerializer(ScopedRolesListSerializerMixin, CreatedModifiedBySerializerMixin):
    """
    Reduced list of fields for filtering a list of courses.
    """
    class Meta:
        model = Course
        fields = (
            "id",
            "slug",
            *name_description_list_fields,
            "is_template",
            *ScopedRolesListSerializerMixin.Meta.fields,
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )
        read_only_fields = fields

class CourseSerializer(ScopedRolesSerializerMixin, CreatedModifiedBySerializerMixin):
    """
    Full list of fields for retrieving a single course.
    """
    class Meta:
        model  = Course
        fields = (
            "id",
            "slug",
            *name_description_fields,
            "is_template",
            *ScopedRolesSerializerMixin.Meta.fields,
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )

        read_only_fields = (
            "id",
            *ScopedRolesSerializerMixin.Meta.read_only_fields,
            *CreatedModifiedBySerializerMixin.Meta.read_only_fields,
        )

class CourseFilter(NameDescriptionFilterMixin, CreatedModifiedByFilterMixin, ScopedRolesFilterMixin):
    class Meta:
        model  = Course
        fields = {
            "slug":        ("exact",),
            **NameDescriptionFilterMixin.Meta.fields,
            "is_template": ("exact",),
            **ScopedRolesFilterMixin.Meta.fields,
            **CreatedModifiedByFilterMixin.Meta.fields,
        }
        permission_field = "public_permissions"

class CourseViewSet(ScopedRolesViewSetMixin, ModelViewSetMixin, ModelViewSet):
    __doc__ = "Courses"

    queryset         = Course.objects.all()
    filterset_class  = CourseFilter
    search_fields    = ("slug", "name", "description")

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        else:
            return CourseSerializer