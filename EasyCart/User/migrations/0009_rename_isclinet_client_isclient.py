# Generated by Django 5.1.2 on 2025-03-17 22:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("User", "0008_client_isclinet"),
    ]

    operations = [
        migrations.RenameField(
            model_name="client",
            old_name="IsClinet",
            new_name="IsClient",
        ),
    ]
