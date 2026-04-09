from django.db import models


class Souvenir(models.Model):
    """A souvenir shop/item."""

    name = models.TextField()
    address = models.TextField()
    link = models.TextField()
    image = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'info_souvenir'
        verbose_name = 'Souvenir'
        verbose_name_plural = 'Souvenirs'

    def __str__(self) -> str:
        return self.name


class App(models.Model):
    """An app/service listing."""

    name = models.TextField()
    image = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'info_app'
        verbose_name = 'App'
        verbose_name_plural = 'Apps'

    def __str__(self) -> str:
        return self.name


class Advertisement(models.Model):
    """An advertisement/banner."""

    image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'info_advertisement'
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'

    def __str__(self) -> str:
        return f"Ad #{self.pk} (priority={self.priority})"


class AdvertisementTranslation(models.Model):
    """Translation for an Advertisement in a specific language."""

    class Language(models.IntegerChoices):
        LANGUAGE_0 = 0
        LANGUAGE_1 = 1
        LANGUAGE_2 = 2
        LANGUAGE_3 = 3

    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name='translations',
    )
    language_id = models.IntegerField(choices=Language.choices)
    name = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'info_advertisementtranslation'
        unique_together = [('advertisement', 'language_id')]
        indexes = [
            models.Index(fields=['advertisement'], name='idx_adtrans_ad'),
        ]
        verbose_name = 'Advertisement Translation'
        verbose_name_plural = 'Advertisement Translations'

    def __str__(self) -> str:
        return f"{self.name} (lang={self.language_id})"
