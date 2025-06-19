"""Админка приложения recipes."""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
    Tag,
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для модели тегов."""

    list_display = ("id", "name", "slug")
    list_display_links = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """Админка для модели ингредиентов."""

    list_display = ("id", "name", "measurement_unit")
    list_display_links = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по названию ингредиента."


class RecipeTagInline(admin.TabularInline):
    """Инлайн для связи рецепта с тегами."""

    model = RecipeTag
    extra = 1


class RecipeIngredientInline(admin.TabularInline):
    """Инлайн для связи рецепта с ингредиентами."""

    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка для модели рецептов."""

    @admin.display(description="Теги")
    def get_tags(self, obj):
        """Возвращает список тегов рецепта через запятую."""
        return ", ".join([tag.name for tag in obj.tags.all()])

    @admin.display(description="Ингредиенты")
    def get_ingredients(self, obj):
        """Возвращает список ингредиентов рецепта с количеством и единицами."""
        return ", ".join(
            [
                f"{ingredients.ingredient} - {ingredients.amount} "
                f"{ingredients.ingredient.measurement_unit}"
                for ingredients in obj.ingredient_list.all()
            ]
        )

    inlines = [RecipeTagInline, RecipeIngredientInline]
    list_display = ("id", "name", "author", "get_tags", "get_ingredients")
    list_display_links = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по названию рецепта."


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Админка для модели избранных рецептов."""

    list_display = ("id", "user", "recipe")
    list_display_links = ("user",)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админка для модели корзины покупок."""

    list_display = ("id", "user", "recipe")
    list_display_links = ("user",)
