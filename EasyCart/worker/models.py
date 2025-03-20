from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from datetime import timedelta
from django.utils.timezone import now


# نموذج الوظائف مع صلاحيات مخصصة
class Job(models.Model):
    JobName = models.CharField(max_length=100, unique=True)
    JobDescription = models.CharField(max_length=255)

    def __str__(self):
        return self.JobName


# جدول مخصص للصلاحيات لكل وظيفة
class WorkerPermission(models.Model):
    JobName = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='permissions')
    can_add_products = models.BooleanField(default=False)
    can_edit_products = models.BooleanField(default=False)
    can_delete_products = models.BooleanField(default=False)

    def __str__(self):
        return f"Permissions for {self.JobName.JobName}"


def worker_directory_path(instance, filename):
    return f'workerPhotos/{instance.WorkerUserName}/{filename}'


# نموذج الموظف
class Worker(models.Model):
    WorkerUserName = models.CharField(max_length=100, unique=True)
    WorkerPassword = models.CharField(max_length=1024, blank=True)
    WorkerName = models.CharField(max_length=100)
    WorkerPhone = models.CharField(max_length=11, null=True, blank=True)
    WorkerEmail = models.CharField(max_length=100, null=True, blank=True)
    WorkerAddress = models.CharField(max_length=255, null=True, blank=True)
    WorkerJobTitle = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='workers')
    WorkerSalary = models.IntegerField(default=0)
    WorkerImage = models.ImageField(upload_to=worker_directory_path, default='workerPhotos/default/workerImage.png')
    IsSupervisor = models.BooleanField(default=False)

    @property
    def is_authenticated(self):
        return True

    def save(self, *args, **kwargs):
        if not self.WorkerPassword:
            self.WorkerPassword = make_password(self.WorkerUserName)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.WorkerUserName


# نموذج التوكن الخاص بالموظف
class WorkerToken(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    token = models.CharField(max_length=512, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=now() + timedelta(days=1))

    def __str__(self):
        return f"{self.worker.WorkerUserName} - Token"


# نموذج المشرف (Admin)
class Admin(models.Model):
    UserName = models.CharField(max_length=100, unique=True)
    Password = models.CharField(max_length=1024, blank=True)
    Name = models.CharField(max_length=100)
    Phone = models.CharField(max_length=11, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    AdminImage = models.ImageField(upload_to='adminPhotos/', default='adminPhotos/default/adminImage.png')
    IsSuperAdmin = models.BooleanField(default=False)

    @property
    def is_authenticated(self):
        return True
    def __str__(self):
        return self.UserName


# نموذج التوكن الخاص بالمشرف (Admin)
class AdminToken(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    token = models.CharField(max_length=512, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=now() + timedelta(days=1))

    def __str__(self):
        return f"{self.admin.UserName} - Token"

