# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.conf                     import settings
from django.conf.urls.static         import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base       import RedirectView
from django.urls                     import include, path
from rest_framework.routers          import DefaultRouter
import openbook.core.urls as openbook_core_urls

from .admin                          import admin_site

router = DefaultRouter()
openbook_core_urls.register_api_routes(router, "/core")

urlpatterns = [
    path("api", include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path("admin/", admin_site.urls),
]

if settings.DEBUG:
    # Static files and media files
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Frontend SPA
    urlpatterns += static("website/", document_root=f"{settings.STATIC_ROOT}/openbook/website")
    urlpatterns += path("", RedirectView.as_view(url="/website/index.html")),