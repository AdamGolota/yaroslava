# Generated by Django 4.2.4 on 2023-08-30 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_ingredient_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='boiling_factor',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
        ),
    ]
