import uuid

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json

SECRET_KEY = settings.SECRET_KEY  # استخدام المفتاح من إعدادات Django


def generate_custom_jwt(user, access_time, refresh_time, EasyCart):
    """توليد Access و Refresh Token بزمن مخصص مع تضمين دور المستخدم في الـ Payload"""

    # SECRET_KEY = settings.SECRET_KEY  # استخدام المفتاح من إعدادات Django
    user_role = "client"  # تحديد دور المستخدم
    jti_access = str(uuid.uuid4())  # إنشاء معرف فريد لكل توكن
    jti_refresh = str(uuid.uuid4())

    current_time = datetime.utcnow()

    # إنشاء Payload للتوكن الأساسي (Access Token)
    access_payload = {
        "token_type": "access",
        "jti": jti_access,
        "sub": str(user.id),  # استخدم 'sub' لضمان توافق التوكين مع DRF
        "user_id": user.id,
        "user_type": user_role,
        "EasyCart": EasyCart,
        "exp": current_time + timedelta(minutes=access_time),
        "iat": current_time,
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")

    # إنشاء Payload لتوكن التحديث (Refresh Token)
    refresh_payload = {
        "token_type": "refresh",
        "jti": jti_refresh,
        "sub": str(user.id),  # تأكد من توافقه مع `JWTAuthentication`
        "user_id": user.id,
        "user_type": user_role,
        "exp": current_time + timedelta(minutes=refresh_time),
        "iat": current_time,
        "EasyCart": EasyCart,
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")

    return {
        "access": access_token,
        "refresh": refresh_token,
        "role": user_role,
    }
#
# def refresh_token_view(request, access_time=15):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             refresh_token = data.get("refresh")
#
#             if not refresh_token:
#                 return JsonResponse({"error": "Refresh token is required"}, status=400)
#
#             # فك التشفير للتحقق من صحة التوكن
#             decoded_payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
#
#             user_id = decoded_payload.get("user_id")
#             user_role = decoded_payload.get("user_type")  # متسجل كده في generate_custom_jwt
#             EasyCart = decoded_payload.get("EasyCart")
#
#             # إنشاء Access Token جديد فقط بنفس البيلود
#             jti_access = str(uuid.uuid4())
#             current_time = datetime.utcnow()
#
#             new_access_payload = {
#                 "token_type": "access",
#                 "jti": jti_access,
#                 "sub": str(user_id),
#                 "user_id": user_id,
#                 "user_type": user_role,
#                 "EasyCart": EasyCart,
#                 "exp": current_time + timedelta(minutes=access_time),
#                 "iat": current_time,
#             }
#
#             new_access_token = jwt.encode(new_access_payload, SECRET_KEY, algorithm="HS256")
#
#             return JsonResponse({"access": new_access_token})
#
#         except jwt.ExpiredSignatureError:
#             return JsonResponse({"error": "Refresh token has expired"}, status=401)
#         except jwt.InvalidTokenError:
#             return JsonResponse({"error": "Invalid refresh token"}, status=401)
#
#     return JsonResponse({"error": "Invalid request method"}, status=405)
#

from cart.models import EasyCart


def getEasyCart(request):
    EasyCartAuthorization = request.headers.get("Authorization")

    if not EasyCartAuthorization:
        return Response({"error": "Need EasyCart ID in Authorization"}, status=status.HTTP_401_UNAUTHORIZED)

    EasyCartdata = EasyCart.objects.filter(cartId=EasyCartAuthorization).first()

    if not EasyCartdata:
        return Response({"error": "Cart Not found"}, status=status.HTTP_404_NOT_FOUND)

    if EasyCartdata.lastUsedAt and (now() - EasyCartdata.lastUsedAt) > timedelta(hours=2):
        EasyCartdata.cartStatus = "ready"
        EasyCartdata.VirtualCart=None
        EasyCartdata.lastUsedBy=None
        EasyCartdata.save(update_fields=["cartStatus","VirtualCart","lastUsedBy"])  # تحديث الحقل فقط

    if EasyCartdata.cartStatus == "ready":
        EasyCartd = EasyCart.objects.filter(cartId=EasyCartAuthorization).first()
        return EasyCartd
    else:
        error = f"Cart is {EasyCartdata.cartStatus}"
        return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)