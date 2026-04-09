from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from apps.info.models import Souvenir, App, Advertisement, AdvertisementTranslation


@admin.register(Souvenir)
class SouvenirAdmin(ModelAdmin):
    list_display = ('id', 'name', 'address')
    search_fields = ('name', 'address')


@admin.register(App)
class AppAdmin(ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class AdvertisementTranslationInline(TabularInline):
    model = AdvertisementTranslation
    extra = 0


@admin.register(Advertisement)
class AdvertisementAdmin(ModelAdmin):
    list_display = ('id', 'is_active', 'priority', 'created_at')
    list_filter = ('is_active',)
    inlines = [AdvertisementTranslationInline]


@admin.register(AdvertisementTranslation)
class AdvertisementTranslationAdmin(ModelAdmin):
    list_display = ('id', 'advertisement', 'language_id', 'name')
    list_filter = ('language_id',)
    search_fields = ('name',)
