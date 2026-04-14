from rest_framework import serializers

from apps.events.models import Event, EventTranslation, CalendarEvent


class EventTranslationSerializer(serializers.ModelSerializer):
    """Nested serializer for event translations (name + description per language)."""

    class Meta:
        model = EventTranslation
        fields = ['id', 'language_id', 'name', 'description']
        extra_kwargs = {
            'language_id': {'help_text': 'Language identifier (0=en, 1=ru, 2=kz, 3=tr).'},
            'name': {'help_text': 'Translated event name.'},
            'description': {'help_text': 'Translated event description.'},
        }


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event with nested translations."""

    translations = EventTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'image', 'date', 'start_time', 'duration',
            'artist', 'cost', 'currency', 'category', 'address',
            'link', 'created_at', 'updated_at', 'translations',
        ]
        extra_kwargs = {
            'image': {'help_text': 'URL or path to the event poster image.'},
            'date': {'help_text': 'Event date (YYYY-MM-DD).'},
            'start_time': {'help_text': 'Event start time (HH:MM:SS).'},
            'duration': {'help_text': 'Duration in minutes (≥ 1).'},
            'artist': {'help_text': 'Performing artist or organiser name.'},
            'cost': {'help_text': 'Ticket price (0 = free).'},
            'currency': {'help_text': 'Price currency code, e.g. KZT.'},
            'category': {'help_text': 'Event category (0=Concerts, 1=Exhibitions, 2=Sport, 3=Festivals).'},
            'address': {'help_text': 'Venue address.'},
            'link': {'help_text': 'External link for tickets or details.'},
        }


class CalendarEventSerializer(serializers.ModelSerializer):
    """Serializer for user calendar entries."""

    class Meta:
        model = CalendarEvent
        fields = ['id', 'user', 'event', 'status']
        read_only_fields = ['user']
        extra_kwargs = {
            'user': {'help_text': 'Owner user ID (auto-set from token, read-only).'},
            'event': {'help_text': 'ID of the saved event.'},
            'status': {'help_text': 'Calendar status (0=saved, 1=attending).'},
        }
