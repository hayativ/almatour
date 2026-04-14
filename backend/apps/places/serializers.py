from rest_framework import serializers

from apps.places.models import Place, PlaceTranslation


class PlaceTranslationSerializer(serializers.ModelSerializer):
    """Nested serializer for place translations."""

    class Meta:
        model = PlaceTranslation
        fields = ['id', 'language_id', 'name', 'timetable', 'description']
        extra_kwargs = {
            'language_id': {'help_text': 'Language identifier (0=en, 1=ru, 2=kz, 3=tr).'},
            'name': {'help_text': 'Translated place name.'},
            'timetable': {'help_text': 'Translated opening-hours / timetable text.'},
            'description': {'help_text': 'Translated place description.'},
        }


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for Place with nested translations and geo-coordinates."""

    translations = PlaceTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = [
            'id', 'image', 'category', 'address', 'link',
            'lat', 'lng',
            'created_at', 'updated_at', 'translations',
        ]
        extra_kwargs = {
            'image': {'help_text': 'URL or path to the place image.'},
            'category': {'help_text': 'Place category (0–3).'},
            'address': {'help_text': 'Street address.'},
            'link': {'help_text': 'External link for more info.'},
            'lat': {'help_text': 'Latitude (WGS 84).'},
            'lng': {'help_text': 'Longitude (WGS 84).'},
        }
