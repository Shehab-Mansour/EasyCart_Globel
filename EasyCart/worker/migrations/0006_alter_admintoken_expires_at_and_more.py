# Generated by Django 5.1.2 on 2025-04-17 20:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("worker", "0005_alter_admintoken_expires_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admintoken",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 4, 18, 20, 20, 13, 234434, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="workertoken",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 4, 18, 20, 20, 13, 234434, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
