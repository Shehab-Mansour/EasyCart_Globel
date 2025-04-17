from django.contrib import admin
from .models import Job, Worker, WorkerPermission, Admin


# Register your models here.


class JobDisplay(admin.ModelAdmin):
  list_display = ("JobName", "JobDescription",)

admin.site.register(Worker)
admin.site.register(Job, JobDisplay)
admin.site.register(WorkerPermission)
admin.site.register(Admin)
