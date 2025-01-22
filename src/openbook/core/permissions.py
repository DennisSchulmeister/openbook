# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from rest_framework import permissions
from .models        import User

class IsSameUserOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow the user itself to change their profile data.
    Administrators are allowed full access.
    """
    
    def has_object_permission(self, request, view, obj: User) -> bool:
        if not request.user.is_authenticated:
            return False
        
        # TODO: Check request method (e.g. no DELETE!)
        # TODO: request.user.has_perm("app_label.permission", obj)
        # TODO: User cannot set is_superuser himself
        # TODO: How to check permissions on the user object itself (e.g. to apply them in the admin, too)
        return obj == request.user or request.user.is_superuser