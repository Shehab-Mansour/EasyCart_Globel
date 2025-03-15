from rest_framework import serializers
from worker.models import Worker, Job ,Admin
from django.contrib.auth.hashers import make_password
# #Worker
#
# class WorkerSerializer(serializers.ModelSerializer):
#     JobName = serializers.CharField(source='WorkerJobTitle.JobName', read_only=True)
#     class Meta:
#         model = Worker
#         fields = ['WorkerUserName','WorkerName','JobName','WorkerSalary','WorkerImage']
#
#
# class NewWorkerSerializer(serializers.ModelSerializer):
#     WorkerPassword = serializers.CharField(write_only=True,required=True)
#     WorkerImage = serializers.ImageField(required=False)
#     class Meta:
#         model = Worker
#         fields = '__all__'
#     def create(self, validated_data):
#         #if pass not set default ==WorkerUserName
#         password_value = validated_data.pop('WorkerPassword', None)
#         if password_value is None:
#             password = Worker.WorkerUserName
#         else:
#             password = password_value
#         validated_data['WorkerPassword'] = make_password(password)
#         instance = Worker(**validated_data)
#         instance.save()
#         return instance
# # job
# class JobSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Job
#         fields =['JobName','JobDescription']
#         extra_kwargs = {
#             'pk': {'read_only':True},
#         }

class NewJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['JobName', 'JobDescription']
        extra_kwargs = {
            'pk': {'read_only': True},
        }
    def create(self, validated_data):
        instance = Job(**validated_data)
        instance.save()
        return instance


#
#
# # class WorkerSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Worker
# #         fields = '__all__'
#
# class AdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Admin
#         fields = '__all__'
#
# class WorkerLoginSerializer(serializers.Serializer):
#     WorkerUserName = serializers.CharField()
#     WorkerPassword = serializers.CharField(write_only=True)
#
#
# class AdminLoginSerializer(serializers.Serializer):
#     UserName = serializers.CharField()
#     Password = serializers.CharField(write_only=True)

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'JobName', 'JobDescription']

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['WorkerUserName', 'WorkerName', 'WorkerPhone', 'WorkerEmail', 'WorkerAddress', 'WorkerJobTitle', 'WorkerSalary', 'WorkerImage']

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
        fields = ['UserName', 'Name', 'Phone', 'Email',"IsSuperAdmin"]

    def create(self, validated_data):
        validated_data['Password'] = make_password(validated_data['UserName'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=1024, write_only=True)
