# OpenBook Studio: Interactive Online Textbooks - Server
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from pathlib import Path

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

# Application definition
#
# NOTE: Sort the apps in the order they should appear in the Admin Dashboard.
# We override the default alphabetical order with the order defined here.
INSTALLED_APPS = [
    # OpenBook Server
    "openbook_server",

    # 3rd-party reusable apps
    "daphne",
    "channels",

    # Django built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
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

    # OpenBook Studio
    "openbook_server.middleware.CurrentUserMiddleware",
]

ROOT_URLCONF = "openbook_server.urls"

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
                "openbook_server.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "openbook_server.wsgi.application"
ASGI_APPLICATION = "openbook_server.asgi.application"

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

AUTH_USER_MODEL = "openbook_server.User"

# E-Mail Settings
# See: https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-EMAIL_BACKEND
# The values below assume you started maildev with "npm start" at the root directory.
DEFAULT_FROM_EMAIL   = "noreply@example.com"
EMAIL_SUBJECT_PREFIX = "[OpenBook Studio] "

#EMAIL_BACKEND        = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST          = "localhost"
EMAIL_PORT          = 1025
# EMAIL_HOST_USER     = ""
# EMAIL_HOST_PASSWORD = ""
# EMAIL_TIMEOUT       = 30

# Website information
SITE_ID = 1

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

# Uploaded media files
# https://docs.djangoproject.com/en/5.0/topics/files/
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "_media"

# Import deployment-specific local settings which can override single values here
try:
    from .local_settings import *
except ImportError:
    pass
