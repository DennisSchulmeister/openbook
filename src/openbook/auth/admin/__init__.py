# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from openbook.admin           import admin_site

from .access_request          import AccessRequestAdmin
from .allowed_role_permission import AllowedRolePermissionAdmin
from .anonymous_permission    import AnonymousPermissionAdmin
from .enrollment_method       import EnrollmentMethodAdmin
from .group                   import GroupAdmin
from .permission              import PermissionTextAdmin
from .role                    import RoleAdmin
from .role_assignment         import RoleAssignmentAdmin
from .user                    import UserAdmin

from ..                       import models

admin_site.register(models.User, UserAdmin)
admin_site.register(models.Group, GroupAdmin)
admin_site.register(models.Permission_T, PermissionTextAdmin)
admin_site.register(models.AnonymousPermission, AnonymousPermissionAdmin)
admin_site.register(models.AllowedRolePermission, AllowedRolePermissionAdmin)
admin_site.register(models.Role, RoleAdmin)
admin_site.register(models.RoleAssignment, RoleAssignmentAdmin)
admin_site.register(models.EnrollmentMethod, EnrollmentMethodAdmin)
admin_site.register(models.AccessRequest, AccessRequestAdmin)