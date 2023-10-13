from enum import Enum
from functools import cached_property

from django.db import models


class Field(Enum):
    PROTEIN = 'protein'
    FAT = 'fat'
    CARBOHYDRATE = 'carbohydrate'
    FIBER = 'fiber'
    CALCIUM = 'calcium'
    IRON = 'iron'
    COST = 'cost'
    CALORIES = 'calories'


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    boiling_factor = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    fiber = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calcium = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    iron = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calories = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fatsecret_name = models.CharField(max_length=200, blank=True)
    fatsecret_id = models.CharField(max_length=200, blank=True)
    fatsecret_json = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    @property
    def protein(self):
        return self._get_ingredients_attribute_sum(Field.PROTEIN.value)

    @property
    def fat(self):
        return self._get_ingredients_attribute_sum(Field.FAT.value)

    @property
    def carbohydrate(self):
        return self._get_ingredients_attribute_sum(Field.CARBOHYDRATE.value)

    @property
    def fiber(self):
        return self._get_ingredients_attribute_sum(Field.FIBER.value)

    @property
    def calcium(self):
        return self._get_ingredients_attribute_sum(Field.CALCIUM.value)

    @property
    def iron(self):
        return self._get_ingredients_attribute_sum(Field.IRON.value)

    @property
    def cost(self):
        return self._get_ingredients_attribute_sum(Field.COST.value)

    @property
    def calories(self):
        return self._get_ingredients_attribute_sum(Field.CALORIES.value)

    @property
    def weight(self):
        return sum([portion.weight for portion in self._ingredient_portions])

    def _get_ingredients_attribute_sum(self, attribute):
        return sum([
            portion.weight * getattr(portion.ingredient, attribute) / 100
            for portion in self._ingredient_portions
        ])

    @cached_property
    def _ingredient_portions(self):
        return self.recipeingredientportion_set.all()

    def __str__(self):
        return self.name


class RecipeIngredientPortion(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=7, decimal_places=2)


class NutritionDay(models.Model):
    name = models.CharField(max_length=200)
    recipes = models.ManyToManyField(Recipe)

    @property
    def protein(self):
        return self._get_ingredients_attribute_sum(Field.PROTEIN.value)

    @property
    def fat(self):
        return self._get_ingredients_attribute_sum(Field.FAT.value)

    @property
    def carbohydrate(self):
        return self._get_ingredients_attribute_sum(Field.CARBOHYDRATE.value)

    @property
    def fiber(self):
        return self._get_ingredients_attribute_sum(Field.FIBER.value)

    @property
    def calcium(self):
        return self._get_ingredients_attribute_sum(Field.CALCIUM.value)

    @property
    def iron(self):
        return self._get_ingredients_attribute_sum(Field.IRON.value)

    @property
    def cost(self):
        return self._get_ingredients_attribute_sum(Field.COST.value)

    @property
    def calories(self):
        return self._get_ingredients_attribute_sum(Field.CALORIES.value)

    @property
    def weight(self):
        return int(
            sum([r.weight for r in self._recipes]) +
            sum([portion.weight for portion in self._supplementary_ingredient_portions]),
        )

    def _get_ingredients_attribute_sum(self, attribute):
        return round(
            sum([getattr(r, attribute) for r in self._recipes]) +
            sum([
                portion.weight * getattr(portion.ingredient, attribute) / 100
                for portion in self._supplementary_ingredient_portions
            ]),
            1
        )

    @cached_property
    def _recipes(self):
        return self.recipes.all()

    @cached_property
    def _supplementary_ingredient_portions(self):
        return self.supplementaryingredientportion_set.all()

    def __str__(self):
        return (
            self.name or
            f"{', '.join([r.name for r in self.recipes.all()])}"
            or 'Той самий день'
        )


class SupplementaryIngredientPortion(models.Model):
    nutrition_day = models.ForeignKey(NutritionDay, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=7, decimal_places=2)

    @property
    def protein(self):
        return self.ingredient.protein * self.weight / 100

    @property
    def fiber(self):
        return self.ingredient.fiber * self.weight / 100

    @property
    def calcium(self):
        return self.ingredient.calcium * self.weight / 100

    @property
    def cost(self):
        return self.ingredient.cost * self.weight / 100


class Menu(models.Model):
    pass


class MenuNutritionDay(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    nutrition_day = models.ForeignKey(NutritionDay, on_delete=models.CASCADE)
    order_number = models.IntegerField(unique=True)
    last_cooked = models.DateField()


class ShoppingList(models.Model):
    pass


class ShoppingListIngredientPortion(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=7, decimal_places=2)
    is_checked = models.BooleanField(default=False)


class ShoppingListNutritionDay(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    menu_nutrition_day = models.OneToOneField(MenuNutritionDay, on_delete=models.CASCADE)
