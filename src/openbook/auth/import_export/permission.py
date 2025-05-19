# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models import Permission
from import_export.widgets      import ForeignKeyWidget
from import_export.widgets      import ManyToManyWidget

from ..utils                    import permission_for_perm_string
from ..utils                    import perm_string_for_permission

class PermissionForeignKeyWidget(ForeignKeyWidget):
    """
    A customized foreign-key widget that exports and imports permissions as
    Django-style permission strings.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(model=Permission, *args, **kwargs)

    def render(self, value, row=None, **kwargs):
        return perm_string_for_permission(value)
    
    def clean(self, value, obj=None, **kwargs):
        return permission_for_perm_string(value)

class PermissionManyToManyWidget(ManyToManyWidget):
    """
    A customized many-to-many widget that exports and imports permissions as
    Django-style permission strings.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(model=Permission, *args, **kwargs)

    def render(self, value, row=None, **kwargs):
        if not value:
            return ""
        
        perm_strings = [perm_string_for_permission(p) for p in value.all()]
        return self.separator.join(perm_strings)
    
    def clean(self, value, obj=None, **kwargs):
        perm_strings = value.split(self.separator)
        perm_strings = filter(None, [ps.strip() for ps in perm_strings])
        return [permission_for_perm_string(ps) for ps in perm_strings]