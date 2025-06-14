"""Админка приложения users."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import Subscriber, User


class SubscriberInline(admin.TabularInline):
    """Инлайн-форма подписок в админке пользователя."""

    model = Subscriber
    fk_name = "author"
    extra = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Кастомная админка для модели пользователя."""

    @admin.display(description="Подписчики")
    def get_subscribers(self, obj):
        """Возвращает список подписчиков пользователя."""
        subscribers = Subscriber.objects.filter(author_id=obj.id)
        return [sub.user for sub in subscribers]

    inlines = [SubscriberInline]
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "get_subscribers",
    )
    list_display_links = ("username",)
    list_filter = ("username",)
    search_fields = ("username",)
    search_help_text = "Поиск по имени пользователя."
    ordering = ("username",)


admin.site.unregister(Group)
