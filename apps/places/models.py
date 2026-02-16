from django.db import models
from django.core.validators import MinValueValidator

from apps.abstracts.models import AbstractBaseModel


class Place(AbstractBaseModel):
    """A place/attraction in Almaty."""

    class Category(models.IntegerChoices):
        CATEGORY_0 = 0
        CATEGORY_1 = 1
        CATEGORY_2 = 2
        CATEGORY_3 = 3

    image = models.TextField()
    category = models.IntegerField(choices=Category.choices)
    address = models.TextField()
    link = models.TextField()

    class Meta:
        db_table = 'places_place'
        indexes = [
            models.Index(fields=['deleted_at'], name='idx_place_deleted_at'),
        ]
        verbose_name = 'Place'
        verbose_name_plural = 'Places'

    def __str__(self) -> str:
        return f"Place #{self.pk}"


class PlaceTranslation(models.Model):
    """Translation for a Place in a specific language."""

    class Language(models.IntegerChoices):
        LANGUAGE_0 = 0
        LANGUAGE_1 = 1
        LANGUAGE_2 = 2
        LANGUAGE_3 = 3

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='translations',
    )
    language_id = models.IntegerField(choices=Language.choices)
    name = models.TextField()
    timetable = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'places_placetranslation'
        unique_together = [('place', 'language_id')]
        indexes = [
            models.Index(fields=['place'], name='idx_placetrans_place'),
        ]
        verbose_name = 'Place Translation'
        verbose_name_plural = 'Place Translations'

    def __str__(self) -> str:
        return f"{self.name} (lang={self.language_id})"
