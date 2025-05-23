# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from drf_spectacular.utils                     import extend_schema
from django_filters.filters                    import CharFilter
from rest_framework.permissions                import IsAuthenticated
from rest_framework.serializers                import ListField
from rest_framework.viewsets                   import ModelViewSet

from openbook.drf                              import ModelViewSetMixin
from openbook.core.filters.mixins.active       import ActiveInactiveFilterMixin
from openbook.core.filters.mixins.slug         import SlugFilterMixin
from openbook.core.filters.mixins.text         import NameDescriptionFilterMixin
from openbook.core.serializers.mixins.active   import ActiveInactiveSerializerMixin
from openbook.core.serializers.mixins.datetime import DurationSerializerMixin
from openbook.core.serializers.mixins.slug     import SlugSerializerMixin
from openbook.core.serializers.mixins.text     import NameDescriptionListSerializerMixin
from openbook.core.serializers.mixins.text     import NameDescriptionSerializerMixin
from openbook.core.serializers.mixins.uuid     import UUIDSerializerMixin

from ..filters.mixins.audit                    import CreatedModifiedByFilterMixin
from ..filters.mixins.scope                    import ScopeFilterMixin
from ..models.enrollment_method                import EnrollmentMethod
from ..serializers.mixins.audit                import CreatedModifiedBySerializerMixin
from ..serializers.mixins.scope                import ScopeSerializerMixin
from ..serializers.permission                  import PermissionReadField
from ..serializers.permission                  import PermissionWriteField
from ..validators                              import validate_permissions

#TODO

class EnrollmentMethodListSerializer(
    UUIDSerializerMixin,
    ScopeSerializerMixin,
    NameDescriptionListSerializerMixin,
    ActiveInactiveSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Reduced list of fields for getting a list of enrollment methods.
    """
    # role = RoleReadField
    class Meta:
        model = EnrollmentMethod
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            "role",
            *NameDescriptionListSerializerMixin.Meta.fields,
            *ActiveInactiveSerializerMixin.Meta.fields,
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )
        read_only_fields = fields

class EnrollmentMethodSerializer(
    UUIDSerializerMixin,
    ScopeSerializerMixin,
    NameDescriptionSerializerMixin,
    ActiveInactiveSerializerMixin,
    DurationSerializerMixin,
    CreatedModifiedBySerializerMixin,
):
    """
    Full list of fields for retrieving a single enrollment method.
    """
    # role = RoleReadField
    # role_slug = RoleWriteField

    class Meta:
        model = EnrollmentMethod
        fields = (
            *UUIDSerializerMixin.Meta.fields,
            *ScopeSerializerMixin.Meta.fields,
            "role", "role_slug",
            *ActiveInactiveSerializerMixin.Meta.fields,
            *DurationSerializerMixin.Meta.fields,
            "end_date", "passphrase",
            *CreatedModifiedBySerializerMixin.Meta.fields,
        )

        read_only_fields = (
            *UUIDSerializerMixin.Meta.read_only_fields,
            *ScopeSerializerMixin.Meta.read_only_fields,
            *NameDescriptionListSerializerMixin.Meta.read_only_fields,
            *ActiveInactiveSerializerMixin.Meta.read_only_fields,
            *DurationSerializerMixin.Meta.read_only_fields,
            *CreatedModifiedBySerializerMixin.Meta.read_only_fields,
        )

# TODO: Action enroll