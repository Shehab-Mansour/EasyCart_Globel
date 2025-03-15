from django.utils import timezone
from django.utils.timezone import now
from rest_framework.permissions import BasePermission
from .models import AdminToken ,WorkerToken

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        try:
            # استخراج التوكن من الهيدر
            token = request.auth

            # البحث في قاعدة البيانات
            admin_token = AdminToken.objects.get(token=token, admin=request.user)

            # التحقق من صلاحية التوكن
            if admin_token.expires_at < timezone.now():
                return False

            # التحقق من الدور
            return admin_token.role == 'Admin'
        except AdminToken.DoesNotExist:
            return False
#
# class IsWorkerRole(BasePermission):
#     allowed_roles = []
#
#     def has_permission(self, request, view):
#         try:
#             # استخراج التوكن من الهيدر
#             token = request.auth
#
#             # البحث عن الجلسة في WorkerToken
#             worker_token = WorkerToken.objects.get(token=token, worker=request.user)
#
#             # التحقق من صلاحية الجلسة
#             if worker_token.expires_at < now():
#                 return False
#
#             # تحقق من الدور إذا كان ضمن الأدوار المسموح بها
#             return worker_token.role in self.allowed_roles
#
#         except WorkerToken.DoesNotExist:
#             return False
#
#
# class IsSupervisor(IsWorkerRole):
#     allowed_roles = ['supervisor']
#
#
# class IsBasicWorker(IsWorkerRole):
#     allowed_roles = ['basic_worker', 'supervisor']
