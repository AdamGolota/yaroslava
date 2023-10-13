import csv
from decimal import Decimal

from models import orm


def import_recipes():
    with open('recipes.csv', 'r') as f:
        rows = csv.reader(f)
        while row := next(rows, None):
            if _is_text(row[2]) and not row[1]:
                keys = _get_not_empty(row[2:])
                values = _get_not_empty(next(rows)[2:])
                recipe_name = _read_recipe_name_after_ingredients(rows)
                _import_recipe(recipe_name, tuple(zip(keys, values)))


def _read_recipe_name_after_ingredients(rows):
    for i in range(5):
        next(rows)
    return next(rows)[0]


def _is_text(cell):
    return cell and not cell.isdigit()


def _get_not_empty(row):
    return [v for v in row if v != '']


def _import_recipe(name, row):
    recipe = orm.Recipe.objects.filter(
        name=name
    ).first() or orm.Recipe(name=name)
    recipe.save()
    for ingredient_name, weight in row:
        ingredient = orm.Ingredient.objects.get(name=ingredient_name)
        recipe_ingredient_portion = orm.RecipeIngredientPortion.objects.filter(
            recipe=recipe,
            ingredient=ingredient
        ).first() or orm.RecipeIngredientPortion(
            recipe=recipe,
            ingredient=ingredient,
            weight=Decimal(weight)
        )
        recipe_ingredient_portion.save()


if __name__ == '__main__':
    import_recipes()
