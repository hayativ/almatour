from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.places.models import Place
from apps.places.serializers import PlaceSerializer


@extend_schema_view(
    list=extend_schema(
        tags=['Places'],
        summary='List places and attractions',
        description=(
            'Returns all places/attractions in Almaty (excluding soft-deleted). '
            'Supports filtering by `category` query parameter.'
        ),
        parameters=[
            OpenApiParameter(
                name='category',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Filter by place category (0–3).',
                required=False,
            ),
        ],
    ),
    retrieve=extend_schema(
        tags=['Places'],
        summary='Get place details',
        description='Returns full details of a single place, including translations and coordinates.',
    ),
)
class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for places (excludes soft-deleted)."""

    serializer_class = PlaceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        return Place.objects.filter(deleted_at__isnull=True).prefetch_related('translations')
