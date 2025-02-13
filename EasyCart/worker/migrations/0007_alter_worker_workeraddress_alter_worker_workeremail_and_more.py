# Generated by Django 5.1.2 on 2024-11-12 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0006_alter_workertoken_worker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='WorkerAddress',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='WorkerEmail',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='WorkerPhone',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='WorkerUserName',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
