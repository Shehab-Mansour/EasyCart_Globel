# Generated by Django 5.1.2 on 2025-03-15 03:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("worker", "0021_admintoken_role_workertoken_role_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="admin",
            name="IsSuperAdmin",
            field=models.BooleanField(default=False),
        ),
    ]
