# OpenBook: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.utils.translation   import gettext_lazy as _
from django.templatetags.static import static
from pathlib                    import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
#
# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don"t run with debug turned on in production!
SECRET_KEY = "django-insecure-jeo+.}_}9(Q.t_IU$WJ!%eL=b:MDbAL.~NY_=a:>D@:W[XPh4["
DEBUG = True
ALLOWED_HOSTS = ["*"]

OB_ROOT_REDIRECT = "/app/index.html"

# Application definition
#
# NOTE: Sort the apps in the order they should appear in the Admin Dashboard.
# We override the default alphabetical order with the order defined here.
INSTALLED_APPS = [
    # OpenBook Server (order determines order in the Django Admin)
    "openbook.core",
    "openbook.auth",
    "openbook.ui_library",
    "openbook.taxonomy",
    "openbook.textbook",
    "openbook.course",

    # 3rd-party reusable apps
    "daphne",
    "channels",

    # Django REST framework
    "rest_wind",
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",

    # Django Unfold (Modern Admin)
    "unfold.apps.BasicAppConfig",            # before django.contrib.admin
    "unfold.contrib.filters",                # optional, if special filters are needed
    "unfold.contrib.forms",                  # optional, if special form elements are needed
    "unfold.contrib.inlines",                # optional, if special inlines are needed
    "unfold.contrib.import_export",          # optional, if django-import-export package is used
    #"unfold.contrib.guardian",              # optional, if django-guardian package is used
    #"unfold.contrib.simple_history",        # optional, if django-simple-history package is used

    # Django built-in apps
    "openbook.apps.OpenBookAdmin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # django-allauth
    "allauth",
    "allauth.account",
    "allauth.idp.oidc",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.saml",

    # Other useful apps
    "django_cleanup.apps.CleanupConfig",    # Django Cleanup: Automatically delete files when models are deleted or updated
    "django_extensions",                    # Django Extensions (additional management commands)
    "dbbackup",                             # Django DBBackup: Database and Media Files Backups
    "import_export",                        # Django Import/Export: Import and export data in the Django Admin
    "djangoql",                             # Django QL: Advanced search language for Django
    "colorfield",                           # Django Color Field: Color field for models with color-picker in the admin
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",

    # django-allauth
    "allauth.account.middleware.AccountMiddleware",

    # OpenBook
    "openbook.auth.middleware.current_user.CurrentUserMiddleware",
    "openbook.core.middleware.current_language.CurrentLanguageMiddleware",
]

ROOT_URLCONF = "openbook.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "openbook.core.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "openbook.wsgi.application"
ASGI_APPLICATION = "openbook.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Channels
CHANNEL_LAYERS = {
    "default": {
        #"BACKEND": "channels.layers.InMemoryChannelLayer",
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

# Django REST framework
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "openbook.drf.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,

    # Remember authenticated user (complimenting our custom middleware)
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "openbook.auth.middleware.current_user.CurrentUserTrackingAuthentication",
    ],

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "openbook.drf.permissions.DjangoObjectPermissionsOnly",
    ],

    "DEFAULT_FILTER_BACKENDS": (
        #"rest_flex_fields.filter_backends.FlexFieldsFilterBackend",    # (Not possible here due to circular import): drf-flex-fields: Automatic query optimization
        "django_filters.rest_framework.DjangoFilterBackend",            # Query filters
        "rest_framework.filters.SearchFilter",                          # _search query parameter
        "openbook.drf.filters.DjangoObjectPermissionsFilter",           # Object-permission based filter
        "rest_framework.filters.OrderingFilter",                        # _sort query parameter
    ),

    "SEARCH_PARAM": "_search",
    "ORDERING_PARAM": "_sort",
    "PAGE_PARAM": "_page",
    "PAGE_SIZE_PARAM": "_page_size",
}

# See: https://drf-spectacular.readthedocs.io/
SPECTACULAR_SETTINGS = {
    "TITLE": "OpenBook API",
    "DESCRIPTION": "Beautiful and Engaging Learning Materials",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,

    # Self-serve Swagger and Redoc instead of loading from CDN
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",

    "DEBUG": True,

    # Create a custom group in the ReDoc documentation for each app, using the custom
    # tags set on each viewset class. Because otherwise drf-spectacular creates a group
    # for each app using the app label and puts all operations in one large group.
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "openbook.drf.viewsets.add_tag_groups",
    ],
}

