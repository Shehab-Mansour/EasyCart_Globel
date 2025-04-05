from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, BasePermission

from User.models import ClientToken ,client
from User.permission import IsClientUser
from functions.product.rate import update_product_rating
from worker.authentication import getUserType
from .serializer import *
import threading
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import CategorySerializer
from worker.permission import IsAdminUser, IsWorker, IsAdminOrWorker
from User.models import client

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


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def productdetails(request, QRNumber):
    try:
        product = Product.objects.get(QRNumber=QRNumber)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        if request.method == 'GET':
            if request.headers.get('Authorization'):
                token_key = request.headers.get('Authorization')
                # print(token_key)
                try:
                    user_role=getUserType(request)
                    if user_role != "user":
                        print("منور يعم النتس اتفضل")
                        pass
                    else:
                        threading.Thread(target=update_views, args=(product, request.user)).start()
                except ClientToken.DoesNotExist:
                    print("DoesNotExist")
                    pass
            serializer = ProductSerializer(product)
            if serializer:
                # print("done+1")
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])  # لا حاجة لـ 'GET' لأن هذا `POST` فقط
@permission_classes([IsAdminOrWorker])  # السماح فقط للمسؤولين والموظفين
def newproduct(request):
    try:
        if request.method == 'POST':
            user_role = getUserType(request) # استخراج الـ role من كائن المستخدم
            serializer = NewProductSerializer(data=request.data,many=True, context={"request": request ,"user_role": user_role})
            if serializer.is_valid():
                serializer.save()
                serializer2 =ProductSerializer(serializer.instance,many=True)
                return Response(serializer2.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['PUT','DELETE'])
@permission_classes([IsAdminOrWorker])
def editproduct(request, QRNumber):
    try:
        try:
            product = Product.objects.get(QRNumber=QRNumber)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
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
############################# END Product #############################




############################# Category #############################

# get all categories , add new category
class CategoriesView(APIView):
    def get(self, request):
        """ إرجاع جميع التصنيفات """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
