# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from . import views

def register_api_routes(router, prefix):
    router.register(f"{prefix}/languages",   views.LanguageViewSet,  basename="language")
    router.register(f"{prefix}/media-files", views.MediaFileViewSet, basename="media-file")
    router.register(f"{prefix}/sites",       views.SiteViewSet,      basename="site")
    router.register(f"{prefix}/users",       views.UserViewSet,      basename="user")