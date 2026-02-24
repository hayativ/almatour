from rest_framework import serializers

from apps.places.models import Place, PlaceTranslation


class PlaceTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceTranslation
        fields = ['id', 'language_id', 'name', 'timetable', 'description']


class PlaceSerializer(serializers.ModelSerializer):
    translations = PlaceTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = [
            'id', 'image', 'category', 'address', 'link',
            'created_at', 'updated_at', 'translations',
        ]
