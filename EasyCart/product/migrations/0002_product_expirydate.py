# Generated by Django 5.1.2 on 2024-11-20 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ExpiryDate',
            field=models.DateField(default='2030-01-01'),
        ),
    ]
