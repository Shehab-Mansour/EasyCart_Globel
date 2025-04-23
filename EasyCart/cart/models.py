import uuid


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from User.models import client
from product.models import Product
from django.db.models.signals import pre_save
from django.dispatch import receiver

# class EasyCart(models.Model):
#     cartId = models.CharField(max_length=50, unique=True, primary_key=True)
#     cartStatus = models.CharField(max_length=20, choices=[
#         ('ready', 'Ready'),
#         ('in_use', 'In Use'),
#         ('error', 'Error')
#     ], default='ready')
#     batteryPercentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
#     location = models.CharField(max_length=50)  # Store location/aisle
#     lastUsedBy = models.ForeignKey(client, on_delete=models.SET_NULL, null=True, blank=True)
#     lastUsedAt = models.DateTimeField(null=True, blank=True)
#     createdAt = models.DateTimeField(auto_now_add=True)
#     updatedAt = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"Cart {self.cartId} - {self.cartStatus}"


# Virtual Cart (Mobile App)
class VirtualCart(models.Model):
    cartId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(client, on_delete=models.CASCADE)
    qrCode = models.CharField(max_length=100, unique=True, null=True, blank=True)
    isActive = models.BooleanField(default=True)
    totalPrice = models.FloatField(default=0.0)
    totalWeight = models.FloatField(default=0.0)
    totalQuantity = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.clientUserName}'s Virtual Cart"

    def update_totals(self):
        items = self.items.all()
        self.totalPrice = sum(item.quantity * item.product.ProductPrice for item in items)
        self.totalWeight = sum(item.quantity * item.product.ProductWeight for item in items)
        self.totalQuantity = sum(item.quantity for item in items)
        self.save()

class VirtualCartItem(models.Model):
    cart = models.ForeignKey(VirtualCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='QRNumber')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    addedAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.ProductName} in Virtual Cart"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_totals()



class EasyCart(models.Model):
    cartId = models.CharField(max_length=50, unique=True, primary_key=True, editable=False)
    cartStatus = models.CharField(max_length=20, choices=[
        ('ready', 'Ready'),
        ('in_use', 'In Use'),
        ('error', 'Error')
    ], default='ready')
    batteryPercentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    location = models.CharField(max_length=50)  # Store location/aisle
    lastUsedBy = models.ForeignKey(client, on_delete=models.SET_NULL, null=True, blank=True)
    lastUsedAt = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    beginningWeight=models.FloatField(default=0)
    weight=models.FloatField(default=0)
    numberOfItems=models.IntegerField(default=0)
    VirtualCart=models.ForeignKey(VirtualCart, on_delete=models.SET_NULL, null=True, blank=True)
    lastMaintenanceTime=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.cartId} - {self.cartStatus}"

# دالة لتوليد `cartId` تلقائيًا بتنسيق EasyCart000
def generate_cart_id():
    last_cart = EasyCart.objects.order_by('-cartId').first()  # جلب آخر كارت تم إنشاؤه
    if last_cart and last_cart.cartId.startswith("EasyCart"):
        last_id = int(last_cart.cartId.replace("EasyCart", ""))  # استخراج الرقم
        new_id = f"EasyCart{last_id + 1:03d}"  # زيادة الرقم وتنسيقه بـ 3 خانات
    else:
        new_id = "EasyCart001"  # أول كارت في النظام
    return new_id

# إشارة لحفظ `cartId` قبل تخزين الكائن
@receiver(pre_save, sender=EasyCart)
def set_cart_id(sender, instance, **kwargs):
    if not instance.cartId:  # إذا لم يتم تعيين cartId مسبقًا
        instance.cartId = generate_cart_id()

# EasyCart Virtual Cart (Before Product Addition)
class EasyCartVirtualCart(models.Model):
    cartId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(client, on_delete=models.CASCADE)
    easyCart = models.ForeignKey(EasyCart, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
    totalPrice = models.FloatField(default=0.0)
    totalWeight = models.FloatField(default=0.0)
    totalQuantity = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.clientUserName}'s EasyCart Virtual Cart"

    def update_totals(self):
        items = self.items.all()
        self.totalPrice = sum(item.quantity * item.product.ProductPrice for item in items)
        self.totalWeight = sum(item.quantity * item.product.ProductWeight for item in items)
        self.totalQuantity = sum(item.quantity for item in items)
        self.save()

class EasyCartVirtualCartItem(models.Model):
    cart = models.ForeignKey(EasyCartVirtualCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='QRNumber')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    addedAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.ProductName} in EasyCart Virtual Cart"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_totals()

# Purchased Cart (History)
class PurchasedCart(models.Model):
    cartId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(client, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=timezone.now)
    totalAmount = models.FloatField()
    totalWeight = models.FloatField()
    totalQuantity = models.IntegerField()
    paymentMethod = models.CharField(max_length=50)
    nfcTransactionId = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.client.clientUserName}'s Purchased Cart - {self.createdAt}"

class PurchasedCartItem(models.Model):
    cart = models.ForeignKey(PurchasedCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='QRNumber')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    priceAtPurchase = models.FloatField()
    purchasedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quantity}x {self.product.ProductName} in Purchased Cart"


