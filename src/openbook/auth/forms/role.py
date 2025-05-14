# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation         import gettext_lazy as _

from .mixins.auth                     import ScopeFormMixin
from ..models.role                    import Role
from ..validators                     import validate_permissions

class RoleForm(ScopeFormMixin):
    """
    Custom model form for roles that checks that only allowed permissions are assigned.
    """
    class Meta:
        model  = Role
        fields = "__all__"
    
    class Media:
        js = ScopeFormMixin.Media.js
    
    def clean(self):
        """
        Check that only allowed permissions are assigned.
        """
        cleaned_data = super().clean()
        scope_type  = cleaned_data["scope_type"]
        permissions = cleaned_data["permissions"]
        
        validate_permissions(scope_type, permissions)
        return cleaned_data