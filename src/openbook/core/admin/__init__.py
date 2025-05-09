# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from openbook.admin              import admin_site

from .file_uploads               import *
from .language                   import *
from .site                       import *

from ..                          import models

admin_site.register(models.Site, SiteAdmin)
admin_site.register(models.Language, LanguageAdmin)