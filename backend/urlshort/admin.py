"""Админка приложения urlshort."""

from django.contrib import admin

from .models import ShortLink


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    """Админ-класс для модели сокращённых ссылок."""

    list_display = ("id", "original_url", "url_hash")
    list_display_links = ("original_url",)
