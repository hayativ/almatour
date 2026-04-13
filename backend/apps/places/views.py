from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.places.models import Place
from apps.places.serializers import PlaceSerializer


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for places (excludes soft-deleted)."""

    serializer_class = PlaceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        return Place.objects.filter(deleted_at__isnull=True).prefetch_related('translations')
