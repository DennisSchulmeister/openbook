# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django_filters.filters                  import CharFilter
from rest_framework.permissions              import IsAuthenticated
from rest_framework.viewsets                 import ModelViewSet

from openbook.drf                            import ModelViewSetMixin
from openbook.core.filters.mixins.active     import ActiveInactiveFilterMixin
from openbook.core.filters.mixins.slug       import SlugFilterMixin
from openbook.core.filters.mixins.text       import NameDescriptionFilterMixin
from openbook.core.serializers.mixins.active import ActiveInactiveSerializerMixin
from openbook.core.serializers.mixins.slug   import SlugSerializerMixin
from openbook.core.serializers.mixins.text   import NameDescriptionListSerializerMixin
from openbook.core.serializers.mixins.text   import NameDescriptionSerializerMixin
from openbook.core.serializers.mixins.uuid   import UUIDSerializerMixin

from ..filters.mixins.audit                  import CreatedModifiedByFilterMixin
from ..filters.mixins.scope                  import ScopeFilterMixin
from ..models.allowed_role_permission        import AllowedRolePermission
from ..serializers.mixins.audit              import CreatedModifiedBySerializerMixin
from ..serializers.mixins.scope              import ScopeSerializerMixin
from ..serializers.permission                import PermissionListReadField
from ..serializers.permission                import PermissionListWriteField
from ..validators                            import validate_permissions
# TODO: Should access be restricted?