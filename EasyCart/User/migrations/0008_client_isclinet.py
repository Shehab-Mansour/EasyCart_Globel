# Generated by Django 5.1.2 on 2025-03-17 22:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("User", "0007_alter_client_clientusername"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="IsClinet",
            field=models.BooleanField(default=True),
        ),
    ]
