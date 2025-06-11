# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from debug_toolbar.toolbar           import debug_toolbar_urls
from django.conf                     import settings
from django.conf.urls.static         import static
from django.views.generic.base       import RedirectView
from django.urls                     import include, path
from drf_spectacular.views           import SpectacularAPIView
from drf_spectacular.views           import SpectacularRedocView
from rest_framework.permissions      import IsAuthenticatedOrReadOnly
from rest_framework.routers          import DefaultRouter as DRFDefaultRouter

from .admin                          import admin_site
from .auth.routes                    import register_api_routes as register_auth_api_routes
from .core.routes                    import register_api_routes as register_core_api_routes
from .course.routes                  import register_api_routes as register_course_api_routes
from .taxonomy.routes                import register_api_routes as register_taxonomy_api_routes
from .textbook.routes                import register_api_routes as register_textbook_api_routes
from .ui_library.routes              import register_api_routes as register_ui_library_api_routes

# Overwrite permission class for API root view, since it uses the default from settings.py,
# where we set AllowNone.
DRFDefaultRouter.APIRootView.permission_classes = [IsAuthenticatedOrReadOnly]
api_router = DRFDefaultRouter()

register_auth_api_routes(api_router, "auth")
register_core_api_routes(api_router, "core")
register_course_api_routes(api_router, "course")
register_taxonomy_api_routes(api_router, "taxonomy")
register_textbook_api_routes(api_router, "textbook")
register_ui_library_api_routes(api_router, "ui_library")

urlpatterns = [
    # REST API
    path("api/",              include(api_router.urls)),
    path("api-auth/",         include("rest_framework.urls")),
    path("api/schema/",       SpectacularAPIView.as_view(), name="api-schema"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="api-schema"), name="api-redoc"),

    # Admin Panel
    path("admin/",            admin_site.urls),

    # User Accounts
    path('accounts/',         include("allauth.urls")),
    path("auth-api/",         include("allauth.headless.urls")),

    # Single Page App
    path("",                  RedirectView.as_view(url=settings.OB_ROOT_REDIRECT)),
] + debug_toolbar_urls()

if settings.DEBUG:
    # NOTE: Static files are automatically served by runserver from the configured
    # static dirs (usually inside each application)
    
    # Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Frontend SPA
    urlpatterns += static("app/", document_root=f"{settings.BASE_DIR}/frontend/app/dist/openbook/app")