from django.contrib import admin
from .models import *
# Register your models here.

class ProductDisplay(admin.ModelAdmin):
  list_display = ("ProductName", "ProductPrice","ProductWeight","NumberOfViews","ProductTotalRate")

class RateDisplay(admin.ModelAdmin):
  list_display = ("ProductName", "ClientUserName","RateValue","RatingTime")

class ViewDisplay(admin.ModelAdmin):
  list_display = ("ProductName", "ClientUserName","ViewNumber")



admin.site.register(Category)
admin.site.register(Product,ProductDisplay)
admin.site.register(Rate,RateDisplay)
admin.site.register(View,ViewDisplay)