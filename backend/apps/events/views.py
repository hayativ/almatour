from datetime import date

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.events.models import Event, CalendarEvent
from apps.events.serializers import EventSerializer, CalendarEventSerializer


class EventPagination(PageNumberPagination):
    page_size = 24


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


class CalendarEventViewSet(viewsets.ModelViewSet):
    """CRUD viewset for user calendar events."""

    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CalendarEvent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
