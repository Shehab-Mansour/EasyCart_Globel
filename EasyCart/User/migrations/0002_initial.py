# Generated by Django 5.1.2 on 2025-04-17 14:20

import datetime
import django.db.models.deletion
import functions.user.client
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("User", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("clientUserName", models.CharField(max_length=50, unique=True)),
                ("clientPassword", models.CharField(max_length=500)),
                (
                    "clientFirstName",
                    models.CharField(default="YourFirstName", max_length=50),
                ),
                (
                    "clientLastName",
                    models.CharField(default="YourLastName", max_length=50),
                ),
                ("clientEmail", models.CharField(default="<EMAIL>", max_length=100)),
                ("clientPhone", models.CharField(default="01234567890", max_length=11)),
                (
                    "clientGender",
                    models.CharField(
                        choices=[
                            ("male", "male"),
                            ("female", "female"),
                            ("other", "other"),
                        ],
                        default="male",
                        max_length=10,
                    ),
                ),
                ("clientBirthdate", models.DateField(default=datetime.date.today)),
                ("clientMoney", models.IntegerField(default=0)),
                ("clientPoints", models.IntegerField(default=0)),
                (
                    "clientImage",
                    models.ImageField(
                        default="clientPhotos/default/clientImage.png",
                        upload_to=functions.user.client.client_directory_path,
                    ),
                ),
                ("IsClient", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="ClientToken",
            fields=[
                (
                    "key",
                    models.CharField(max_length=40, primary_key=True, serialize=False),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_tokens",
                        to="User.client",
                    ),
                ),
            ],
        ),
    ]
