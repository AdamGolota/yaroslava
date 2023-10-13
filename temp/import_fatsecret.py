import json
from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property
from pathlib import Path
from time import sleep

import requests

from constants.fatsecret import FATSECRET_API_KEY, FATSECRET_CLIENT_ID
from models import orm


@dataclass
class Serving:
    fields: dict

    def __getitem__(self, item):
        return Decimal(self.fields[item]) * self.factor if item in self.fields else 0

    @cached_property
    def factor(self):
        return 100 / Decimal(self.fields['metric_serving_amount'])


def import_fatsecret():
    token = _get_and_save_token()
    for ingredient in orm.Ingredient.objects.all():
        if not ingredient.fatsecret_id:
            if not ingredient.fatsecret_name:
                continue
            ingredient.fatsecret_id = _find_food_id(token, ingredient.fatsecret_name)
        serving = Serving(
            fields=_get_saved_food(ingredient) or _get_food(token, ingredient.fatsecret_id)
        )
        ingredient.protein = serving['protein'] or ingredient.protein
        ingredient.fat = serving['fat'] or ingredient.fat
        ingredient.carbohydrate = serving['carbohydrate'] or ingredient.carbohydrate
        ingredient.fiber = serving['fiber'] or ingredient.fiber
        ingredient.calcium = serving['calcium'] or ingredient.calcium
        ingredient.iron = serving['iron'] or ingredient.iron
        ingredient.calories = serving['calories'] or ingredient.calories
        ingredient.fatsecret_json = json.dumps(serving.fields)
        ingredient.save()


def _get_saved_food(ingredient: orm.Ingredient):
    if ingredient.fatsecret_json:
        return json.loads(ingredient.fatsecret_json)


def _get_food(auth_token, food_id):
    sleep(1)
    res = requests.post(
        'https://platform.fatsecret.com/rest/server.api',
        headers={'Authorization': f'Bearer {auth_token}'},
        params={
            'method': 'food.get.v3',
            'food_id': food_id,
            'format': 'json',
        }
    )
    servings = res.json()['food']['servings']['serving']
    for serving in servings:
        if serving['serving_description'] == '100 g':
            return serving
    for serving in servings:
        if serving['metric_serving_unit'] == 'g':
            return serving
    for serving in servings:
        if serving['metric_serving_unit'] == 'ml':
            return serving
    raise


def _find_food_id(auth_token, name_to_find):
    res = requests.post(
        'https://platform.fatsecret.com/rest/server.api',
        headers={'Authorization': f'Bearer {auth_token}'},
        params={
            'method': 'foods.search',
            'search_expression': name_to_find,
            'format': 'json',
        }
    )
    for food in res.json()['foods']['food']:
        full_name = (
            food['food_name'] +
            (f"  ({food['brand_name']})" if 'brand_name' in food else '')
        )
        if full_name == name_to_find:
            return food['food_id']
    raise


def _get_and_save_token():
    Path('token').touch()
    with open('token', 'r+') as f:
        token = f.read() or _get_new_token()
    with open('token', 'w') as f:
        f.write(token)
    return token


def _get_new_token():
    data = {
        'grant_type': 'client_credentials',
        'scope': 'basic',
    }

    response = requests.post(
        'https://oauth.fatsecret.com/connect/token',
        data=data,
        auth=(FATSECRET_CLIENT_ID, FATSECRET_API_KEY)
    )
    return response.json()['access_token']


if __name__ == '__main__':
    import_fatsecret()
