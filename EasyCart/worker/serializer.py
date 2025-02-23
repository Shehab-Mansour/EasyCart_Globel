from rest_framework import serializers
from worker.models import Worker, Job
from django.contrib.auth.hashers import make_password
#Worker

class WorkerSerializer(serializers.ModelSerializer):
    JobName = serializers.CharField(source='WorkerJobTitle.JobName', read_only=True)
    class Meta:
        model = Worker
        fields = ['WorkerUserName','WorkerName','JobName','WorkerSalary','WorkerImage']


class NewWorkerSerializer(serializers.ModelSerializer):
    WorkerPassword = serializers.CharField(write_only=True,required=True)
    WorkerImage = serializers.ImageField(required=False)
    class Meta:
        model = Worker
        fields = '__all__'
    def create(self, validated_data):
        #if pass not set default ==WorkerUserName
        password_value = validated_data.pop('WorkerPassword', None)
        if password_value is None:
            password = Worker.WorkerUserName
        else:
            password = password_value
        validated_data['WorkerPassword'] = make_password(password)
        instance = Worker(**validated_data)
        instance.save()
        return instance
# job
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields ='__all__'

class NewJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
    def create(self, validated_data):
        instance = Job(**validated_data)
        instance.save()
        return instance

