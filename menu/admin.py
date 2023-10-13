from decimal import Decimal

from django.contrib import admin
from django.db.models import F

from . import models


# Register your models here.

class IngredientAdmin(admin.ModelAdmin):
    model = models.Ingredient
    list_per_page = 150
    list_editable = ['fatsecret_name']
    list_display = [
        'name',
        'protein_per_fiber',
        'protein',
        'fat',
        'carbohydrate',
        'fiber_cost',
        'fiber',
        'cost',
        'carbohydrate',
        'calcium',
        'fatsecret_name',
    ]
    list_display_links = ['name']

    def get_queryset(self, request):
        return super(IngredientAdmin, self).get_queryset(request).annotate(
            protein_per_fiber=F('protein') / F('fiber')
        ).annotate(
            protein_per_cost=F('protein') / F('cost')
        ).annotate(
            protein_per_fiber_cost=F('protein') / (F('fiber') * F('cost') ** (Decimal('0.5')))
        ).annotate(
            protein_per_fiber_carbo_cost=(
                F('protein') /
                (
                    F('fiber') *
                    F('carbohydrate') ** (Decimal('0.5')) *
                    F('cost') ** (Decimal('0.5'))
                )
            )
        ).annotate(
            fiber_cost=F('fiber') * F('cost') ** (Decimal('0.5'))
        ).annotate(
            carbo_per_fiber=F('carbohydrate') / F('fiber')
        )

    def protein_per_fiber(self, obj):
        return round(obj.protein_per_fiber, 1) if obj.protein_per_fiber else obj.protein_per_fiber

    def protein_per_cost(self, obj):
        return (
            round(obj.protein_per_cost, 1)
            if obj.protein_per_cost
            else obj.protein_per_cost
        )

    def protein_per_fiber_cost(self, obj):
        return (
            round(obj.protein_per_fiber_cost * 10, 1)
            if obj.protein_per_fiber_cost
            else obj.protein_per_fiber_cost
        )

    def protein_per_fiber_carbo_cost(self, obj):
        return (
            round(obj.protein_per_fiber_carbo_cost * 10, 1)
            if obj.protein_per_fiber_carbo_cost
            else obj.protein_per_fiber_carbo_cost
        )

    def fiber_cost(self, obj):
        return (
            round(obj.fiber_cost * 10, 1)
            if obj.fiber_cost
            else obj.fiber_cost
        )

    def carbo_per_fiber(self, obj):
        return (
            round(obj.carbo_per_fiber, 2)
            if obj.carbo_per_fiber
            else obj.carbo_per_fiber
        )

    protein_per_fiber.admin_order_field = 'protein_per_fiber'
    protein_per_cost.admin_order_field = 'protein_per_cost'
    protein_per_fiber_cost.admin_order_field = 'protein_per_fiber_cost'
    protein_per_fiber_carbo_cost.admin_order_field = 'protein_per_fiber_carbo_cost'
    fiber_cost.admin_order_field = 'fiber_cost'
    carbo_per_fiber.admin_order_field = 'carbo_per_fiber'


class RecipeIngredientPortionInline(admin.TabularInline):
    model = models.RecipeIngredientPortion


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ["protein", "fat", "carbohydrate", "fiber", "calcium", "iron", "cost"]
    inlines = [RecipeIngredientPortionInline]


class SupplementaryIngredientPortionInline(admin.TabularInline):
    model = models.SupplementaryIngredientPortion
    readonly_fields = ['protein', 'fiber', 'cost', 'calcium']


class NutritionDayAdmin(admin.ModelAdmin):
    model = models.NutritionDay
    save_as = True
    readonly_fields = [
        "protein", "fat", "carbohydrate", "fiber", "calcium", "iron", "calories", "cost", "weight"
    ]
    inlines = [SupplementaryIngredientPortionInline]


admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.NutritionDay, NutritionDayAdmin)
