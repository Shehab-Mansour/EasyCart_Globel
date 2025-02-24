
import uuid
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ClientToken ,client
from .serializer import *

# Create your views here.


def userhome (request):
    return HttpResponse("User Home page ")
def sinin(request):
    return HttpResponse("sinin page")


def login(request):
    return HttpResponse("login page")




#API
@api_view(['GET'])
def getclient(request):
    try:
        if request.method == "GET":
            clientdata=client.objects.all()
            serializer=ClientSerializer(clientdata.values(), many=True)
            if serializer is not None:
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        #/////////// this was test for POST in this def //////
        # elif request.method == "POST":
        #     serializer=NewClientSerializer(data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data,status=status.HTTP_201_CREATED)
        #     else:
        #         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)


# username = request.GET.get('username')
# password = request.GET.get('password')


@csrf_exempt
@api_view(['POST'])
def login(request):
    try:
        #User Log in
        if request.method == "POST":
            username = request.data.get('username')
            password = request.data.get('password')
            if '@' in username:
                user_obj = get_object_or_404(client, clientEmail=username)
            else:
                user_obj = get_object_or_404(client, clientUserName=username)
            if check_password(password, user_obj.clientPassword):
                token_key = str(uuid.uuid4())
                token = ClientToken.objects.create(user=user_obj, key=token_key) # creat the token session
                clintdata={
                    'Authorization':token.key,
                    'clientUserName':user_obj.clientUserName,
                    'clientFirstName':user_obj.clientFirstName,
                    'clientLastName':user_obj.clientLastName,
                    'clientImage':user_obj.clientImage.url,
                }
                return Response(clintdata, status=status.HTTP_200_OK)
            elif check_password(password, user_obj.clientPassword)==False:
                return Response({'error': 'Wrong password'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET','POST','DELETE',"OPTIONS"])
def register(request):
    # print(request.method)
    try:
        #User register
        if request.method =="POST":
            serializer = NewClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Registration Successfully",
                     "data":serializer.data
                     },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #User LogOut
        elif request.method == "DELETE":
            token_key = request.data.get('Authorization')
            if not token_key:
                return Response({'error': 'Authorization is required.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                token = get_object_or_404(ClientToken, key=token_key)
                token.delete()
                return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def userdetail(request, clientUserName):
    try:

        # print(request.headers.get('Authorization'))
        # Get the authenticated user using the token
        token_key = request.headers.get('Authorization')
        if not token_key:
            return Response({"error": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)
        token = get_object_or_404(ClientToken, key=token_key)
        authenticated_user = token.user
        # Ensure the authenticated user matches the clientUserName
        if authenticated_user.clientUserName != clientUserName:
            return Response(
                {"error": "You are not authorized to access this user's data"},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Fetch the client instance
        user = get_object_or_404(client, clientUserName=clientUserName)
        # Handle GET request to retrieve user data
        if request.method == "GET":
            serializer = UpdateClientSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Handle PUT request to update user data
        elif request.method == "PUT":
            if request.data.get("clientUserName"):
                if request.data.get("clientUserName") != clientUserName :
                    return Response({"error": "User Name can`t be changed"}, status=status.HTTP_403_FORBIDDEN)
            if request.data.get("clientPoints"):
                if request.data.get("clientPoints") != user.clientPoints:
                    return Response({"error":"Points  can`t be changed"}, status=status.HTTP_403_FORBIDDEN)
            if request.data.get("clientMoney"):
                if request.data.get("clientMoney") != user.clientMoney:
                    return Response({"error":"Money  can`t be changed"}, status=status.HTTP_403_FORBIDDEN)
            serializer = UpdateClientSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Client updated successfully", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Handle DELETE request to delete the user
        elif request.method == "DELETE":
            user.delete()
            token.delete()  # Delete the associated token
            return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#
# @csrf_exempt
# @api_view(['GET', 'POST', 'DELETE', 'OPTIONS'])
# def register(request):
#     try:
#         # User Log in
#         if request.method == 'GET' or request.method == 'OPTIONS':
#             username = request.GET.get('username')
#             password = request.GET.get('password')
#             print(username, password)
#
#             if not username or not password:
#                 return Response({'error': 'اسم المستخدم وكلمة المرور مطلوبين.'}, status=status.HTTP_400_BAD_REQUEST)
#
#             user_obj = get_object_or_404(client, clientEmail=username) if '@' in username else get_object_or_404(client, clientUserName=username)
#
#             if check_password(password, user_obj.clientPassword):
#                 token_key = str(uuid.uuid4())
#                 token = ClientToken.objects.create(user=user_obj, key=token_key)
#
#                 clintdata = {
#                     'Authorization': token.key,
#                     'clientUserName': user_obj.clientUserName,
#                     'clientFirstName': user_obj.clientFirstName,
#                     'clientLastName': user_obj.clientLastName,
#                     'clientImage': f'http://127.0.0.1:8000{user_obj.clientImage.url}',
#                 }
#                 return Response(clintdata, status=status.HTTP_200_OK)
#
#             return Response({'error': 'كلمة المرور غير صحيحة.'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         # User register
#         elif request.method == 'POST':
#             serializer = NewClientSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     {
#                         'message': 'Registration Successfully',
#                         'data': serializer.data
#                     },
#                     status=status.HTTP_201_CREATED
#                 )
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         # User LogOut
#         elif request.method == 'DELETE':
#             token_key = request.data.get('Authorization')
#             if not token_key:
#                 return Response({'error': 'التوكن مطلوب.'}, status=status.HTTP_400_BAD_REQUEST)
#
#             token = get_object_or_404(ClientToken, key=token_key)
#             token.delete()
#             return Response({'message': 'تم تسجيل الخروج بنجاح.'}, status=status.HTTP_200_OK)
#
#     except Exception as e:
#         print(e)
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#

@csrf_exempt
@api_view(['GET', 'PUT'])
def adminGetUserDetail(request, clientUserName):
    try:
        # Fetch the client instance
        user = get_object_or_404(client, clientUserName=clientUserName)
        # Handle GET request to retrieve user data
        if request.method == "GET":
            serializer = UpdateClientSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Handle PUT request to update user data
        elif request.method == "PUT":
            if request.data.get("clientUserName"):
                if request.data.get("clientUserName") != clientUserName :
                    return Response({"error": "User Name can`t be changed"}, status=status.HTTP_403_FORBIDDEN)
            serializer = UpdateClientSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Client updated successfully", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)








# def clientimage(request):
#     clientdata=get_object_or_404(client)
#     return HttpResponse(f'<img src="media/{clientdata.clientImage}" alt="Client Image" style=" height: 300px; width: auto;">')

