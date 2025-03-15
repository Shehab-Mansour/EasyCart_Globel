# from datetime import timezone
#
# from django.contrib.auth.hashers import make_password
# from django.db import models
# from django.db.models.functions import datetime
#
# # from sympy.logic.algorithms.z3_wrapper import clause_to_assertion
#
# from functions.worker.worker import worker_directory_path ,password
# from django.contrib.auth.hashers import make_password
#
#
# # Create your models here.
# class Job(models.Model):
#     JobName = models.CharField(max_length=100,unique=True)
#     JobDescription = models.CharField(max_length=100)
#     def __str__(self):
#         return self.JobName
#
#
# class Worker(models.Model):
#     WorkerUserName = models.CharField(max_length=100, unique=True , null=False , blank=False )
#     WorkerPassword = models.CharField(max_length=1024,null=True,blank=True) #default as workerUserName
#     WorkerName = models.CharField(max_length=100,null=False)
#     WorkerPhone = models.CharField(max_length=11,null=True)
#     WorkerEmail = models.CharField(max_length=100,null=True)
#     WorkerAddress = models.CharField(max_length=100,null=True)
#     WorkerJobTitle = models.ForeignKey(Job, on_delete=models.CASCADE ,related_name='WorkerJob' ,null=False)
#     WorkerSalary = models.IntegerField(default=0 , null=False)
#     WorkerImage = models.ImageField(upload_to=worker_directory_path, default='workerPhotos/default/workerImage.png')
#     def __str__(self):
#         return self.WorkerUserName
#
#
# import uuid
#
# class WorkerToken(models.Model):
#     id = models.BigAutoField(primary_key=True,default=1)
#     worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
#     token = models.CharField(max_length=512, unique=True, default=uuid.uuid4)  # توليد تلقائي
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField(default=None, null=True)
#
#     def __str__(self):
#         return self.worker
#
# class Admin(models.Model):
#     UserName = models.CharField(max_length=100, unique=True, null=False, blank=False)
#     Password = models.CharField(max_length=1024, null=True, blank=True)  # default as workerUserName
#     Name = models.CharField(max_length=100, null=False)
#     Phone = models.CharField(max_length=11, null=True)
#     Email = models.CharField(max_length=100, null=True)
#     WorkerImage = models.ImageField(upload_to=worker_directory_path, default='workerPhotos/default/workerImage.png')
#
#     def __str__(self):
#         return self.UserName
#
# class AdminToken(models.Model):
#     admin = models.ForeignKey('Admin', on_delete=models.CASCADE)  # تعديل هنا
#     token = models.CharField(max_length=512, unique=True, default=uuid.uuid4)
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField()
#
#     def __str__(self):
#         return self.admin


#
#
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# import uuid
#
# def worker_directory_path(instance, filename):
#     return f'workerPhotos/{instance.WorkerUserName}/{filename}'
#
# class Job(models.Model):
#     JobName = models.CharField(max_length=100, unique=True)
#     JobDescription = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.JobName
#
# class WorkerManager(BaseUserManager):
#     def create_worker(self, WorkerUserName, WorkerPassword=None, **extra_fields):
#         if not WorkerUserName:
#             raise ValueError('Worker must have a username')
#         worker = self.model(WorkerUserName=WorkerUserName, **extra_fields)
#         worker.set_password(WorkerPassword)
#         worker.save(using=self._db)
#         return worker
#
# class Worker(AbstractBaseUser, PermissionsMixin):
#     WorkerUserName = models.CharField(max_length=100, unique=True, null=False, blank=False)
#     WorkerPassword = models.CharField(max_length=1024, null=True, blank=True)
#     WorkerName = models.CharField(max_length=100, null=False)
#     WorkerPhone = models.CharField(max_length=11, null=True)
#     WorkerEmail = models.EmailField(max_length=100, null=True)
#     WorkerAddress = models.CharField(max_length=100, null=True)
#     WorkerJobTitle = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='WorkerJob', null=False)
#     WorkerSalary = models.IntegerField(default=0, null=False)
#     WorkerImage = models.ImageField(upload_to=worker_directory_path, default='workerPhotos/default/workerImage.png')
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     # تعطيل العلاقات العكسية لتجنب التعارض
#     groups = models.ManyToManyField('auth.Group', related_name='+', blank=True)
#     user_permissions = models.ManyToManyField('auth.Permission', related_name='+', blank=True)
#
#     objects = WorkerManager()
#
#     USERNAME_FIELD = 'WorkerUserName'
#
#     def __str__(self):
#         return self.WorkerUserName
#
# class WorkerToken(models.Model):
#     worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
#     token = models.CharField(max_length=512, unique=True, default=uuid.uuid4)
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return f"Token for {self.worker.WorkerUserName}"
#
# class AdminManager(BaseUserManager):
#     def create_admin(self, UserName, Password=None, **extra_fields):
#         if not UserName:
#             raise ValueError('Admin must have a username')
#         admin = self.model(UserName=UserName, **extra_fields)
#         admin.set_password(Password)
#         admin.save(using=self._db)
#         return admin
#
# class Admin(AbstractBaseUser, PermissionsMixin):
#     UserName = models.CharField(max_length=100, unique=True, null=False, blank=False)
#     Password = models.CharField(max_length=1024, null=True, blank=True)
#     Name = models.CharField(max_length=100, null=False)
#     Phone = models.CharField(max_length=11, null=True)
#     Email = models.EmailField(max_length=100, null=True)
#     WorkerImage = models.ImageField(upload_to=worker_directory_path, default='workerPhotos/default/workerImage.png')
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#
#     # تعطيل العلاقات العكسية لتجنب التعارض
#     groups = models.ManyToManyField('auth.Group', related_name='+', blank=True)
#     user_permissions = models.ManyToManyField('auth.Permission', related_name='+', blank=True)
#
#     objects = AdminManager()
#
#     USERNAME_FIELD = 'UserName'
#
#     def __str__(self):
#         return self.UserName
#
# class AdminToken(models.Model):
#     admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
#     token = models.CharField(max_length=512, unique=True, default=uuid.uuid4)
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField()
#
#     def __str__(self):
#         return f"Token for {self.admin.UserName}"

