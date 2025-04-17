from django.contrib import admin
from .models import VirtualCart, VirtualCartItem, EasyCartVirtualCart, EasyCart, EasyCartVirtualCartItem, PurchasedCart, \
    PurchasedCartItem

# Register your models here.

admin.site.register(VirtualCart)
admin.site.register(VirtualCartItem)

admin.site.register(EasyCart)
admin.site.register(EasyCartVirtualCart)

admin.site.register(EasyCartVirtualCartItem)

admin.site.register(PurchasedCart)
admin.site.register(PurchasedCartItem)



