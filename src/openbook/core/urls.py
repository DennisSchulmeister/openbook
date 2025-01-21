# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.urls            import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"languages", views.LanguageViewSet, basename="language")
router.register(r"media-files", views.MediaFileViewSet, basename="media-file")
router.register(r"sites", views.SiteViewSet, basename="site")
router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = [
    path('', include(router.urls)),
]