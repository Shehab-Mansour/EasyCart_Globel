# Generated by Django 5.1.2 on 2024-11-11 11:44

# import django.db.models.deletion
# import functions.worker.worker
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        # migrations.CreateModel(
        #     name='Job',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('JobName', models.CharField(max_length=100)),
        #         ('JobDescription', models.CharField(max_length=100)),
        #     ],
        # ),
        # migrations.CreateModel(
        #     name='Worker',
        #     fields=[
        #         ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('workerUserName', models.CharField(max_length=100)),
        #         ('WorkerPassword', models.CharField(max_length=1024)),
        #         ('WorkerName', models.CharField(max_length=100)),
        #         ('WorkerPhone', models.CharField(max_length=11)),
        #         ('WorkerEmail', models.CharField(max_length=100)),
        #         ('WorkerAddress', models.CharField(max_length=100)),
        #         ('WorkerSalary', models.IntegerField(default=0, max_length=10)),
        #         ('WorkerImage', models.ImageField(default='workerPhotos/default/workerImage.png', upload_to=functions.worker.worker.worker_directory_path)),
        #         ('WorkerJobTitle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worker.job')),
        #     ],
        # ),
    ]
