# Generated by Django 4.2.4 on 2023-08-30 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protein', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('fat', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('carbohydrate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('boiling_factor', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('fiber', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('calcium', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('iron', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MenuNutritionDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(unique=True)),
                ('last_cooked', models.DateField()),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.menu')),
            ],
        ),
        migrations.CreateModel(
            name='NutritionDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SupplementaryIngredientPortion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.ingredient')),
                ('nutrition_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.nutritionday')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingListNutritionDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_nutrition_day', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='menu.menunutritionday')),
                ('shopping_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.shoppinglist')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingListIngredientPortion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('is_checked', models.BooleanField(default=False)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.ingredient')),
                ('shopping_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.shoppinglist')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredientPortion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='nutritionday',
            name='recipes',
            field=models.ManyToManyField(to='menu.recipe'),
        ),
        migrations.AddField(
            model_name='menunutritionday',
            name='nutrition_day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.nutritionday'),
        ),
    ]
