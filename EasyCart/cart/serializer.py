from  rest_framework import serializers
from django.contrib.auth.hashers import make_password
import datetime
from rest_framework.views import APIView
from worker.models import Worker
from django.db.models import Avg


