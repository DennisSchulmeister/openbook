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
from django.urls                     import include, path

from .admin                          import admin_site

urlpatterns = [
    # TODO: Single Page App

    ## path("example/", include("ob_example.urls")),
    path("admin/",  admin_site.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)