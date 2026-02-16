from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.places.models import Place, PlaceTranslation


class PlaceTranslationInline(TabularInline):
    model = PlaceTranslation
    extra = 0


@admin.register(Place)
class PlaceAdmin(ModelAdmin):
    list_display = ('id', 'category', 'address', 'created_at')
    list_filter = ('category',)
    search_fields = ('address',)
    inlines = [PlaceTranslationInline]


@admin.register(PlaceTranslation)
class PlaceTranslationAdmin(ModelAdmin):
    list_display = ('id', 'place', 'language_id', 'name')
    list_filter = ('language_id',)
    search_fields = ('name',)
