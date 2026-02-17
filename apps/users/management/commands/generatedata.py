# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Any
from datetime import date, time as dtime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from apps.users.models import CustomUser 
from apps.places.models import Place, PlaceTranslation
from apps.info.models import Souvenir, App, Advertisement, AdvertisementTranslation
from apps.events.models import Event, EventTranslation, CalendarEvent

NOW = timezone.now


# ============================================================
# ===================== НАЧАЛО =================
# ============================================================

USERS_DATA = [
    {
        "id": 1,
        "email": "admin@example.com",
        "phone": "+77010000001",
        "password": make_password("AdminStrongPass123"),
        "is_superuser": True,
        "username": "admin",
        "is_active": True, #проставить везде True
    },
]

PLACES_DATA = [
    {
        "id": 1,
        "image": "places/opera.jpg",
        "category": 1,  # От 0 до 3
        "address": "Almaty, Abay 110",
        "link": "https://opera.kz",
    },
]

PLACE_TRANSLATIONS_DATA = [
    {
        "id": 1,
        "place_id": 1,
        "language_id": 1,  # От 0 до 3
        "name": "Kazakh State Opera",
        "timetable": "10:00 - 19:00",
        "description": "Main opera theatre in Almaty", # написать побольше
    },
]

EVENTS_DATA = [
    {
        "id": 1,
        "image": "events/concert.jpg",
        "date": date.today() + timedelta(days=3),  # DATE (не timestamp)
        "start_time": dtime(19, 0),               # TIME
        "duration": 120,                          # в минутах, > 0
        "artist": "Symphony Orchestra",
        "cost": 5000,
        "currency": "KZT",                        # проставить везде KZT
        "category": 1,                            # От 0 до 3
        "address": "Abay 110",
        "link": "https://tickets.kz",
    },
]

EVENT_TRANSLATIONS_DATA = [
    {
        "id": 1,
        "event_id": 1,
        "language_id": 1,  # От 0 до 3
        "name": "Evening Concert",
        "description": "Classical music concert",
    },
]

CALENDAR_EVENTS_DATA = [
    {
        "id": 1,
        "user_id": 1,
        "event_id": 1,
        "status": 1,  # проставить везде 1
    }
]

SOUVENIRS_DATA = [
    {
        "id": 1,
        "name": "City Magnet",
        "address": "Almaty souvenir shop",
        "link": "https://shop.kz",
        "image": "souvenirs/magnet.jpg",
    }
]

APPS_DATA = [
    {
        "id": 1,
        "name": "City Guide",
        "image": "apps/cityguide.png",
        "description": "Official city guide application",
    }
]

ADVERTISEMENTS_DATA = [
    {
        "id": 1,
        "image": "ads/banner.jpg",
        "is_active": True,
        "priority": 1,
    }
]

ADVERTISEMENT_TRANSLATIONS_DATA = [
    {
        "id": 1,
        "advertisement_id": 1,
        "language_id": 1,  # От 0 до 3
        "name": "Winter Sale",
        "description": "Up to 50% discount",
    }
]


