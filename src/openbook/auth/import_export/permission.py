# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib.auth.models import Permission
from import_export.widgets      import ManyToManyWidget

from ..utils                    import permission_for_perm_string
from ..utils                    import perm_string_for_permission

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
        
        perm_strings = [perm_string_for_permission(permission) for permission in value.all()]
        return self.separator.join(perm_strings)
    
    def clean(self, value, obj=None, **kwargs):
        perm_strings = value.split(self.separator)
        perm_strings = filter(None, [perm_string.strip() for perm_string in perm_strings])
        return [permission_for_perm_string(perm_string) for perm_string in perm_strings]