from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import AccessToken

from worker.models import WorkerToken

# class WorkerTokenAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         auth_header = request.headers.get('Authorization')
#
#         if not auth_header or not auth_header.startswith('Bearer '):
#             return None  # ⬅️ يسمح بمرور الطلب بدون مصادقة (للطلبات العامة)
#
#         token = auth_header.split(' ')[1]
#
#         try:
#             worker_token = WorkerToken.objects.get(token=token)
#
#             if worker_token.expires_at < now():
#                 raise AuthenticationFailed("Token expired")
#
#             return (worker_token.worker, worker_token)  # ✅ إرجاع المستخدم والتوكن
#         except WorkerToken.DoesNotExist:
#             raise AuthenticationFailed("Invalid token")

class WorkerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # ⬅️ السماح باستخدام مصادقات أخرى مثل JWT

        token = auth_header.split(' ')[1]
        try:
            worker_token = WorkerToken.objects.get(token=token)



            if worker_token.expires_at < now():
                raise AuthenticationFailed("Token expired")
            return (worker_token.worker, worker_token)  # ✅ إرجاع المستخدم والتوكن
        except WorkerToken.DoesNotExist:
            raise AuthenticationFailed("Invalid token")
