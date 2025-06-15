# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from .viewsets.media_file import MediaFileViewSet
from .viewsets.language   import LanguageViewSet
from .viewsets.site       import SiteViewSet

def register_api_routes(router, prefix):
    router.register(f"{prefix}/languages",   LanguageViewSet,  basename="language")
    router.register(f"{prefix}/media_files", MediaFileViewSet, basename="media_file")
    router.register(f"{prefix}/sites",       SiteViewSet,      basename="site")