from django.contrib.auth.hashers import make_password
import uuid
from django.db import models

# Create your models here.
class Job(models.Model):
    JobName = models.CharField(max_length=100, unique=True)
    JobDescription = models.CharField(max_length=100)

    def __str__(self):
        return self.JobName

def worker_directory_path(instance, filename):
    return f'workerPhotos/{instance.WorkerUserName}/{filename}'

class Worker(models.Model):
    WorkerUserName = models.CharField(max_length=100, unique=True, null=False, blank=False)
    WorkerPassword = models.CharField(max_length=1024, null=True, blank=True)  # سيتم تشفيره تلقائيًا
    WorkerName = models.CharField(max_length=100, null=False)
    WorkerPhone = models.CharField(max_length=11, null=True)
    WorkerEmail = models.CharField(max_length=100, null=True)
    WorkerAddress = models.CharField(max_length=100, null=True)
    WorkerJobTitle = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='WorkerJob', null=False)
    WorkerSalary = models.IntegerField(default=0, null=False)
    WorkerImage = models.ImageField(upload_to=worker_directory_path, default='workerPhotos/default/workerImage.png')
    IsSupervisor = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.WorkerPassword:  # إذا لم يتم تحديد كلمة المرور
            self.WorkerPassword = make_password(self.WorkerUserName)  # تشفير كلمة المرور كاسم المستخدم
        super().save(*args, **kwargs)

    def __str__(self):
        return self.WorkerUserName

class WorkerToken(models.Model):
    WORKER_ROLES = [
        ('basic_worker', 'Basic Worker'),
        ('supervisor', 'Supervisor'),
        ('worker', 'Worker'),
    ]

    worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    token = models.CharField(max_length=512, unique=True, default=uuid.uuid4)
    role = models.CharField(max_length=20, choices=WORKER_ROLES, default='basic_worker')  # إضافة الدور
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.worker} - {self.role}"

class Admin(models.Model):
    UserName = models.CharField(max_length=100, unique=True, null=False, blank=False)
    Password = models.CharField(max_length=1024, null=True, blank=True)  # سيتم تشفيره لاحقًا
    Name = models.CharField(max_length=100, null=False)
    Phone = models.CharField(max_length=11, null=True)
    Email = models.CharField(max_length=100, null=True)
    WorkerImage = models.ImageField(upload_to=worker_directory_path, default='workerPhotos/default/workerImage.png')
    IsSuperAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.UserName

class AdminToken(models.Model):
    ADMIN_ROLES = [
        ('super_admin', 'Super Admin'),
        ('manager', 'Manager'),
    ]

    admin = models.ForeignKey('Admin', on_delete=models.CASCADE)
    token = models.CharField(max_length=512, unique=True, default=uuid.uuid4)
    role = models.CharField(max_length=20, choices=ADMIN_ROLES, default='manager')  # إضافة الدور
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.admin} - {self.role}"
