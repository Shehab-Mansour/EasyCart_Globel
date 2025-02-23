from django.contrib.auth.hashers import make_password
from django.db import models

from functions.worker.worker import worker_directory_path ,password
from django.contrib.auth.hashers import make_password


# Create your models here.
class Job(models.Model):
    JobName = models.CharField(max_length=100,unique=True)
    JobDescription = models.CharField(max_length=100)
    def __str__(self):
        return self.JobName


class Worker(models.Model):
    WorkerUserName = models.CharField(max_length=100, unique=True , null=False , blank=False )
    WorkerPassword = models.CharField(max_length=1024,null=True,blank=True) #default as workerUserName
    WorkerName = models.CharField(max_length=100,null=False)
    WorkerPhone = models.CharField(max_length=11,null=True)
    WorkerEmail = models.CharField(max_length=100,null=True)
    WorkerAddress = models.CharField(max_length=100,null=True)
    WorkerJobTitle = models.ForeignKey(Job, on_delete=models.CASCADE ,related_name='WorkerJob' ,null=False)
    WorkerSalary = models.IntegerField(default=0 , null=False)
    WorkerImage = models.ImageField(upload_to=worker_directory_path, default='workerPhotos/default/workerImage.png')
    def __str__(self):
        return self.WorkerUserName


class WorkerToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    worker = models.ForeignKey(Worker, related_name='worker_auth_tokens', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


