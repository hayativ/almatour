from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.info.models import Souvenir, App, Advertisement
from apps.info.serializers import (
    SouvenirSerializer,
    AppSerializer,
    AdvertisementSerializer,
)


class SouvenirViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Souvenir.objects.all()
    serializer_class = SouvenirSerializer
    permission_classes = [AllowAny]


class AppViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [AllowAny]


class AdvertisementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdvertisementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Advertisement.objects.filter(is_active=True).prefetch_related(
            'translations'
        ).order_by('-priority')
