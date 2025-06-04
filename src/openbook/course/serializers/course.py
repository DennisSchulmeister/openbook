# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from openbook.auth.serializers.mixins.audit import CreatedModifiedBySerializerMixin
from openbook.auth.serializers.mixins.scope import ScopedRolesSerializerMixin
from openbook.core.serializers.mixins.slug  import SlugSerializerMixin
from openbook.core.serializers.mixins.text  import NameDescriptionSerializerMixin
from openbook.core.serializers.mixins.uuid  import UUIDSerializerMixin
from ..models.course                        import Course

class CourseSerializer(
    UUIDSerializerMixin,
    SlugSerializerMixin,
    NameDescriptionSerializerMixin,
    ScopedRolesSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
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

        expandable_fields = {}