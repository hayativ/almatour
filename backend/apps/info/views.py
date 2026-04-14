from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.info.models import Souvenir, App, Advertisement
from apps.info.serializers import (
    SouvenirSerializer,
    AppSerializer,
    AdvertisementSerializer,
)


@extend_schema_view(
    list=extend_schema(
        tags=['Souvenirs'],
        summary='List souvenir shops',
        description='Returns all souvenir shops/items available in Almaty.',
    ),
    retrieve=extend_schema(
        tags=['Souvenirs'],
        summary='Get souvenir details',
        description='Returns full details of a single souvenir entry.',
    ),
)
class SouvenirViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for souvenir shops and items."""

    queryset = Souvenir.objects.all()
    serializer_class = SouvenirSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    list=extend_schema(
        tags=['Apps'],
        summary='List useful apps',
        description='Returns all useful mobile apps and services recommended for tourists.',
    ),
    retrieve=extend_schema(
        tags=['Apps'],
        summary='Get app details',
        description='Returns full details of a single app/service listing.',
    ),
)
class AppViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for useful mobile apps and services."""

    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    list=extend_schema(
        tags=['Advertisements'],
        summary='List active advertisements',
        description=(
            'Returns all active advertisements/banners, '
            'ordered by priority (highest first).'
        ),
    ),
    retrieve=extend_schema(
        tags=['Advertisements'],
        summary='Get advertisement details',
        description='Returns full details of a single advertisement, including translations.',
    ),
)
class AdvertisementViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for active promotional advertisements."""

    serializer_class = AdvertisementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Advertisement.objects.filter(is_active=True).prefetch_related(
            'translations'
        ).order_by('-priority')
