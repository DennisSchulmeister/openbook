# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from .access_request          import AccessRequestViewSet
from .allowed_role_permission import AllowedRolePermissionViewSet
from .current_user            import CurrentUserViewSet
from .enrollment_method       import EnrollmentMethodViewSet
from .permission              import PermissionTViewSet
from .role_assignment         import RoleAssignmentViewSet
from .role                    import RoleViewSet
from .scope                   import ScopeTypeViewSet
from .user                    import UserViewSet