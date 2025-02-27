from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from User.models import ClientToken ,client
from functions.product.rate import update_product_rating
from .models import Product,Category,Rate,View
from .serializer import *

import threading
# Create your views here.


def products(request):
    return HttpResponse("product list page")

############################# Product #############################

#get all Products
@csrf_exempt
@api_view(['GET'])
def getallproducts(request):
    try:
        products = Product.objects.all()
        serializer=GetallProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

# get specific product by QRNumber in header
# @csrf_exempt
# @api_view(['GET','PUT','DELETE'])
# def productdetails(request, QRNumber):
#     try:
#         product = Product.objects.get(QRNumber=QRNumber)
#     except Product.DoesNotExist:
#         return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
#     try:
#         if request.method == 'GET':
#             serializer=ProductSerializer(product)
#             if serializer:
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         if request.method == 'PUT':
#             serializer = ProductSerializer(product, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         if request.method == 'DELETE':
#             product.delete()
#             return Response({'message':'The Product Deleted Success'},status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def productdetails(request, QRNumber):
    try:
        product = Product.objects.get(QRNumber=QRNumber)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        if request.method == 'GET':
            # print(request.headers.get('Authorization'))
            if request.headers.get('Authorization'):
                token_key = request.headers.get('Authorization')
                # print(token_key)
                try:
                    token = ClientToken.objects.get(key=token_key)
                    client_user = token.user
                    # print(client_user)
                    threading.Thread(target=update_views, args=(product, client_user)).start()
                except ClientToken.DoesNotExist:
                    print("DoesNotExist")
                    pass
            serializer = ProductSerializer(product)
            if serializer:
                # print("done+1")
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'PUT':
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            product.delete()
            return Response({'message': 'The Product Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

# add New Product
@csrf_exempt
@api_view(['GET','POST'])
def newproduct(request):
    if request.method == 'GET':
        return Response({'message':'Add New Product '})
    try:
        if request.method == 'POST':
            serializer = NewProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                product=get_object_or_404(Product,QRNumber=serializer.data['QRNumber'])
                serializer2=ProductSerializer(product)
                return Response(serializer2.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
############################# END Product #############################




############################# Category #############################

# get all categories , add new category
@csrf_exempt
@api_view(['GET','POST'])
def categories(request):
    try:
        if request.method == 'GET':
            categories = Category.objects.all()
            serializer=CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'POST':
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
# get category with category name , Update and Delete category
@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def categorydetails(request, CategoryName):
    try:
        category = Category.objects.get(CategoryName=CategoryName)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        if request.method == 'GET':
            serializer = CategorySerializer(category)
            if serializer:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'PUT':
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            category.delete()
            return Response({'message':'Deleted done'},status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def getProductsInCategory(request, CategoryName):
    try:
        if request.method == 'GET':
            category = get_object_or_404(Category, CategoryName=CategoryName)
            products = Product.objects.filter(ProductCategory=category)
            if products:
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Category is Empty"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
############################# END Category #############################





#############################   Rate   #############################
@csrf_exempt
@api_view(['GET','POST','PUT','DELETE'])
def rate(request):
    try:
        if request.method == 'GET':
            rates = Rate.objects.all()
            serializer = RateSerializer(rates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'POST' or  request.method == 'PUT' or request.method == 'DELETE':
            # token_key = request.data.get('Authorization')
            # qr_number = request.data.get('QRNumber')
            # if not token_key:
            #     return Response({"error": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)
            # if not qr_number:
            #     return Response({"error": "QRNumber is required"}, status=status.HTTP_400_BAD_REQUEST)
            # token = get_object_or_404(ClientToken, key=token_key)
            # client_user = token.user
            # product = get_object_or_404(Product, QRNumber=qr_number)
            # request_data = {
            #     "ProductName": product.id,
            #     "ClientUserName": client_user.id,
            #     "RateValue": request.data.get('RateValue'),
            #     "Comment": request.data.get('Comment', ""),
            # }
            # existing_rate = Rate.objects.filter(ProductName=product, ClientUserName=client_user).first()
            # if existing_rate:
            #     serializer = RateSerializer(existing_rate, data=request_data)
            #     action = "updated"
            # else:
            #     serializer = NewRateSerializer(data=request_data)
            #     action = "created"
            #
            # if serializer.is_valid():
            #     rate_instance = serializer.save()
            #     update_product_rating(product)
            #     return Response(
            #         {
            #             "message": f"Rate {action} successfully.",
            #             "data": serializer.data,
            #         },
            #         status=status.HTTP_201_CREATED if action == "created" else status.HTTP_200_OK,
            #     )
            # else:
            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                token_key = request.data.get('Authorization')
                qr_number = request.data.get('QRNumber')
                if not token_key:
                    return Response({"error": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)
                if not qr_number:
                    return Response({"error": "QRNumber is required"}, status=status.HTTP_400_BAD_REQUEST)
                token = get_object_or_404(ClientToken, key=token_key)
                client_user = token.user
                product = get_object_or_404(Product, QRNumber=qr_number)
                if request.method == 'POST':
                    request_data = {
                        "ProductName": product.id,
                        "ClientUserName": client_user.id,
                        "RateValue": request.data.get('RateValue'),
                        "Comment": request.data.get('Comment', ""),
                    }
                    # print(request_data)
                    existing_rate = Rate.objects.filter(ProductName=product, ClientUserName=client_user).first()
                    if existing_rate:
                        return Response(
                            {"error": "Rate already exists for this product."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    serializer = NewRateSerializer(data=request_data)
                    if serializer.is_valid():
                        serializer.save()
                        update_product_rating(product)
                        return Response(
                            {
                                "message": "Rate created successfully.",
                                "data": serializer.data,
                            },
                            status=status.HTTP_201_CREATED,
                        )
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                elif request.method == 'PUT':
                    existing_rate = get_object_or_404(Rate, ProductName=product, ClientUserName=client_user)
                    request_data = {
                        "ProductName": product.id,
                        "ClientUserName": client_user.id,
                        "RateValue": request.data.get('RateValue'),
                        "Comment": request.data.get('Comment', existing_rate.Comment),
                    }
                    serializer = RateSerializer(existing_rate, data=request_data)
                    if serializer.is_valid():
                        serializer.save()
                        update_product_rating(product)
                        return Response(
                            {
                                "message": "Rate updated successfully.",
                                "data": serializer.data,
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                elif request.method == 'DELETE':  # Delete
                    rate_instance = Rate.objects.filter(ProductName=product, ClientUserName=client_user).first()
                    if not rate_instance:
                        return Response({"error": "Rate not found for this product."}, status=status.HTTP_404_NOT_FOUND)
                    rate_instance.delete()
                    update_product_rating(product)
                    return Response({"message": "Rate deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def getAllProductRates(request,QRNumber):
    try:
        if request.method == 'GET':
            product = get_object_or_404(Product, QRNumber=QRNumber)
            rates = Rate.objects.filter(ProductName=product)
            if not rates:
                return Response({"message": "No Rates yet"}, status=status.HTTP_404_NOT_FOUND)
            serializer = RateSerializer(rates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)



### get AllClient Rates with clientUserName ##
@csrf_exempt
@api_view(['GET'])
def getAllClientRates(request,clientUserName):
    try:
        if request.method == 'GET':
            token_key = request.headers.get('Authorization')
            if not token_key:
                return Response({"error": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)
            token = get_object_or_404(ClientToken, key=token_key)
            client_user = token.user
            if str(client_user) == str(clientUserName):
                rates = Rate.objects.filter(ClientUserName=client_user)
                serializer = RateSerializer(rates, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Client is Not Found or not the same Authorization"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

#############################  END Rate   #############################


#############################    Views    #############################
from django.db.models import F
from datetime import timedelta
from django.utils.timezone import now
from django.db import transaction

# This function is used to save the number of times a customer visits a specific product, and record it in the customer's viewing database.
#
# Also, calculate the total number of visits to the product and put it in the database.
# But on condition that a minute passes for each customer since the last visit to the product in order for the visit to be counted.

def update_views(product, client_user):
    # print("in update_views")
    try:
        last_view = View.objects.filter(
            ProductName=product,
            ClientUserName=client_user
        ).order_by('-LastView').first()
        if last_view:
            time_diff = now() - last_view.LastView
            if time_diff < timedelta(minutes=1):
                return
            last_view.ViewNumber = F('ViewNumber') + 1
            product.NumberOfViews = F('NumberOfViews') + 1
            product.save(update_fields=['NumberOfViews'])
            last_view.LastView = now()
            last_view.save(update_fields=['ViewNumber', 'LastView'])
            # print("new view")
        else:
            with transaction.atomic():
                product.NumberOfViews = F('NumberOfViews') + 1
                product.save(update_fields=['NumberOfViews'])
            View.objects.create(
                ProductName=product,
                ClientUserName=client_user,
                LastView=now(),
                ViewNumber=1
            )
            # print("upda view")
    except Exception as e:
        print(f"Error updating views: {e}")



@api_view(['GET'])
def  getAllProudactThatViewByClient(request):
    try:
        token_key = request.headers.get('Authorization')
        if not token_key:
            return Response({"error": "Token is required"}, status=status.HTTP_401_UNAUTHORIZED)
        token = get_object_or_404(ClientToken, key=token_key)
        client_user = token.user
        user_views = View.objects.filter(ClientUserName=client_user)
        if not user_views.exists():
            return Response({"message": "No views found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ViewSerializer(user_views, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getAllProudactView(request,QRNumber):
    try:
        product = get_object_or_404(Product, QRNumber=QRNumber)
        product_views = View.objects.filter(ProductName=product)
        if not product_views.exists():
            return Response({"message": "No views found for this product."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ViewSerializer(product_views, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
