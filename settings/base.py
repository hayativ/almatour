# Python modules

import os

# Project modules
from settings.conf import *


# ----------------------------------------------
# Path
#
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_URLCONF = "settings.urls"
WSGI_APPLICATION = "settings.wsgi.application"
ASGI_APPLICATION = "settings.asgi.application"

# ----------------------------------------------
# Apps
#
DJANGO_AND_THIRD_PARTY_APPS = [
    "unfold",

    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
]

PROJECT_APPS = [
    "apps.users.apps.UsersConfig",
    "apps.places.apps.PlacesConfig",
    "apps.events.apps.EventsConfig",
    "apps.info.apps.InfoConfig",
    "apps.abstracts.apps.AbstractsConfig",
]

INSTALLED_APPS = DJANGO_AND_THIRD_PARTY_APPS + PROJECT_APPS

# ----------------------------------------------
# Middleware | Templates | Validators
#
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ----------------------------------------------
# Internationalization
#
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------------------------
# Static | Media
#
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

# ----------------------------------------------
# Unfold
#
UNFOLD = {
    "SITE_HEADER": "Almatour",
    "SITE_TITLE": "Almatour",
    "SITE_SYMBOL": "🏔️",
    "SHOW_LANG_SWITCH": False,

    "SIDEBAR": {
        "items": [
            {
                "label": "Users",
                "icon": "user",
                "items": [
                    {"model": "users.CustomUser"},
                ],
            },
            {
                "label": "Places",
                "icon": "map-pin",
                "items": [
                    {"model": "places.Place"},
                    {"model": "places.PlaceTranslation"},
                ],
            },
            {
                "label": "Events",
                "icon": "calendar",
                "items": [
                    {"model": "events.Event"},
                    {"model": "events.EventTranslation"},
                    {"model": "events.CalendarEvent"},
                ],
            },
            {
                "label": "Info",
                "icon": "info",
                "items": [
                    {"model": "info.Souvenir"},
                    {"model": "info.App"},
                    {"model": "info.Advertisement"},
                    {"model": "info.AdvertisementTranslation"},
                ],
            },
        ]
    },
}

# ----------------------------------------------
# Rest Framework
#
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
