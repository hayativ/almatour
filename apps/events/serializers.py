from rest_framework import serializers

from apps.events.models import Event, EventTranslation, CalendarEvent


class EventTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTranslation
        fields = ['id', 'language_id', 'name', 'description']


class EventSerializer(serializers.ModelSerializer):
    translations = EventTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'image', 'date', 'start_time', 'duration',
            'artist', 'cost', 'currency', 'category', 'address',
            'link', 'created_at', 'updated_at', 'translations',
        ]


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = ['id', 'user', 'event', 'status']
        read_only_fields = ['user']
