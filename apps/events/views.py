from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.events.models import Event, CalendarEvent
from apps.events.serializers import EventSerializer, CalendarEventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for events (excludes soft-deleted)."""

    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        return Event.objects.filter(deleted_at__isnull=True).prefetch_related('translations')


class CalendarEventViewSet(viewsets.ModelViewSet):
    """CRUD viewset for user calendar events."""

    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CalendarEvent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
