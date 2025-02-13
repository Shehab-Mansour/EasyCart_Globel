from django.core.validators import *
from django.db.models import Index


from functions.product.produact import category_directory_path,product_directory_path
from django.db import models

## models import
from worker.models import Worker
from User.models import client

# Create your models here.


class Category(models.Model):
    CategoryName = models.CharField(max_length=120,unique=True)
    CategoryImage = models.ImageField(upload_to=category_directory_path, default='CategoryPhotos/CategoryDefaultPhoto.png')
    def __str__(self):
        return self.CategoryName


class Product(models.Model):
    ProductName = models.CharField(max_length=100)#1
    ProductPrice = models.FloatField()#2
    ProductDescription = models.TextField()#3
    ProductImage = models.ImageField(upload_to=product_directory_path, default='ProductPhotos/ProductDefaultPhoto.png')#4
    ProductWeight = models.FloatField()#5
    ProductBrand = models.CharField(max_length=120)#6
    ProductFasting=models.BooleanField()#7
    ProductBoycott=models.BooleanField()#8
    NumberOfViews=models.IntegerField(default=0)#9
    ProductPlace=models.CharField(max_length=12,unique=True)#10  #A1-5R-2-1 ()   #https://chatgpt.com/c/673c230a-e058-8011-b61d-b8f5231e014a
    AICode=models.CharField(max_length=12 ,default="code")#11
    ProductTotalRate=models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])#12
    ProductDiscount=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)#13
    ProductQuantity=models.IntegerField()#14
    ProductAvailable=models.BooleanField()#15
    QRNumber=models.CharField(max_length=25,unique=True)#16
    ExpiryDate=models.DateField(default="2030-01-01")#17

    #ForeignKey
    ProductCategory=models.ForeignKey(Category, on_delete=models.SET_DEFAULT,related_name='ProductCategory',default=None)
    ModifiedBy=models.ForeignKey(Worker, on_delete=models.SET_DEFAULT,related_name='ProductModifiedBy',default=None)
    ModifiedDate=models.DateTimeField(auto_now_add=True,blank=True ,null=True) #auto


    def __str__(self):
        return self.ProductName


class Rate(models.Model):
    ProductName=models.ForeignKey(Product, on_delete=models.CASCADE)
    ClientUserName=models.ForeignKey(client, on_delete=models.CASCADE)
    RateValue=models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0,blank=False ,null=False)
    Comment=models.TextField(null=True,blank=True)
    RatingTime=models.DateTimeField(auto_now_add=True,blank=True ,null=True)

    def __str__(self):
        return f"Rate: {self.ProductName} by {self.ClientUserName}"

    class Meta:
        unique_together = (('ProductName', 'ClientUserName'),)
        indexes = [
            Index(fields=['ProductName', 'ClientUserName']),
        ]


class View(models.Model):
    ProductName=models.ForeignKey(Product, on_delete=models.CASCADE)
    ClientUserName=models.ForeignKey(client, on_delete=models.CASCADE)
    LastView=models.DateTimeField(auto_now_add=True ,null=False)
    ViewNumber=models.IntegerField()
    def __str__(self):
        return f"View: {self.ProductName} by {self.ClientUserName}"




