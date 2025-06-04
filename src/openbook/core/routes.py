# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from . import viewsets

def register_api_routes(router, prefix):
    pass
    # router.register(f"{prefix}/languages",   viewsets.LanguageViewSet,  basename="language")
    # router.register(f"{prefix}/media_files", viewsets.MediaFileViewSet, basename="media_file")
    # router.register(f"{prefix}/sites",       viewsets.SiteViewSet,      basename="site")