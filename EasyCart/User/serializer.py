from  rest_framework import serializers
from django.contrib.auth.hashers import make_password
import datetime

from rest_framework.views import APIView

from .models import client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = client
        fields = ['clientUserName','clientFirstName','clientLastName','clientEmail','clientImage']

class NewClientSerializer(serializers.ModelSerializer):
    clientPassword = serializers.CharField(write_only=True, required=True)  # To ensure password isn't returned in the response
    clientBirthdate = serializers.DateField(default=datetime.date.today,write_only=True)    # Ensure date format is handled correctly
    clientImage = serializers.ImageField(write_only=True,required=False,default='clientPhotos/default/clientImage.png')
    class Meta:
        model = client
        fields = ['clientUserName', 'clientFirstName', 'clientLastName', 'clientEmail','clientBirthdate','clientPassword','clientImage']
    def create(self, validated_data):
        password = validated_data.pop('clientPassword')
        validated_data['clientPassword'] = make_password(password)
        instance = client(**validated_data)
        instance.save()
        return instance

class UpdateClientSerializer(serializers.ModelSerializer):
    clientPassword = serializers.CharField(write_only=True,required=True)  # To ensure password isn't returned in the response
    clientBirthdate = serializers.DateField(default=datetime.date.today)  # Ensure date format is handled correctly
    clientImage = serializers.ImageField(required=False, default='clientPhotos/default/clientImage.png')
    class Meta:
        model = client
        # read_only_fields = ['clientPassword']
        fields = ['clientPassword','clientUserName', 'clientFirstName', 'clientLastName', 'clientEmail','clientImage','clientPhone','clientGender','clientMoney','clientPoints','clientBirthdate']
    def update(self, instance, validated_data):
        # Handle password separately
        password = validated_data.pop('clientPassword', None)
        if password:
            instance.clientPassword = make_password(password)
        # Update only the fields that are sent in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

