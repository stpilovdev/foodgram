"""Модели и генератор хэша для сокращения ссылок."""

import string
from random import choice, randint

from django.db import models

from foodgram.constants import (
    HASH_FIELD_LENGTH,
    MAX_HASH_LENGTH,
    MAX_URL_LENGTH,
    MIN_HASH_LENGTH,
)


def generate_hash():
    """Генерирует случайный хэш для короткой ссылки."""
    return "".join(
        choice(string.ascii_letters + string.digits)
        for _ in range(randint(MIN_HASH_LENGTH, MAX_HASH_LENGTH))
    )


class ShortLink(models.Model):
    """Модель для хранения сокращённых ссылок."""

    original_url = models.CharField(
        max_length=MAX_URL_LENGTH,
        verbose_name="Оригинальная ссылка",
    )
    url_hash = models.CharField(
        unique=True,
        max_length=HASH_FIELD_LENGTH,
        default=generate_hash,
        verbose_name="Хэш ссылки",
    )

    class Meta:
        """Мета."""

        verbose_name = "Сокращённая ссылка"
        verbose_name_plural = "Сокращённые ссылки"
        ordering = ["-id"]

    def __str__(self):
        """Возвращает строковое представление сокращённой ссылки."""
        return f"{self.url_hash} → {self.original_url}"