# See: https://github.com/rsinger86/drf-flex-fields?tab=readme-ov-file#customization
# Must be defined before the first import of rest_flex_field!
REST_FLEX_FIELDS = {
    "EXPAND_PARAM": "_expand",
    "FIELDS_PARAM": "_fields",
    "OMIT_PARAM": "_omit",
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "openbook_auth.User"

AUTHENTICATION_BACKENDS = (
    "openbook.auth.backends.RoleBasedObjectPermissionsBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Private key for OpenID Connect (Identity Provider)
# IMPORTANT - Generate your own key with:
# $ openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
# See: https://docs.allauth.org/en/latest/idp/openid-connect/installation.html
IDP_OIDC_PRIVATE_KEY = """
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC8rtj7ytTwHvw6
w0BTxwJ12T8ol8Z2fWSReBZ92QEzYxDXkXYFEcMx7WXfX/2Gp463Bv9vG6z/2m1+
IWlnRpwbC8Q5RYx53yZ5IKv4WUwwYo6ScHV3LFPC2KpOEI9ocROryrF286OuQKAx
2cx3SCsm0jAPlmJh59LumiGcVKZrlSHj0axsZISLmD+A4BMXeeAIHbLU72T6hc7x
U7gZlbMilB0Mi/x3BLcjXHSeU+3B4gYESQjQ7y0+5bVpoiMZjDyDI5KhEtl3uZpI
c+3/xaPPWQ72h0X+uOqvEBV7HssbHvO4AUMVNF1pqcaY7HVIElvLTVODdr3Kv6pf
7ZjH5e7ZAgMBAAECggEAFKuE6sSUIkAKurdEF0lwbA+iGyTRYY6oE0WYFS5OMt5x
7GOrja+d9hy/McLWx8cYW9Wg6v+Zqqe3of8wCFfUZyQZWXrUgk9fbBqXrEvADHbn
joRSYf1RqcFJmua2hycIFCRO36yeLEs5IWzuOM0HqSeSi0qauYYHdgsdjn45gwRx
YKWCr3j2f6UBorrAdvs1JYrYqtWgELR6a4sZ/vd5oJZkTpuG+y3aDHPN0z3wJvTr
3Z0ODEfCpOaHMXEDGMN7lkztUCpSaZH44AWTF4/ZKFJcCf1SV1ICflnCD9BF49mJ
1+zfV+OW73siiMscyHU73aoo8haMhMI35coHgwoQAQKBgQD4O+aZRMIfMGRXk4Hf
EHxAp9kBgM7fYhPsrVeXCnimGfemqCjAFwt6Qbal6vbvabCb8U/kiPoO6PBxl+1G
mcf2zSkLWG1sLIirHatMODHY1YY7gc60piNK/7AIxxpJutrTHQijBYH9TplUHQLG
QJYQSlVKv1IvFWeLUbHZULa62QKBgQDClgErnb4+wO6mYY+CklCJ3ayt2HnGbRWU
vw30zmELrSr80cD5oqP0rs5SYW6F08uw59lLUEpOUxBOtqc9LGXJT5/dxEhFIT6l
dtMBDOolgM2En58UOGQ1rnmMLLkDF5TrXuGd6Z4OoHRyak+SMq74TTYyzAqBk1rF
rkz1pOBUAQKBgC38gtrQBxpaD6y9seiOGEauEaCaqThu5fwJnNlpYjJ7Swq/ylTT
sBelBt4z6i0uKj6pdMCEs7aBZtHUcGuM36OUHE9ywUqx8Vup8mr7WhiubeCmSpHi
2VTyiz0FDZStHg7QKSJyScOQhQ01Fqd9nY9FBgoD6Yi5cWY46za0IjX5AoGAW8ci
sC7Lr4+SQHmdlalrQUuECc8jyLpkxm7Cp2e8ECTSNMK+MUBL8rmMaQC5f3ehCESi
kcpB8eVtuKKgCNNrAuOCdLgCmlCO2r5L0aAExEGXLemXv5LFeShc/geOD+5MeCOd
aLzqpt15bwnDlCJBsq3AVX81qV4WH00R0X69rAECgYEA3TzcSJZ4PCqOzsggrtVm
+RI8D2ZkPUuNeNGyGgk/t1AC/+v89kZCxeZkxUAWk3dlk5clzNqAfW+hoL8mdwt+
XVwMmmjcJkmCOX5+J09lkI4aA9HdaudunX7NqOGiHUItnsdd4/f2MEXU0UtFK6YB
bMGK8/i84PEbNBK/8Iy8pdk=
-----END PRIVATE KEY-----
"""

# Django Unfold Admin
UNFOLD = {
    "SITE_TITLE":  _("OpenBook: Admin"),
    "SITE_HEADER": _("OpenBook: Admin"),
    "STYLES": [
        lambda request: static("openbook/admin/bundle.css"),
    ],
    "SCRIPTS": [
        lambda request: static("openbook/admin/bundle.js"),
    ]
}

# E-Mail Settings
# See: https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-EMAIL_BACKEND
# The values below assume you started maildev with "npm start" at the root directory.
DEFAULT_FROM_EMAIL   = "noreply@example.com"
EMAIL_SUBJECT_PREFIX = "[OpenBook] "

#EMAIL_BACKEND        = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST          = "localhost"
EMAIL_PORT          = 1025
# EMAIL_HOST_USER     = ""
# EMAIL_HOST_PASSWORD = ""
# EMAIL_TIMEOUT       = 30

# Website information
SITE_ID = 1
LOGIN_REDIRECT_URL = "/"

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
USE_TZ = True
TIME_ZONE = "UTC"

LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "_static"

STATICFILES_DIRS = [
    BASE_DIR / "frontend" / "admin" / "dist",
    BASE_DIR / "frontend" / "app" / "dist",
]

# Uploaded media files
# https://docs.djangoproject.com/en/5.0/topics/files/
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "_media"

# Database and media files backups
DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": BASE_DIR / "_backup"}

# Import deployment-specific local settings which can override single values here
try:
    EXTRA_INSTALLED_APPS = []

    from .local_settings import *

    INSTALLED_APPS = [*INSTALLED_APPS, *EXTRA_INSTALLED_APPS]
except ImportError:
    pass
