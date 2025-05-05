# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models   import AbstractUser

class RoleBasedObjectPermissionsBackend(BaseBackend):
    """
    Custom authentication backend for object permissions via scoped roles. Checks whether
    the user is the scope owner or has a role with the required permission.
    """
    def has_perm(self, user_obj: AbstractUser, perm: str, obj=None) -> bool:
        if obj is not None:
            if hasattr(obj, "owner") and obj.owner == user_obj:
                return True
            elif hasattr(obj, "has_perm"):
                return obj.has_perm(user_obj, perm)
        
        return False

# TODO: Unit tests, including all special cases in DRF