####################################### get category with category name , Update and Delete category###############3
@csrf_exempt
@api_view(['GET'])
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
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAdminUser])
def categoryadd(request):
    try:
        if request.method == 'POST':
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(['PUT','DELETE'])
@permission_classes([IsAdminOrWorker])
def categoryedite(request, CategoryName):
    try:
        category = Category.objects.get(CategoryName=CategoryName)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
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
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rate(request):
    try:
        if request.method == 'GET':
            rates = Rate.objects.all()
            serializer = RateSerializer(rates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET','POST','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def getAllProductRates(request,QRNumber):
    try:
        product = Product.objects.filter(QRNumber=QRNumber).first()
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            rates = Rate.objects.filter(ProductName=product)
            if not rates:
                return Response({"message": "No Rates yet"}, status=status.HTTP_404_NOT_FOUND)
            serializer = RateSerializer(rates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
            try:
                client_user = request.user
                user_type=getUserType(request)
                if user_type not in ['user']:
                    return Response({"error": f"{user_type} can't be rated or updated rats"}, status=status.HTTP_401_UNAUTHORIZED)
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
                        serializer = RateSerializer(existing_rate, data=request_data)
                        if serializer.is_valid():
                            serializer.save()
                            update_product_rating(product)
                            return Response(
                                {
                                    "message": "you was Rate this product and the Rate updated successfully.",
                                    "data": serializer.data,
                                },
                                status=status.HTTP_200_OK,
                            )
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
                elif request.method == 'DELETE':  # Delete
                    rate_instance = Rate.objects.filter(ProductName=product, ClientUserName=client_user).first()
                    if not rate_instance:
                        return Response({"error": "Rate not found for this product."},
                                        status=status.HTTP_404_NOT_FOUND)
                    rate_instance.delete()
                    update_product_rating(product)
                    return Response({"message": "Rate deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)



### get AllClient Rates with clientUserName ##
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllClientRates(request):
    try:
        user_type=getUserType(request)
        print(user_type)
        if user_type in["user"]:
            if request.method == 'GET':
                client_user = request.user
                if str(client_user):
                    rates = Rate.objects.filter(ClientUserName=client_user.id)
                    serializer = RateSerializer(rates, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Client is Not Found or not the same Authorization"}, status=status.HTTP_404_NOT_FOUND)
        elif user_type in ["admin","worker"]:
            if request.method == 'GET':
                return Response({"error": "You Act as Admin or worker"}, status=status.HTTP_404_NOT_FOUND)
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


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAdminOrWorker])
def getAllProudactThatViewByClient(request,clientUserName):
    try:
        if request.method == 'GET':
            client_user = client.objects.filter(clientUserName=clientUserName).first()
            if not client_user:
                return Response({"error": "Client User not found"}, status=status.HTTP_404_NOT_FOUND)
            user_views = View.objects.filter(ClientUserName=client_user.id).order_by('-LastView')
            if not user_views.exists():
                return Response({"message": "No views found for this user."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ViewSerializer(user_views, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Method not allowed"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsClientUser])
def getlastview(request):
    try:
        if request.method == 'GET':
            client_user = request.user
            if not client_user:
                return Response({"error": "Client User not found"}, status=status.HTTP_404_NOT_FOUND)
            user_views = View.objects.filter(ClientUserName=client_user.id).order_by('-LastView')[:3]
            if not user_views.exists():
                return Response({"message": "No views yet."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ViewSerializer(user_views, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Method not allowed"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAdminOrWorker])
def getAllProudactView(request,QRNumber):
    try:
        if request.method == 'GET':
            print(IsAdminOrWorker)
            product = Product.objects.filter(QRNumber=QRNumber).first()
            if not product:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            product_views = View.objects.filter(ProductName=product)
            if not product_views.exists():
                return Response({"message": "No views found for this product."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ViewSerializer(product_views, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Method not allowed"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





#################################### My Wishlist #############################
class MyWishlistView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request):
        client = request.user
        wishlist = Wishlist.objects.filter(client=client)
        if not wishlist:
            return Response({"message": "empty"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, qr_number):
        client = request.user
        product = get_object_or_404(Product, QRNumber=qr_number)
        wishlist_item, created = Wishlist.objects.get_or_create(client=client, product=product)

        if not created:
            return Response({"error": "Product already in wishlist"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Product added to wishlist"}, status=status.HTTP_201_CREATED)

    def delete(self, request, qr_number):
        client = request.user
        wishlist_item = Wishlist.objects.filter(client=client, product__QRNumber=qr_number).first()

        if wishlist_item:
            wishlist_item.delete()
            return Response({"message": "Product removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Product not in wishlist"}, status=status.HTTP_404_NOT_FOUND)


class AllWishlistsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrWorker]

    def get(self, request):
        wishlist = Wishlist.objects.select_related('client', 'product')
        data = [
            {"client": w.client.clientUserName, "product": w.product.ProductName, "added_at": w.added_at}
            for w in wishlist
        ]
        return Response(data, status=status.HTTP_200_OK)


class UserWishlistView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrWorker]

    def get(self, request, clientUserName):
        Client = get_object_or_404(client, clientUserName=clientUserName)
        wishlist = Wishlist.objects.filter(client=Client)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


############################### data analysis ###############
class StatisticsView(APIView):
    permission_classes = [IsAdminOrWorker]  # اجعلها اختيارية إذا لم يكن هناك توثيق مطلوب

    def get(self, request):
        data = {
            "Categories": Category.objects.count(),
            "Products": Product.objects.count(),
            "Rates": Rate.objects.count(),
            "Customers": client.objects.count(),
            "Feedback": Rate.objects.exclude(Comment__isnull=True).exclude(Comment="").count(),
            "Carts": "not yet", #Cart.objects.count(),
            "Orders":0
        }
        return Response(data)

class CommentsListView(APIView):
    permission_classes = [IsAdminOrWorker]

    def get(self, request):
        comments = Rate.objects.exclude(Comment__isnull=True).exclude(Comment="")
        data = [
            {
                "product": rate.ProductName.ProductName,  # اسم المنتج
                "comment": rate.Comment,  # نص التعليق
                "customer": rate.ClientUserName.clientUserName  # اسم العميل
            }
            for rate in comments
        ]

        return Response(data)


class CategoriesWithProductCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()

        data = [
            {
                "category": category.CategoryName,  # اسم الـ Category
                "products": category.ProductCategory.count()  # عدد المنتجات المرتبطة بها
            }
            for category in categories
        ]

        return Response(data)