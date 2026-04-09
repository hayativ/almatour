from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.abstracts.models import AbstractBaseModel


class Event(AbstractBaseModel):
    """An event happening in Almaty."""

    class Category(models.IntegerChoices):
        CATEGORY_0 = 0
        CATEGORY_1 = 1
        CATEGORY_2 = 2
        CATEGORY_3 = 3

    image = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    artist = models.TextField()
    cost = models.PositiveIntegerField(default=0)
    currency = models.TextField(default='KZT')
    category = models.IntegerField(choices=Category.choices)
    address = models.TextField()
    link = models.TextField()

    class Meta:
        db_table = 'events_event'
        indexes = [
            models.Index(fields=['deleted_at'], name='idx_event_deleted_at'),
        ]
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self) -> str:
        return f"Event #{self.pk}"


class EventTranslation(models.Model):
    """Translation for an Event in a specific language."""

    class Language(models.IntegerChoices):
        LANGUAGE_0 = 0
        LANGUAGE_1 = 1
        LANGUAGE_2 = 2
        LANGUAGE_3 = 3

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='translations',
    )
    language_id = models.IntegerField(choices=Language.choices)
    name = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'events_eventtranslation'
        unique_together = [('event', 'language_id')]
        indexes = [
            models.Index(fields=['event'], name='idx_eventtrans_event'),
        ]
        verbose_name = 'Event Translation'
        verbose_name_plural = 'Event Translations'

    def __str__(self) -> str:
        return f"{self.name} (lang={self.language_id})"


class CalendarEvent(models.Model):
    """Links a user to an event with a status."""

    class Status(models.IntegerChoices):
        STATUS_0 = 0
        STATUS_1 = 1

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='calendar_events',
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='calendar_entries',
    )
    status = models.IntegerField(choices=Status.choices)

    class Meta:
        db_table = 'events_calendarevent'
        unique_together = [('user', 'event')]
        indexes = [
            models.Index(fields=['user'], name='idx_calendar_user'),
            models.Index(fields=['event'], name='idx_calendar_event'),
        ]
        verbose_name = 'Calendar Event'
        verbose_name_plural = 'Calendar Events'

    def __str__(self) -> str:
        return f"User {self.user_id} → Event {self.event_id} (status={self.status})"
