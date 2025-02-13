# Generated by Django 5.1.2 on 2024-11-11 21:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0002_rename_workerusername_worker_workerusername'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_tokens', to='worker.worker')),
            ],
        ),
    ]
