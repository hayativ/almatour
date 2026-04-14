from rest_framework import serializers

from apps.info.models import Souvenir, App, Advertisement, AdvertisementTranslation


class SouvenirSerializer(serializers.ModelSerializer):
    """Serializer for souvenir shops/items."""

    class Meta:
        model = Souvenir
        fields = ['id', 'name', 'address', 'link', 'image']
        extra_kwargs = {
            'name': {'help_text': 'Souvenir shop or item name.'},
            'address': {'help_text': 'Shop address.'},
            'link': {'help_text': 'External link to the shop.'},
            'image': {'help_text': 'Image URL or path.'},
        }


class AppSerializer(serializers.ModelSerializer):
    """Serializer for useful mobile apps and services."""

    class Meta:
        model = App
        fields = ['id', 'name', 'image', 'description']
        extra_kwargs = {
            'name': {'help_text': 'Application name.'},
            'image': {'help_text': 'App icon/image URL or path.'},
            'description': {'help_text': 'Short description of the app.'},
        }


class AdvertisementTranslationSerializer(serializers.ModelSerializer):
    """Nested serializer for advertisement translations."""

    class Meta:
        model = AdvertisementTranslation
        fields = ['id', 'language_id', 'name', 'description']
        extra_kwargs = {
            'language_id': {'help_text': 'Language identifier (0=en, 1=ru, 2=kz, 3=tr).'},
            'name': {'help_text': 'Translated advertisement title.'},
            'description': {'help_text': 'Translated advertisement body text.'},
        }


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer for advertisements with nested translations."""

    translations = AdvertisementTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = [
            'id', 'image', 'created_at', 'updated_at',
            'is_active', 'priority', 'translations',
        ]
        extra_kwargs = {
            'image': {'help_text': 'Banner image URL or path.'},
            'is_active': {'help_text': 'Whether the advertisement is currently active.'},
            'priority': {'help_text': 'Display priority (higher = shown first).'},
        }
