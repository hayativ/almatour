from rest_framework.routers import DefaultRouter

from apps.events.views import EventViewSet, CalendarEventViewSet

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('calendar', CalendarEventViewSet, basename='calendar-event')

urlpatterns = router.urls
