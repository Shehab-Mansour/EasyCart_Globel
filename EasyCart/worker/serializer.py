from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import Worker, Admin, Job, WorkerPermission
from .authentication import CustomRefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
#
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#
#     def validate(self, data):
#         username = data.get("username")
#         password = data.get("password")
#
#         # تحقق مما إذا كان المستخدم Admin أو Worker
#         user = Worker.objects.filter(WorkerUserName=username).first()
#         role = "worker"
#         if not user:
#             user = Admin.objects.filter(UserName=username).first()
#             role = "admin"
#
#         if user and check_password(password, user.WorkerPassword if role == "worker" else user.Password):
#             refresh = RefreshToken.for_user(user)
#             return {
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "role": role
#             }
#         raise serializers.ValidationError("Invalid username or password")

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = Worker.objects.filter(WorkerUserName=username).first()
        role = "worker"

        if not user:
            user = Admin.objects.filter(UserName=username).first()
            role = "admin"
        if user and check_password(password, getattr(user, "WorkerPassword" if role == "worker" else "Password")):
            refresh = CustomRefreshToken.for_custom_user(user, role)
            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": role
            }

        raise serializers.ValidationError({"error": "Invalid username or password"})

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Worker
#
# class WorkerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Worker
#         fields = [
#             'id',
#             'WorkerUserName',
#             'WorkerPassword',
#             'WorkerName',
#             'WorkerPhone',
#             'WorkerEmail',
#             'WorkerAddress',
#             'WorkerJobTitle',
#             'WorkerSalary',
#             'WorkerImage',
#             'IsSupervisor'
#         ]
#         extra_kwargs = {
#             'WorkerPassword': {'write_only': True}  # عدم إرجاع كلمة المرور في الاستجابات
#         }
#
#     def create(self, validated_data):
#         """
#         عند إنشاء موظف جديد، يتم تشفير كلمة المرور تلقائيًا.
#         """
#         validated_data['WorkerPassword'] = make_password(validated_data['WorkerUserName'])
#         return super().create(validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         منع تحديث كلمة المرور مباشرةً (يجب أن يتم ذلك عبر API منفصل لتغيير كلمة المرور).
#         """
#         validated_data.pop('WorkerPassword', None)
#         return super().update(instance, validated_data)
class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = [
            # 'id',
            'WorkerUserName',
            'WorkerPassword',
            'WorkerName',
            'WorkerPhone',
            'WorkerEmail',
            'WorkerAddress',
            'WorkerJobTitle',
            'WorkerSalary',
            'WorkerImage',
            'IsSupervisor'
        ]
        extra_kwargs = {
            # 'id':{'read_only': True},
            'WorkerUserName': {'required': True},
            'WorkerPassword': {'write_only': True},
            'WorkerName': {'required': False},
            'WorkerPhone': {'required': True},
            'WorkerEmail': {'required': False},
            'WorkerAddress': {'required': False},
            'WorkerSalary': {'required': True},
            'WorkerJobTitle': {'required': True},
            'IsSupervisor': {'required': True}
        }


    def create(self, validated_data):
        validated_data['WorkerPassword'] = make_password(validated_data['WorkerUserName'])
        return super().create(validated_data)


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['UserName', 'Name', 'Phone', 'Email',"IsSuperAdmin" ,'AdminImage']

    def create(self, validated_data):
        validated_data['Password'] = make_password(validated_data['UserName'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'JobName','JobDescription'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'JobName': {'required': False}
                }

class WorkerPermissionSerializer(serializers.ModelSerializer):
    JobName = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())  # ربط الصلاحيات بالوظيفة
    class Meta:
        model = WorkerPermission
        fields = ['JobName', 'can_add_products', 'can_edit_products', 'can_delete_products']