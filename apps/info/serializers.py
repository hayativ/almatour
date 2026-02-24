from rest_framework import serializers

from apps.info.models import Souvenir, App, Advertisement, AdvertisementTranslation


class SouvenirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Souvenir
        fields = ['id', 'name', 'address', 'link', 'image']


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'name', 'image', 'description']


class AdvertisementTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementTranslation
        fields = ['id', 'language_id', 'name', 'description']


class AdvertisementSerializer(serializers.ModelSerializer):
    translations = AdvertisementTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = [
            'id', 'image', 'created_at', 'updated_at',
            'is_active', 'priority', 'translations',
        ]