class Command(BaseCommand):
    help = "Load production initial data into database"

    @transaction.atomic
    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        started = NOW()

        self.load_users()
        self.load_places()
        self.load_place_translations()
        self.load_events()
        self.load_event_translations()
        self.load_calendar_events()
        self.load_souvenirs()
        self.load_apps()
        self.load_advertisements()
        self.load_advertisement_translations()

        self.stdout.write(
            self.style.SUCCESS(
                f"Data successfully loaded in {(NOW() - started).total_seconds()} sec"
            )
        )

    # ========================================================
    # ===================== КОНЕЦ ======================
    # ========================================================

    def load_users(self):
        for user in USERS_DATA:
            CustomUser.objects.update_or_create(
                id=user["id"],
                defaults={
                    "email": user["email"],
                    "phone": user["phone"],
                    "password": user["password"],
                    "is_superuser": bool(user["is_superuser"]),
                    "username": user["username"],
                    # date_joined по схеме DEFAULT CURRENT_TIMESTAMP, но можно проставить явно:
                    "date_joined": NOW(),
                    "last_login": NOW(),
                    "is_active": bool(user["is_active"]),
                },
            )

    def load_places(self):
        for place in PLACES_DATA:
            Place.objects.update_or_create(
                id=place["id"],
                defaults={
                    "image": place["image"],
                    "category": place["category"],
                    "address": place["address"],
                    "link": place["link"],
                    # created_at по схеме DEFAULT CURRENT_TIMESTAMP — можно не трогать,
                    # но при update лучше обновлять updated_at:
                    "updated_at": NOW(),
                    # deleted_at в новой схеме DATETIME NULL, НЕ 0:
                    "deleted_at": None,
                },
            )

    def load_place_translations(self):
        """
        Важно: в схеме UNIQUE(place_id, language_id)
        Поэтому лучше искать по (place_id, language_id), а не по id,
        чтобы не ловить дубли при изменении сидов.
        """
        for tr in PLACE_TRANSLATIONS_DATA:
            PlaceTranslation.objects.update_or_create(
                place_id=tr["place_id"],
                language_id=tr["language_id"],
                defaults={
                    "name": tr["name"],
                    "timetable": tr["timetable"],
                    "description": tr["description"],
                },
            )

    def load_events(self):
        for event in EVENTS_DATA:
            Event.objects.update_or_create(
                id=event["id"],
                defaults={
                    "image": event["image"],
                    "date": event["date"],                 # DATE
                    "start_time": event["start_time"],     # TIME
                    "duration": event["duration"],
                    "artist": event["artist"],
                    "cost": event["cost"],
                    "currency": event.get("currency", "KZT"),
                    "category": event["category"],
                    "address": event["address"],
                    "link": event["link"],
                    "updated_at": NOW(),
                    "deleted_at": None,
                },
            )

    def load_event_translations(self):
        """
        UNIQUE(event_id, language_id) -> ищем по этим полям.
        """
        for tr in EVENT_TRANSLATIONS_DATA:
            EventTranslation.objects.update_or_create(
                event_id=tr["event_id"],
                language_id=tr["language_id"],
                defaults={
                    "name": tr["name"],
                    "description": tr["description"],
                },
            )

    def load_calendar_events(self):
        """
        В новой схеме нет поля date.
        UNIQUE(user_id, event_id) -> ищем по (user_id, event_id).
        """
        for item in CALENDAR_EVENTS_DATA:
            CalendarEvent.objects.update_or_create(
                user_id=item["user_id"],
                event_id=item["event_id"],
                defaults={
                    "status": item["status"],
                },
            )

    def load_souvenirs(self):
        for item in SOUVENIRS_DATA:
            Souvenir.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "address": item["address"],
                    "link": item["link"],
                    "image": item.get("image"),  # image nullable
                },
            )

    def load_apps(self):
        for item in APPS_DATA:
            App.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item["name"],
                    "image": item["image"],
                    "description": item["description"],
                },
            )

    def load_advertisements(self):
        for ad in ADVERTISEMENTS_DATA:
            Advertisement.objects.update_or_create(
                id=ad["id"],
                defaults={
                    "image": ad["image"],
                    "updated_at": NOW(),
                    "is_active": bool(ad["is_active"]),
                    "priority": ad["priority"],
                },
            )

    def load_advertisement_translations(self):
        """
        UNIQUE(advertisement_id, language_id) -> ищем по этим полям.
        """
        for tr in ADVERTISEMENT_TRANSLATIONS_DATA:
            AdvertisementTranslation.objects.update_or_create(
                advertisement_id=tr["advertisement_id"],
                language_id=tr["language_id"],
                defaults={
                    "name": tr["name"],
                    "description": tr["description"],
                },
            )
