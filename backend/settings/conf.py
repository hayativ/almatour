# Project modules
from decouple import config

# ----------------------------------------------
# Env id
#
ENV_POSSIBLE_OPTIONS = (
    "local",
    "prod",
)
ENV_ID = config("PROJECT_ENV_ID")
SECRET_KEY = "django-insecure--!sazwabf2m!-q#8ui0rlql_@^cii54s9cuu6@hhzli(-#yk_@"

# ----------------------------------------------
# DRF Spectacular
#
SPECTACULAR_SETTINGS = {
    'TITLE': 'Almatour API',
    'DESCRIPTION': (
        'Almatour — interactive tourism guide for Almaty, Kazakhstan.\n\n'
        '## Overview\n'
        'This API provides endpoints for discovering places, events, '
        'souvenirs, useful apps, and advertisements in Almaty. '
        'Authenticated users can manage their profile and personal '
        'calendar of events.\n\n'
        '## Authentication\n'
        'Most read-only endpoints are public. User-specific endpoints '
        '(profile, calendar) require a **JWT Bearer token**.\n\n'
        '1. Obtain a token pair via `POST /api/v1/users/token/`\n'
        '2. Include the access token in the `Authorization` header: '
        '`Bearer <access_token>`\n'
        '3. Refresh expired tokens via `POST /api/v1/users/token/refresh/`'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    # ---- Security ----
    'SECURITY': [{'BearerAuth': []}],
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'BearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': (
                    'JWT access token obtained from /api/v1/users/token/. '
                    'Enter the token WITHOUT the "Bearer " prefix.'
                ),
            },
        },
    },

    # ---- Schema generation ----
    'SCHEMA_PATH_PREFIX': r'/api/v1/',
    'COMPONENT_SPLIT_REQUEST': True,

    # ---- Tag ordering ----
    'TAGS': [
        {
            'name': 'Authentication',
            'description': 'Register, obtain and refresh JWT tokens.',
        },
        {
            'name': 'Users',
            'description': 'View and update the authenticated user profile.',
        },
        {
            'name': 'Events',
            'description': (
                'Browse upcoming events in Almaty. '
                'Filterable by category. Paginated (24 per page).'
            ),
        },
        {
            'name': 'Calendar',
            'description': (
                'Personal event calendar for authenticated users. '
                'Add, update status, or remove saved events.'
            ),
        },
        {
            'name': 'Places',
            'description': (
                'Discover attractions and landmarks in Almaty. '
                'Filterable by category.'
            ),
        },
        {
            'name': 'Souvenirs',
            'description': 'Browse souvenir shops and items.',
        },
        {
            'name': 'Apps',
            'description': 'Useful mobile apps and services for tourists.',
        },
        {
            'name': 'Advertisements',
            'description': 'Active promotional banners and announcements.',
        },
    ],

    # ---- Enum naming ----
    'ENUM_NAME_OVERRIDES': {
        'EventCategoryEnum': 'apps.events.models.Event.Category',
        'PlaceCategoryEnum': 'apps.places.models.Place.Category',
        'CalendarStatusEnum': 'apps.events.models.CalendarEvent.Status',
        'LanguageEnum': 'apps.events.models.EventTranslation.Language',
    },

    # ---- UI ----
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
        'filter': True,
    },
    'REDOC_UI_SETTINGS': {
        'hideDownloadButton': False,
    },
}
