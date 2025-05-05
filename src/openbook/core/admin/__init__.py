# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.contrib              import admin
from django.contrib.auth.models  import Group as DjangoGroup

from .file_uploads               import *
from .group                      import *
from .language                   import *
from .site                       import *
from .user                       import *
from ..                          import models

try:
    admin.site.unregister(DjangoGroup)
except:
    pass

admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.Language, LanguageAdmin)
admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.UserGroup, CustomGroupAdmin)

# TODO: https://unfoldadmin.com/docs/configuration/settings/
# TODO: ../admin.py: Override order, possible with Unfold Admin?
# TODO: Unregister sites.Site (not possible?)
# Admin UI for roles etc.