"""Конфигурация приложения urlshort."""

from django.apps import AppConfig


class UrlshortConfig(AppConfig):
    """Конфигурация приложения Urlshort."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "urlshort"
    verbose_name = "Сокращение ссылок"
