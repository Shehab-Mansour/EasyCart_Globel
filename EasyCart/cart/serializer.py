# cart/serializers.py
from rest_framework import serializers
from .models import (
    EasyCart, VirtualCart, VirtualCartItem,
    EasyCartVirtualCart, EasyCartVirtualCartItem,
    PurchasedCart, PurchasedCartItem
)
from product.models import Product
from User.serializer import ClientSerializer


class ProductSerializer(serializers.ModelSerializer):
    ProductCategory = serializers.CharField(source='ProductCategory.CategoryName', read_only=True)
    class Meta:
        model = Product
        fields = ['QRNumber','ProductName','ProductPrice','ProductDiscount','ProductCategory','ProductBrand','ProductImage','ProductWeight','ProductPlace' ]


class EasyCartSerializer(serializers.ModelSerializer):
    lastUsedBy = ClientSerializer(read_only=True)

    class Meta:
        model = EasyCart
        fields = [
            'cartId', 'cartStatus', 'batteryPercentage',
            'location', 'lastUsedBy', 'lastUsedAt',
            'createdAt', 'updatedAt' ,'lastMaintenanceTime'
        ]
        read_only_fields = ['cartId', 'createdAt', 'updatedAt']


class VirtualCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    qr_number = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        source='product',
        slug_field='QRNumber',
        write_only=True
    )
    total_price = serializers.SerializerMethodField()
    total_weight = serializers.SerializerMethodField()

    class Meta:
        model = VirtualCartItem
        fields = [
            'product', 'qr_number', 'quantity',
            'total_price', 'total_weight', 'addedAt', 'updatedAt'
        ]
        read_only_fields = ['id', 'addedAt', 'updatedAt']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.ProductPrice * (1 - obj.product.ProductDiscount / 100)

    def get_total_weight(self, obj):
        return obj.quantity * obj.product.ProductWeight


# class VirtualCartSerializer(serializers.ModelSerializer):
#     items = VirtualCartItemSerializer(many=True, read_only=True)
#     # client = ClientSerializer(read_only=True)
#
#     class Meta:
#         model = VirtualCart
#         fields = [
#             'cartId', 'qrCode', 'isActive','totalQuantity',
#             'totalPrice', 'totalWeight',
#              'createdAt', 'updatedAt','items'
#         ]
#         read_only_fields = ['cartId','items','createdAt', 'updatedAt']
# class VirtualCartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VirtualCartItem
#         fields = ['id', 'product', 'quantity', 'total_price', 'total_weight', 'addedAt', 'updatedAt']

class VirtualCartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()  # تحويل `items` إلى قاموس

    class Meta:
        model = VirtualCart
        fields = [
             'qrCode', 'isActive', 'totalQuantity',
            'totalPrice', 'totalWeight', 'createdAt', 'updatedAt', 'items'
        ]
        read_only_fields = ['cartId', 'items', 'createdAt', 'updatedAt']

    def get_items(self, obj):
        """ترقيم العناصر وإرجاعها كقاموس {1: {...}, 2: {...}, ...}"""
        items = obj.items.all().order_by('id')  # ترتيب العناصر حسب ID
        return {index + 1: VirtualCartItemSerializer(item).data for index, item in enumerate(items)}

class VirtualCartSerializerData(serializers.ModelSerializer):
    class Meta:
        model = VirtualCart
        fields = [
            'cartId', 'qrCode', 'isActive',
            'totalPrice', 'totalWeight', 'totalQuantity',
            'createdAt', 'updatedAt'
        ]
class EasyCartVirtualCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    qr_number = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        source='product',
        slug_field='QRNumber',
        write_only=True
    )
    total_price = serializers.SerializerMethodField()
    total_weight = serializers.SerializerMethodField()

    class Meta:
        model = EasyCartVirtualCartItem
        fields = [
            'product', 'qr_number', 'quantity',
            'total_price', 'total_weight', 'addedAt', 'updatedAt'
        ]
        read_only_fields = ['id', 'addedAt', 'updatedAt']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.ProductPrice * (1 - obj.product.ProductDiscount / 100)

    def get_total_weight(self, obj):
        return obj.quantity * obj.product.ProductWeight


class EasyCartVirtualCartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    # client = ClientSerializer(read_only=True)
    # easyCart = EasyCartSerializer(read_only=True)

    class Meta:
        model = EasyCartVirtualCart
        fields = [
            'isActive',
            # 'cartId', 'easyCart', 'client',
            'totalPrice', 'totalWeight', 'totalQuantity',
            'items', 'createdAt', 'updatedAt'
        ]
        read_only_fields = ['cartId', 'easyCart','client','createdAt', 'updatedAt']

    def get_items(self, obj):
        items = obj.items.all().order_by('id')
        return {index + 1: EasyCartVirtualCartItemSerializer(item).data for index, item in enumerate(items)}


class PurchasedCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    total_weight = serializers.SerializerMethodField()

    class Meta:
        model = PurchasedCartItem
        fields = [
            'product', 'quantity', 'priceAtPurchase',
            'total_price', 'total_weight', 'purchasedAt'
        ]
        read_only_fields = ['purchasedAt']

    def get_total_price(self, obj):
        return obj.quantity * obj.priceAtPurchase

    def get_total_weight(self, obj):
        return obj.quantity * obj.product.ProductWeight


class PurchasedCartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    # client = ClientSerializer(read_only=True)

    class Meta:
        model = PurchasedCart
        fields = [
            'totalAmount', 'totalWeight',
            'totalQuantity', 'paymentMethod', 'nfcTransactionId',
            'items', 'createdAt'
        ]
        read_only_fields = ['cartId', 'createdAt']

    def get_items(self, obj):
        items = obj.items.all().order_by('id')
        return {index + 1: EasyCartVirtualCartItemSerializer(item).data for index, item in enumerate(items)}

class AdminPurchasedCartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    client = ClientSerializer(read_only=True)

    class Meta:
        model = PurchasedCart
        fields = [
            'client','totalAmount', 'totalWeight',
            'totalQuantity', 'paymentMethod', 'nfcTransactionId',
            'items', 'createdAt'
        ]
        read_only_fields = ['cartId', 'createdAt']

    def get_items(self, obj):
        items = obj.items.all().order_by('id')
        return {index + 1: EasyCartVirtualCartItemSerializer(item).data for index, item in enumerate(items)}
