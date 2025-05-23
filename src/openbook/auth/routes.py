# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from . import viewsets

def register_api_routes(router, prefix):
    # router.register(f"{prefix}/access_requests",          viewsets.AccessRequestViewSet,         basename="access_request")
    router.register(f"{prefix}/allowed_role_permissions", viewsets.AllowedRolePermissionViewSet, basename="allowed_role_permission")
    router.register(f"{prefix}/current_user",             viewsets.CurrentUserViewSet,           basename="current_user")
    # router.register(f"{prefix}/enrollment_methods",       viewsets.EnrollmentMethodViewSet,      basename="enrollment_method")
    router.register(f"{prefix}/users",                    viewsets.UserViewSet,                  basename="user")
    router.register(f"{prefix}/permissions",              viewsets.PermissionTViewSet,           basename="permission")
    router.register(f"{prefix}/roles",                    viewsets.RoleViewSet,                  basename="role")
    router.register(f"{prefix}/role_assignments",         viewsets.RoleAssignmentViewSet,        basename="role_assignment")
    router.register(f"{prefix}/scope_types",              viewsets.ScopeTypeViewSet,             basename="scope_type")