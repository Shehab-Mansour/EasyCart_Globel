from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .authentication import CustomRefreshToken
from .serializer import *
from worker.permission import IsAdminUser
from .permission import IsClientUser


def sinin(request):
    return HttpResponse("sinin page")


#API
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getclient(request):
    try:
        if request.method == "GET":
            clientdata=client.objects.all()
            serializer=ClientSerializer(clientdata.values(), many=True)
            if serializer is not None:
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

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
                role='user'
                refresh = CustomRefreshToken.for_custom_user(user_obj, role)
                clintdata = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role
                }
                return Response(clintdata, status=status.HTTP_200_OK)
            elif check_password(password, user_obj.clientPassword)==False:
                return Response({'error': 'Wrong password'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def register(request):
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
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsClientUser])
def logout(request):
    try:
        if request.method == "DELETE":
            try:
                refresh_token = request.data.get("refresh")
                if not refresh_token:
                    return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
            except TokenError:
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsClientUser])
def userdetail(request):
    try:
        user = get_object_or_404(client, id=request.user.id)
        clientUserName=user.clientUserName
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
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            user.delete()
            return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT'])
@permission_classes([IsAdminUser])
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

