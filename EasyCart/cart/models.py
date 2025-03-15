from django.db import models
import datetime
from User.models import client
from product.models import Product , Category
from django.db.models import Index

# Create your models here.




class VirtualCart(models.Model):
    VCId = models.AutoField(primary_key=True)
    Client=models.ForeignKey(client,related_name="UserName",on_delete=models.SET("deleted user"))
    VCQuantity = models.FloatField(default=0.0)
    VCTotalPrice = models.FloatField(default=0.0)
    VCTotalWeight = models.FloatField(default=0.0)



    VCQRCode=models.CharField(max_length=11,default='')
    VCPINcode = models.CharField(max_length=6,default='')
    VCStatus = models.BooleanField(default=False)
    """
    لو ترو معناها ان الكارت اتعملها اسكان من الكارت الحقيقية
    واليوز ميعرفش يضيف حاجة تاني 
     
     """
    VCDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.Client.clientUserName


class VirtualCartItems(models.Model):
    VCItimeID = models.ForeignKey(VirtualCart, on_delete=models.CASCADE)
    Product=models.ForeignKey(Product,on_delete=models.CASCADE)
    Quantity=models.FloatField(default=0.0)
    Price=models.FloatField(default=0.0)
    Weight=models.FloatField(default=0.0)
    ProductName=models.CharField(max_length=100,default='')
    CategoryName=models.CharField(max_length=100,default='')

    class Meta:
        unique_together = (('Product', 'VCItimeID'),)
        indexes = [
            Index(fields=['Product', 'VCItimeID']),
        ]
    def __str__(self):
        return self.ProductName


class EasyCart(models.Model):
    EasyCartID = models.AutoField(primary_key=True)
    ECStatus = models.BooleanField(default=False)
    
