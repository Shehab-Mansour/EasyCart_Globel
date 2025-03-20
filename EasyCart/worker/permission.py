from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'IsSuperAdmin') and request.user.IsSuperAdmin
class IsWorker(BasePermission):
    def has_permission(self, request, view):
        print(request.user.is_authenticated)
        print( hasattr(request.user, 'WorkerJobTitle'))
        return request.user.is_authenticated and hasattr(request.user, 'WorkerJobTitle')
class IsAdminOrWorker(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and hasattr(request.user, 'IsSuperAdmin') and request.user.IsSuperAdmin) or (request.user.is_authenticated and hasattr(request.user, 'WorkerJobTitle'))
