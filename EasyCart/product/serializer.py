from  rest_framework import serializers
from django.contrib.auth.hashers import make_password
import datetime
from rest_framework.views import APIView
from .models import Product,Category,Rate,View
from worker.models import Worker
from django.db.models import Avg



############################# Product #############################
class GetallProductSerializer(serializers.ModelSerializer):
    ProductCategory = serializers.CharField(source='ProductCategory.CategoryName', read_only=True)
    ModifiedBy=serializers.CharField(source='ModifiedBy.WorkerUserName', read_only=True)
    class Meta:
        model = Product
        fields = ['QRNumber','ProductName','ProductPrice','ProductCategory','ProductBrand','ProductDescription','ProductImage','ProductWeight','ProductFasting','ProductBoycott',
                  'ProductTotalRate','ProductDiscount','ProductAvailable','ExpiryDate','ModifiedBy','ModifiedDate',
                  ]

class ProductSerializer(serializers.ModelSerializer):
    ProductCategory = serializers.CharField(source='ProductCategory.CategoryName', read_only=True)
    ModifiedBy=serializers.CharField(source='ModifiedBy.WorkerUserName', read_only=True)
    class Meta:
        model = Product
        fields = ['QRNumber','ProductName','ProductPrice','ProductCategory','ProductBrand','ProductDescription','ProductImage','ProductWeight','ProductFasting','ProductBoycott',
                  'ProductTotalRate','ProductDiscount','ProductAvailable','ExpiryDate','ModifiedBy','ModifiedDate',
                  ]
    def update(self, instance, validated_data):
        category_name = validated_data.pop('ProductCategory', None)
        if category_name:
            try:
                category = Category.objects.get(CategoryName=category_name)
                instance.ProductCategory = category
            except Category.DoesNotExist:
                raise serializers.ValidationError({"ProductCategory": "Category not found"})

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

class NewProductSerializer(serializers.ModelSerializer):
    ProductCategory = serializers.CharField(write_only=True)
    ModifiedBy = serializers.CharField(write_only=True)
    class Meta:
        model = Product
        exclude = ['ModifiedDate']
    def create(self, validated_data):
        category_name = validated_data.pop('ProductCategory', None)
        worker_username = validated_data.pop('ModifiedBy', None)
        try:
            category = Category.objects.get(CategoryName=category_name)
        except Category.DoesNotExist:
            raise serializers.ValidationError({"ProductCategory": "Category not found"})
        try:
            worker = Worker.objects.get(WorkerUserName=worker_username)
        except Worker.DoesNotExist:
            raise serializers.ValidationError({"ModifiedBy": "Worker not found"})
        product = Product.objects.create(ProductCategory=category, ModifiedBy=worker, **validated_data)
        return product
############################# Product #############################


############################# Category #############################
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['CategoryName','CategoryImage']
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
    def create(self, validated_data):
        instance = Category(**validated_data)
        instance.save()
        return instance

class AllProductsInCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['ProductCategory','CategoryName']
        # fields='__all__'
############################# Category #############################


#############################   Rate   #############################
class RateSerializer(serializers.ModelSerializer):
    ProductName = serializers.CharField(source='ProductName.ProductName', read_only=True)
    ClientUserName = serializers.CharField(source='ClientUserName.clientUserName', read_only=True)
    ClientName=serializers.SerializerMethodField()
    RatingTime = serializers.SerializerMethodField()
    class Meta:
        model = Rate
        fields = ['ClientUserName','ClientName','ProductName', 'RateValue', 'Comment', 'RatingTime']
        read_only_fields = ['RatingTime']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
    def get_ClientName(self, obj):
        first_name = obj.ClientUserName.clientFirstName
        last_name = obj.ClientUserName.clientLastName
        return f"{first_name} {last_name}"
    def get_RatingTime(self, obj):
        return obj.RatingTime.strftime("%Y/%m/%d")

class NewRateSerializer(serializers.ModelSerializer):
    RatingTime = serializers.SerializerMethodField()
    class Meta:
        model = Rate
        fields = ['ProductName', 'ClientUserName', 'RateValue', 'Comment', 'RatingTime']
        read_only_fields = ['RatingTime']  # Ensure RatingTime is set automatically
    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance
    def get_RatingTime(self, obj):
        return obj.RatingTime.strftime("%d/%m/%Y")

############################# END Rate #############################

#############################   View   #############################
class ViewSerializer(serializers.ModelSerializer):
    ProductName = serializers.CharField(source="ProductName.ProductName", read_only=True)
    ClientName = serializers.SerializerMethodField()
    LastView=serializers.SerializerMethodField()
    ClientUserName=serializers.SerializerMethodField()
    class Meta:
        model = View
        fields = ['ProductName','ClientUserName','ClientName', 'ViewNumber', 'LastView']
    def get_ClientName(self, obj):
        return f"{obj.ClientUserName.clientFirstName} {obj.ClientUserName.clientLastName}"
    def get_LastView(self, obj):
        return obj.LastView.strftime("%d/%m/%Y %H:%M:%S")
    def get_ClientUserName(self, obj):
        return f"{obj.ClientUserName.clientUserName}"

############################# END View   #############################
