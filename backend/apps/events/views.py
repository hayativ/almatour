from datetime import date

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample,
)

from apps.events.models import Event, CalendarEvent
from apps.events.serializers import EventSerializer, CalendarEventSerializer


class EventPagination(PageNumberPagination):
    """Paginate event listings — 24 items per page."""
    page_size = 24


@extend_schema_view(
    list=extend_schema(
        tags=['Events'],
        summary='List upcoming events',
        description=(
            'Returns a paginated list of upcoming events in Almaty '
            '(date ≥ today, not soft-deleted), ordered chronologically. '
            'Supports filtering by `category` query parameter.'
        ),
        parameters=[
            OpenApiParameter(
                name='category',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Filter by event category (0–3).',
                required=False,
            ),
            OpenApiParameter(
                name='page',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Page number for pagination (24 items per page).',
                required=False,
            ),
        ],
    ),
    retrieve=extend_schema(
        tags=['Events'],
        summary='Get event details',
        description='Returns full details of a single event, including all translations.',
    ),
)
class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for events (excludes soft-deleted and past)."""

    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    pagination_class = EventPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        return (
            Event.objects.filter(deleted_at__isnull=True, date__gte=date.today())
            .prefetch_related('translations')
            .order_by('date', 'start_time')
        )


@extend_schema_view(
    list=extend_schema(
        tags=['Calendar'],
        summary='List saved calendar events',
        description='Returns all events the authenticated user has saved to their personal calendar.',
        responses={
            200: CalendarEventSerializer(many=True),
            401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.'),
        },
    ),
    retrieve=extend_schema(
        tags=['Calendar'],
        summary='Get a calendar entry',
        description='Returns a single calendar entry for the authenticated user.',
        responses={
            200: CalendarEventSerializer,
            401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.'),
            404: OpenApiResponse(description='Calendar entry not found.'),
        },
    ),
    create=extend_schema(
        tags=['Calendar'],
        summary='Add event to calendar',
        description='Save an event to the authenticated user\'s personal calendar.',
        responses={
            201: CalendarEventSerializer,
            400: OpenApiResponse(description='Validation error (e.g. duplicate entry).'),
            401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.'),
        },
    ),
    update=extend_schema(
        tags=['Calendar'],
        summary='Update calendar entry',
        description='Fully update a calendar entry (e.g. change status).',
        responses={
            200: CalendarEventSerializer,
            401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.'),
            404: OpenApiResponse(description='Calendar entry not found.'),
        },
    ),
    partial_update=extend_schema(
        tags=['Calendar'],
        summary='Partially update calendar entry',
        description='Patch one or more fields of a calendar entry (e.g. change status).',
        examples=[
            OpenApiExample(
                'Status Update Example',
                summary='Change status to "attending"',
                value={'status': 1},
                request_only=True,
            ),
        ],
        responses={
            200: CalendarEventSerializer,
            401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.'),
            404: OpenApiResponse(description='Calendar entry not found.'),
        },
    ),
    destroy=extend_schema(
        tags=['Calendar'],
        summary='Remove event from calendar',
        description='Delete a saved calendar entry for the authenticated user.',
        responses={
            204: OpenApiResponse(description='Calendar entry deleted.'),
            401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.'),
            404: OpenApiResponse(description='Calendar entry not found.'),
        },
    ),
)
class CalendarEventViewSet(viewsets.ModelViewSet):
    """CRUD viewset for user calendar events."""

    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CalendarEvent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
