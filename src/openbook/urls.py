# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import openbook.core.routes as openbook_core_routes

from django.conf                     import settings
from django.conf.urls.static         import static
from django.views.generic.base       import RedirectView
from django.urls                     import include, path
from rest_framework.permissions      import IsAuthenticatedOrReadOnly
from rest_framework.routers          import DefaultRouter as DRFDefaultRouter

from .admin                          import admin_site

# Overwrite permission class for API root view, since it uses the default from settings.py,
# where we set AllowNone.
DRFDefaultRouter.APIRootView.permission_classes = [IsAuthenticatedOrReadOnly]
router = DRFDefaultRouter()
openbook_core_routes.register(router, "core")

urlpatterns = [
    path("api/",      include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/",    admin_site.urls),

    path("", RedirectView.as_view(url=settings.OB_ROOT_REDIRECT)),
]

if settings.DEBUG:
    # NOTE: Static files are automatically served by runserver from the configured
    # static dirs (usually inside each application)

    # Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Frontend SPA
    urlpatterns += static("app/", document_root=f"{settings.BASE_DIR}/frontend/app/dist/openbook/app")
