# Generated by Django 5.1.2 on 2025-04-02 21:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("worker", "0039_alter_admintoken_expires_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admintoken",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 4, 3, 21, 49, 3, 171868, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="workertoken",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 4, 3, 21, 49, 3, 160609, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
