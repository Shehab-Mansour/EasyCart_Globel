# # cart/views.py
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.shortcuts import get_object_or_404
# from django.db import transaction
# from django.core.exceptions import ValidationError
# from decimal import Decimal
# from .models import (
#     EasyCart, VirtualCart, VirtualCartItem,
#     EasyCartVirtualCart, EasyCartVirtualCartItem,
#     PurchasedCart, PurchasedCartItem
# )
# from .serializer import (
#     EasyCartSerializer, VirtualCartSerializer, VirtualCartItemSerializer,
#     EasyCartVirtualCartSerializer, EasyCartVirtualCartItemSerializer,
#     PurchasedCartSerializer
# )
# from User.permission import IsClientUser
# from User.views import login
# from product.models import Product
#
#
# class BaseCartViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated, IsClientUser]
#
#     def handle_exception(self, exc):
#         if isinstance(exc, ValidationError):
#             return Response(
#                 {'error': str(exc)},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         return super().handle_exception(exc)
#
#
# class VirtualCartViewSet(BaseCartViewSet):
#     serializer_class = VirtualCartSerializer
#
#     def get_queryset(self):
#         return VirtualCart.objects.filter(client=self.request.user, isActive=True)
#
#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)
#
#     @action(detail=True, methods=['post'])
#     def add_item(self, request, pk=None):
#         try:
#             with transaction.atomic():
#                 cart = self.get_object()
#                 qr_number = request.data.get('qr_number')
#                 quantity = int(request.data.get('quantity', 1))
#
#                 if quantity <= 0:
#                     raise ValidationError('Quantity must be positive')
#
#                 product = get_object_or_404(Product, QRNumber=qr_number)
#
#                 if not product.ProductAvailable:
#                     raise ValidationError('Product is not available')
#
#                 cart_item, created = VirtualCartItem.objects.get_or_create(
#                     cart=cart,
#                     product=product,
#                     defaults={'quantity': quantity}
#                 )
#
#                 if not created:
#                     cart_item.quantity += quantity
#                     cart_item.save()
#
#                 return Response(self.get_serializer(cart).data)
#
#         except Exception as e:
#             return self.handle_exception(e)
#
#     @action(detail=True, methods=['put'])
#     def update_item(self, request, pk=None, item_id=None):
#         try:
#             with transaction.atomic():
#                 cart = self.get_object()
#                 cart_item = get_object_or_404(VirtualCartItem, id=item_id, cart=cart)
#
#                 quantity = int(request.data.get('quantity', cart_item.quantity))
#
#                 if quantity <= 0:
#                     raise ValidationError('Quantity must be positive')
#
#                 cart_item.quantity = quantity
#                 cart_item.save()
#
#                 return Response(self.get_serializer(cart).data)
#
#         except Exception as e:
#             return self.handle_exception(e)
#
#     @action(detail=True, methods=['delete'])
#     def remove_item(self, request, pk=None, item_id=None):
#         try:
#             with transaction.atomic():
#                 cart = self.get_object()
#                 cart_item = get_object_or_404(VirtualCartItem, id=item_id, cart=cart)
#                 cart_item.delete()
#                 return Response(self.get_serializer(cart).data)
#         except Exception as e:
#             return self.handle_exception(e)
#
#     @action(detail=True, methods=['post'])
#     def generate_qr(self, request, pk=None):
#         try:
#             cart = self.get_object()
#             cart.qrCode = f"VC-{cart.cartId}"
#             cart.save()
#             return Response({'qr_code': cart.qrCode})
#         except Exception as e:
#             return self.handle_exception(e)
#
#
# class EasyCartViewSet(BaseCartViewSet):
#     queryset = EasyCart.objects.all()
#     serializer_class = EasyCartSerializer
#
#     @action(detail=True, methods=['post'])
#     def update_status(self, request, pk=None):
#         try:
#             cart = self.get_object()
#             status = request.data.get('status')
#             if status not in dict(EasyCart._meta.get_field('cartStatus').choices):
#                 raise ValidationError('Invalid status')
#
#             cart.cartStatus = status
#             cart.save()
#             return Response(self.get_serializer(cart).data)
#         except Exception as e:
#             return self.handle_exception(e)
#
#     @action(detail=True, methods=['post'])
#     def update_battery(self, request, pk=None):
#         try:
#             cart = self.get_object()
#             battery = int(request.data.get('battery_percentage'))
#             if not 0 <= battery <= 100:
#                 raise ValidationError('Battery percentage must be between 0 and 100')
#
#             cart.batteryPercentage = battery
#             cart.save()
#             return Response(self.get_serializer(cart).data)
#         except Exception as e:
#             return self.handle_exception(e)
#
#     @action(detail=True, methods=['post'])
#     def update_location(self, request, pk=None):
#         try:
#             cart = self.get_object()
#             location = request.data.get('location')
#             if not location:
#                 raise ValidationError('Location is required')
#
#             cart.location = location
#             cart.save()
#             return Response(self.get_serializer(cart).data)
#         except Exception as e:
#             return self.handle_exception(e)
#
#
# class EasyCartVirtualCartViewSet(BaseCartViewSet):
#     serializer_class = EasyCartVirtualCartSerializer
#
#     def get_queryset(self):
#         return EasyCartVirtualCart.objects.filter(client=self.request.user, isActive=True)
#
#     def perform_create(self, serializer):
#         serializer.save(client=self.request.user)
#
#     @action(detail=False, methods=['post'])
#     def verify_qr(self, request):
#         try:
#             qr_code = request.data.get('qr_code')
#             easy_cart_id = request.data.get('easy_cart_id')
#
#             if not qr_code or not easy_cart_id:
#                 raise ValidationError('QR code and easy cart ID are required')
#
#             virtual_cart = get_object_or_404(VirtualCart, qrCode=qr_code, isActive=True)
#             login_response = login(request)
#
#             if login_response.status_code != status.HTTP_200_OK:
#                 return login_response
#
#             easy_cart = get_object_or_404(EasyCart, cartId=easy_cart_id)
#
#             with transaction.atomic():
#                 cart, created = EasyCartVirtualCart.objects.get_or_create(
#                     client=request.user,
#                     easyCart=easy_cart,
#                     isActive=True
#                 )
#
#                 for item in virtual_cart.items.all():
#                     EasyCartVirtualCartItem.objects.create(
#                         cart=cart,
#                         product=item.product,
#                         quantity=item.quantity
#                     )
#
#             return Response({
#                 'tokens': login_response.data,
#                 'cart': self.get_serializer(cart).data
#             })
#         except Exception as e:
#             return self.handle_exception(e)
#
#     @action(detail=True, methods=['post'])
#     def add_item(self, request, pk=None):
#         try:
#             with transaction.atomic():
#                 cart = self.get_object()
#                 qr_number = request.data.get('qr_number')
#                 quantity = int(request.data.get('quantity', 1))
#
#                 if quantity <= 0:
#                     raise ValidationError('Quantity must be positive')
#
#                 product = get_object_or_404(Product, QRNumber=qr_number)
#
#                 if not product.ProductAvailable:
#                     raise ValidationError('Product is not available')
#
#                 if quantity > product.ProductQuantity:
#                     raise ValidationError(f'Insufficient stock. Available: {product.ProductQuantity}')
#
#                 cart_item, created = EasyCartVirtualCartItem.objects.get_or_create(
#                     cart=cart,
#                     product=product,
#                     defaults={'quantity': quantity}
#                 )
#
#                 if not created:
#                     cart_item.quantity += quantity
#                     cart_item.save()
#
#                 product.ProductQuantity -= quantity
#                 product.save()
#
#                 return Response(self.get_serializer(cart).data)
#         except Exception as e:
#             return self.handle_exception(e)
#
#     @action(detail=True, methods=['post'])
#     def complete_purchase(self, request, pk=None):
#         try:
#             with transaction.atomic():
#                 cart = self.get_object()
#                 payment_method = request.data.get('payment_method')
#                 nfc_transaction_id = request.data.get('nfc_transaction_id')
#
#                 if not payment_method:
#                     raise ValidationError('Payment method is required')
#
#                 purchase = PurchasedCart.objects.create(
#                     client=request.user,
#                     totalAmount=cart.totalPrice,
#                     totalWeight=cart.totalWeight,
#                     totalQuantity=cart.totalQuantity,
#                     paymentMethod=payment_method,
#                     nfcTransactionId=nfc_transaction_id
#                 )
#
#                 for item in cart.items.all():
#                     PurchasedCartItem.objects.create(
#                         cart=purchase,
#                         product=item.product,
#                         quantity=item.quantity,
#                         priceAtPurchase=item.product.ProductPrice
#                     )
#
#                 cart.isActive = False
#                 cart.save()
#                 VirtualCart.objects.filter(client=request.user, isActive=True).update(isActive=False)
#
#                 return Response(PurchasedCartSerializer(purchase).data)
#         except Exception as e:
#             return self.handle_exception(e)
#
#
# class PurchasedCartViewSet(BaseCartViewSet):
#     serializer_class = PurchasedCartSerializer
#
#     def get_queryset(self):
#         return PurchasedCart.objects.filter(client=self.request.user)
#
#     @action(detail=True, methods=['get'])
#     def list_items(self, request, pk=None):
#         try:
#             cart = self.get_object()
#             items = cart.items.all()
#             serializer = PurchasedCartItemSerializer(items, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#             return self.handle_exception(e)

