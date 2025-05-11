# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.core.exceptions           import ValidationError
from django.utils.translation         import gettext_lazy as _

from .mixins.scope                    import ScopeFormMixin
from ..models.allowed_role_permission import AllowedRolePermission
from ..models.role                    import Role

class RoleForm(ScopeFormMixin):
    """
    Custom model form for roles that checks that only allowed permissions are assigned.
    """
    class Meta:
        model  = Role
        fields = "__all__"
    
    class Media:
        js = ScopeFormMixin.Media.js
    
    def clean_permissions(self):
        """
        Check that only allowed permissions are assigned.
        """
        scope_type  = self.cleaned_data["scope_type"]
        permissions = self.cleaned_data["permissions"]

        if not scope_type or not permissions:
            return permissions
        
        allowed_permissions = AllowedRolePermission.get_for_scope_type(scope_type).all()
        allowed_permission_objects = [allowed_permission.permission for allowed_permission in allowed_permissions]

        for permission in permissions:
            if not permission in allowed_permission_objects:
                raise ValidationError(_("Permission %(perm)s cannot be assigned in this scope"), params={
                    "perm": f"{permission}",
                })
        
        return permissions