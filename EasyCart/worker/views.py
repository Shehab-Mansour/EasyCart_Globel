import uuid
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WorkerToken
from .serializer import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


# Create your views here.


@csrf_exempt
@api_view(['GET','POST','PUT','DELETE'])
def worker(request):
    try:
        #worker log in
        if request.method == "GET":
            workerusername = request.data.get('workerusername')
            workerpassword = request.data.get('workerpassword')
            if '@' in workerusername:
                user_obj = get_object_or_404(Worker, WorkerEmail=workerusername)
            else:
                user_obj = get_object_or_404(Worker, WorkerUserName=workerusername)
            # password=make_password(workerpassword)
            # print(password)
            # print(user_obj.WorkerPassword)
            if check_password(workerpassword, user_obj.WorkerPassword):
                token_key = str(uuid.uuid4())
                token =WorkerToken.objects.create(key=token_key,worker=user_obj)
                jobname = get_object_or_404(Job, id=user_obj.WorkerJobTitle_id) #get job name by id
                workerdata={
                    'Authorization ':token.key,
                    'WorkerUserName':user_obj.WorkerUserName,
                    'WorkerName':user_obj.WorkerName,
                    'WorkerJobTitle':jobname.JobName,
                    'WorkerImage':user_obj.WorkerImage.url,
                }
                return Response(workerdata, status=status.HTTP_200_OK)
            else:
                return Response({'error':' wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        # New worker from admin only
        if request.method == 'POST':
            data=request.data.copy() # take copy from sended data to add new pass and job id
            data['WorkerPassword'] = data['WorkerUserName'] #set pass as  WorkerUserName
            #get job id by job name to send to DB
            jobname=data['WorkerJobTitle']
            data['WorkerJobTitle']=Job.objects.get(JobName=jobname).id
            #send to serializer
            serializer = NewWorkerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #edit Worker note: Not working yet
        if request.method == 'PUT':
            serializer = NewWorkerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #worker log out
        if request.method == 'DELETE':
            token_key = request.data.get('Authorization')
            if not token_key:
                return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                token = get_object_or_404(WorkerToken, key=token_key)
                token.delete()
                return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def getallWorkers(request):
    workers = Worker.objects.select_related('WorkerJobTitle').all()
    serializer = WorkerSerializer(workers, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET','POST'])
def job(request):
    try:
        if request.method == "GET":
            serializer = JobSerializer(Job.objects.all(), many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        elif request.method == "POST":
            serializer = NewJobSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Method not allowed'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