from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import (
    EasyCart, VirtualCart, VirtualCartItem,
    EasyCartVirtualCart, EasyCartVirtualCartItem,
    PurchasedCart, PurchasedCartItem
)
from .serializer import (
    EasyCartSerializer, VirtualCartSerializer, VirtualCartItemSerializer,
    EasyCartVirtualCartSerializer, EasyCartVirtualCartItemSerializer,
    PurchasedCartSerializer, PurchasedCartItemSerializer
)

# EasyCart ViewSet
class EasyCartViewSet(viewsets.ModelViewSet):
    queryset = EasyCart.objects.all()
    serializer_class = EasyCartSerializer
    permission_classes = [IsAuthenticated]

# Virtual Cart Views
class VirtualCartViewSet(viewsets.ModelViewSet):
    queryset = VirtualCart.objects.all()
    serializer_class = VirtualCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VirtualCart.objects.filter(client=self.request.user)

class VirtualCartItemViewSet(viewsets.ModelViewSet):
    queryset = VirtualCartItem.objects.all()
    serializer_class = VirtualCartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.virtualcart)

# EasyCart Virtual Cart Views
class EasyCartVirtualCartViewSet(viewsets.ModelViewSet):
    queryset = EasyCartVirtualCart.objects.all()
    serializer_class = EasyCartVirtualCartSerializer
    permission_classes = [IsAuthenticated]

class EasyCartVirtualCartItemViewSet(viewsets.ModelViewSet):
    queryset = EasyCartVirtualCartItem.objects.all()
    serializer_class = EasyCartVirtualCartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(cart=self.request.user.easycartvirtualcart)

# Purchased Cart Views
class PurchasedCartViewSet(viewsets.ModelViewSet):
    queryset = PurchasedCart.objects.all()
    serializer_class = PurchasedCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PurchasedCart.objects.filter(client=self.request.user)

class PurchasedCartItemViewSet(viewsets.ModelViewSet):
    queryset = PurchasedCartItem.objects.all()
    serializer_class = PurchasedCartItemSerializer
    permission_classes = [IsAuthenticated]



