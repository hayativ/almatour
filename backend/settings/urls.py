# Django modules
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ---------- OpenAPI schema ----------
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema-alt'),

    # ---------- Swagger UI ----------
    path(
        'api/v1/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/docs/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui-alt'
    ),

    # ---------- ReDoc ----------
    path(
        'api/v1/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
    path(
        'api/docs/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc-alt'
    ),

    # ---------- API endpoints ----------
    path('api/v1/places/', include('apps.places.urls')),
    path('api/v1/events/', include('apps.events.urls')),
    path('api/v1/info/', include('apps.info.urls')),
    path('api/v1/users/', include('apps.users.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
