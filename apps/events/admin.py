from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.events.models import Event, EventTranslation, CalendarEvent


class EventTranslationInline(TabularInline):
    model = EventTranslation
    extra = 0


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ('id', 'date', 'start_time', 'artist', 'category', 'cost', 'currency')
    list_filter = ('category', 'date')
    search_fields = ('artist', 'address')
    inlines = [EventTranslationInline]


@admin.register(EventTranslation)
class EventTranslationAdmin(ModelAdmin):
    list_display = ('id', 'event', 'language_id', 'name')
    list_filter = ('language_id',)
    search_fields = ('name',)


@admin.register(CalendarEvent)
class CalendarEventAdmin(ModelAdmin):
    list_display = ('id', 'user', 'event', 'status')
    list_filter = ('status',)
