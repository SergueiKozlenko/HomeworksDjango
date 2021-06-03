from django.conf import settings
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.DRAFT
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.title


class Favorites(models.Model):
    """Избранное."""

    advertisement = models.ForeignKey(
        Advertisement,
        related_name='advertisement',
        on_delete=models.DO_NOTHING
    )

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='user',
        on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return self.advertisement.title
