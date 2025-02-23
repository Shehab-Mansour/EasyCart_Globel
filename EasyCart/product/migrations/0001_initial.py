# Generated by Django 5.1.2 on 2024-11-19 22:58

import django.core.validators
import django.db.models.deletion
import functions.product.produact
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0007_alter_client_clientusername'),
        ('worker', '0012_alter_worker_workersalary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryName', models.CharField(max_length=120, unique=True)),
                ('CategoryImage', models.ImageField(default='CategoryPhotos/CategoryDefaultPhoto.png', upload_to=functions.product.produact.category_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductName', models.CharField(max_length=100)),
                ('ProductPrice', models.FloatField()),
                ('ProductDescription', models.TextField()),
                ('ProductImage', models.ImageField(default='ProductPhotos/ProductDefaultPhoto.png', upload_to=functions.product.produact.product_directory_path)),
                ('ProductWeight', models.FloatField()),
                ('ProductBrand', models.CharField(max_length=120)),
                ('ProductFasting', models.BooleanField()),
                ('ProductBoycott', models.BooleanField()),
                ('NumberOfViews', models.IntegerField()),
                ('ProductPlace', models.CharField(max_length=12)),
                ('AICode', models.CharField(max_length=12)),
                ('ProductTotalRate', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('ProductDiscount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('ProductQuantity', models.IntegerField()),
                ('ProductAvailable', models.BooleanField()),
                ('QRNumber', models.CharField(max_length=25)),
                ('ModifiedDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('ModifiedBy', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='ProductModifiedBy', to='worker.worker')),
                ('ProductCategory', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='ProductCategory', to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LastView', models.DateTimeField(auto_now_add=True)),
                ('ViewNumber', models.IntegerField()),
                ('ClientUserName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.client')),
                ('ProductName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RateValue', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('Comment', models.TextField(blank=True, null=True)),
                ('RatingTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('ClientUserName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.client')),
                ('ProductName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'indexes': [models.Index(fields=['ProductName', 'ClientUserName'], name='product_rat_Product_3792ab_idx')],
                'unique_together': {('ProductName', 'ClientUserName')},
            },
        ),
    ]
