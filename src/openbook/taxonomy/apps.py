# OpenBook: Interactive Online Textbooks - Server
# © 2025 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.apps              import AppConfig
from django.utils.translation import gettext_lazy as _

class TaxonomyApp(AppConfig):
    name         = "openbook.taxonomy"
    label        = "openbook_taxonomy"
    verbose_name = _("Learning Taxonomies")
