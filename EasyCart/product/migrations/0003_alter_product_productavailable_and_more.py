# Generated by Django 5.1.2 on 2025-04-17 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="ProductAvailable",
            field=models.BooleanField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="ProductBoycott",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="ProductFasting",
            field=models.BooleanField(default=False, null=True),
        ),
    ]
