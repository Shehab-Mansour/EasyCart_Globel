# Generated by Django 5.1.2 on 2025-04-03 11:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0011_easycart_virtualcart_easycart_beginningweight_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="easycart",
            name="weight",
            field=models.FloatField(default=0),
        ),
    ]
