"""Модели приложения users."""

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from foodgram.constants import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        verbose_name="Электронная почта",
    )
    username = models.CharField(
        unique=True,
        max_length=NAME_MAX_LENGTH,
        validators=[UnicodeUsernameValidator()],
        verbose_name="Имя пользователя",
    )
    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name="Фамилия",
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to="avatars/",
        verbose_name="Аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        """Мета."""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return f"{self.username}"


class Subscriber(models.Model):
    """Модель подписки пользователя на автора."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribing",
        verbose_name="Автор",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="Подписчик",
    )

    class Meta:
        """Мета."""

        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_subscription"
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F("user")),
                name="author_and_user_personal",
            ),
        ]

    def __str__(self):
        """Возвращает строковое представление подписки."""
        return f"{self.user} → {self.author}"
