"""Модели приложения recipes."""

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from users.models import User

from foodgram.constants import (
    AMOUNT_MIN,
    COOKING_MIN_TIME,
    INGREDIENT_MAX_LENGTH,
    RECIPE_MAX_LENGTH,
    SLUG_REGEXVALIDATOR,
    TAG_MAX_LENGTH,
    UNIT_INGREDIENT_MAX_LENGTH,
)


class Tag(models.Model):
    """Модель тега для рецептов."""

    name = models.CharField(
        unique=True,
        max_length=TAG_MAX_LENGTH,
        verbose_name="Название тега",
    )
    slug = models.SlugField(
        unique=True,
        max_length=TAG_MAX_LENGTH,
        verbose_name="Слаг",
        validators=[
            RegexValidator(
                SLUG_REGEXVALIDATOR,
                message=(
                    "Slug может содержать только буквы, "
                    "цифры, дефисы и нижние подчеркивания."
                ),
            )
        ],
    )

    class Meta:
        """Мета."""

        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        """Возвращает название тега."""
        return f"{self.name}"


class Ingredient(models.Model):
    """Модель ингредиента с названием и единицей измерения."""

    name = models.CharField(
        unique=True,
        max_length=INGREDIENT_MAX_LENGTH,
        verbose_name="Название ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=UNIT_INGREDIENT_MAX_LENGTH,
        verbose_name="Единица измерения",
    )

    class Meta:
        """Мета."""

        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"],
                name="unique_name_measurement_unit",
            )
        ]
        ordering = ["name"]

    def __str__(self):
        """Возвращает название ингредиента с единицей измерения."""
        return f"{self.name} ({self.measurement_unit})"


class Recipe(models.Model):
    """Модель рецепта с ингредиентами, тегами и автором."""

    tags = models.ManyToManyField(
        Tag,
        through="RecipeTag",
        related_name="recipes",
        verbose_name="Теги",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        verbose_name="Ингредиенты",
    )
    is_favorited = models.BooleanField(
        default=True,
        verbose_name="Добавлен в избранное",
    )
    is_in_shopping_cart = models.BooleanField(
        default=True,
        verbose_name="В списке покупок",
    )
    name = models.CharField(
        max_length=RECIPE_MAX_LENGTH,
        verbose_name="Название рецепта",
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="recipes/",
        verbose_name="Изображение",
    )
    text = models.TextField(
        verbose_name="Описание рецепта",
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                COOKING_MIN_TIME,
                message="Минимальное время приготовления",
            )
        ],
        verbose_name="Время приготовления (мин)",
    )

    class Meta:
        """Мета."""

        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-id"]

    def __str__(self):
        """Возвращает название рецепта."""
        return f"{self.name}"


class RecipeTag(models.Model):
    """Модель связи между рецептом и тегом."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="tag_list",
        verbose_name="Рецепт",
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="tag_recipe",
        verbose_name="Тег",
    )

    class Meta:
        """Мета."""

        verbose_name = "Связь рецепта и тега"
        verbose_name_plural = "Связи рецептов и тегов"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "tag"],
                name="unique_recipe_tag",
            )
        ]

    def __str__(self):
        """Возвращает связь рецепта и тега."""
        return f"{self.recipe} — {self.tag}"


class RecipeIngredient(models.Model):
    """Модель связи ингредиента с рецептом и количеством."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredient_list",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_recipe",
        verbose_name="Ингредиент",
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                AMOUNT_MIN,
                message="Минимальное количество",
            )
        ],
        verbose_name="Количество",
    )

    class Meta:
        """Мета."""

        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецептах"
        constraints = [
            models.UniqueConstraint(
                fields=("recipe", "ingredient"),
                name="unique_recipe_ingredient",
            )
        ]

    def __str__(self):
        """Возвращает строку с ингредиентом и его количеством в рецепте."""
        return f"{self.ingredient} — {self.amount}"


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favoriterecipes",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favoriterecipes",
        verbose_name="Рецепт",
    )

    class Meta:
        """Мета."""

        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_favorite_recipe",
            )
        ]

    def __str__(self):
        """Возвращает строку с пользователем и избранным рецептом."""
        return f"{self.user} → {self.recipe}"


class ShoppingCart(models.Model):
    """Модель корзины покупок пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shoppingcarts",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shoppingcarts",
        verbose_name="Рецепт",
    )

    class Meta:
        """Мета."""

        verbose_name = "Корзина покупок"
        verbose_name_plural = "Корзины покупок"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_shopping_cart",
            )
        ]

    def __str__(self):
        """Возвращает строку с пользователем и рецептом в корзине."""
        return f"{self.user} → {self.recipe}"
