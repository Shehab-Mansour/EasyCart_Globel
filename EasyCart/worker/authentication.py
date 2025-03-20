from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken, AccessToken
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .models import Admin, Worker  # استيراد الموديلات الخاصة بك
from User.models import client
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

from rest_framework_simplejwt.tokens import RefreshToken

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_custom_user(cls, user, user_type):
        token = cls()
        token["user_id"] = user.id
        token["user_type"] = user_type  # إضافة نوع المستخدم
        return token

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # لا يوجد توكين، يتم متابعة باقي المصادقات

        token = auth_header.split(" ")[1]  # استخراج التوكين
        try:
            validated_token = AccessToken(token)
            user_id = validated_token["user_id"]
            user_type = validated_token["user_type"]
            # print(user_type, user_id)

            if user_type == "admin":
                user = Admin.objects.filter(id=user_id).first()
            elif user_type == "worker":
                user = Worker.objects.filter(id=user_id).first()
            elif user_type == "user":
                user = client.objects.filter(id=user_id).first()
            else:
                raise AuthenticationFailed(("Invalid user type."))

            if user is None:
                raise AuthenticationFailed(("User not found."))

            # ✅ إضافة `is_authenticated` لتمكين المصادقة
            # user.is_authenticated = True
            # print(user.is_authenticated)
            return user, validated_token

        except Exception:
            raise AuthenticationFailed(("Invalid or expired token."))


def getUserType(request):
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1]  # استخراج التوكين
    try:
        validated_token = AccessToken(token)
        user_type = validated_token["user_type"]
    except:
        raise AuthenticationFailed(("Invalid user type."))
    return user_type
