import datetime
from django.db import models
from functions.user.client import client_directory_path
# Create your models here.


#
class client(models.Model):
    clientUserName = models.CharField(max_length=50,null=False , blank=False , unique=True)
    clientPassword = models.CharField(max_length=500,null=False , blank=False)
    clientFirstName = models.CharField(max_length=50 ,null=False ,default='YourFirstName')
    clientLastName = models.CharField(max_length=50 ,null=False ,default='YourLastName')
    clientEmail = models.CharField(max_length=100,null=False ,default='<EMAIL>')
    clientPhone = models.CharField(max_length=11,null=False ,default='01234567890')
    clientGender = models.CharField(max_length=10,null=False ,default='male', choices=[('male','male'),('female','female'),('other','other')])
    clientBirthdate = models.DateField(null=False , blank=False ,default=datetime.date.today)
    clientMoney = models.IntegerField(null=False , blank=False, default=0)
    clientPoints = models.IntegerField(null=False , blank=False ,default=0)
    clientImage = models.ImageField(upload_to=client_directory_path, default='clientPhotos/default/clientImage.png')
    IsClient = models.BooleanField(default=True)
    def __str__(self):
        return self.clientUserName

    @property
    def is_authenticated(self):
        return True


class ClientToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey('client', related_name='auth_tokens', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
