from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from User.permission import IsClientUser
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView

from worker.authentication import CustomAuthentication
from worker.permission import IsAdminOrWorker
from .serializer import *
from .models import  VirtualCart
from functions.cart.user import *
from rest_framework.decorators import api_view, permission_classes


from django.conf import settings
############################## USER Time in cart ########################
access_time=500
refresh_time=50000
SECRET_KEY = settings.SECRET_KEY  # استخدام المفتاح من إعدادات Django
#########################################################################

class VirtualCartViewSet(APIView):
    permission_classes = [IsClientUser]
    serializer_class = VirtualCartSerializer
    def get_queryset(self):
        return VirtualCart.objects.filter(client=self.request.user, isActive=True)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
    def get(self,request):
        cart=self.get_queryset()
        if not cart:
            return Response({"massage":"You dont add product yat"},status=status.HTTP_404_NOT_FOUND)
        # items=VirtualCartItem.objects.filter(cart=cart)
        return Response(VirtualCartSerializer(cart,many=True).data,status=status.HTTP_200_OK)

    def post(self, request):
        try:
            cart = self.get_queryset().first()
            if not cart:
                cart = VirtualCart.objects.create(client=self.request.user, isActive=True)

            qr_number = request.data.get('QRNumber')
            if not qr_number:
                return Response({"error": "QRNumber is Required"}, status=status.HTTP_400_BAD_REQUEST)

            quantity = int(request.data.get('quantity', 1))
            if quantity <= 0:
                return Response({"error": "quantity must be positive"}, status=status.HTTP_400_BAD_REQUEST)

            product = Product.objects.filter(QRNumber=qr_number).first()
            if not product:
                return Response({"error": "product not found"}, status=status.HTTP_404_NOT_FOUND)

            cart_item, created = VirtualCartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response(VirtualCartSerializerData(cart).data, status=status.HTTP_201_CREATED)
        except VirtualCart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            cart = self.get_queryset().first()
            if not cart:
                return Response({"error": "cart not found"}, status=status.HTTP_404_NOT_FOUND)

            products_data = request.data if isinstance(request.data, list) else [request.data]

            for item in products_data:
                qr_number = item.get('QRNumber')
                quantity = int(item.get('quantity', 1))

                if not qr_number:
                    return Response({"error": "QRNumber is required for all items"}, status=status.HTTP_400_BAD_REQUEST)
                if quantity <= 0:
                    return Response({"error": f"quantity must be positive for QRNumber {qr_number}"},
                                    status=status.HTTP_400_BAD_REQUEST)

                product = Product.objects.filter(QRNumber=qr_number).first()
                if not product:
                    return Response({"error": f"product with QRNumber {qr_number} not found"},
                                    status=status.HTTP_404_NOT_FOUND)

                cart_item, created = VirtualCartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': quantity}
                )
                if not created:
                    cart_item.quantity = quantity
                    cart_item.save()

            cart = self.get_queryset().first()
            return Response(VirtualCartSerializerData(cart).data, status=status.HTTP_200_OK)

        except VirtualCart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        try:
            cart = self.get_queryset().first()
            if not cart:
                return Response({"error": "cart not found"}, status=status.HTTP_404_NOT_FOUND)

            products_data = request.data if isinstance(request.data, list) else [request.data]

            for item in products_data:
                qr_number = item.get('QRNumber')
                if not qr_number:
                    return Response({"error": "QRNumber is required for all items"}, status=status.HTTP_400_BAD_REQUEST)

                product = Product.objects.filter(QRNumber=qr_number).first()
                if not product:
                    return Response({"error": f"product with QRNumber {qr_number} not found"},
                                    status=status.HTTP_404_NOT_FOUND)

                VirtualCartItem.objects.filter(cart=cart, product=product).delete()

            cart_items = VirtualCartItem.objects.filter(cart=cart)
            cart.totalQuantity = sum(item.quantity for item in cart_items)
            cart.totalWeight = sum(item.quantity * item.product.ProductWeight for item in cart_items)
            cart.totalPrice=sum(item.product.ProductPrice * item.quantity *(1- item.product.ProductDiscount) for item in cart_items)
            cart.save()
            return Response(VirtualCartSerializerData(cart).data, status=status.HTTP_200_OK)

        except VirtualCart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class  VirtualCartCheckOut(APIView):
    permission_classes = [IsClientUser]
    def post(self, request):
        QRNumber = request.data.get('CartQRNumber')
        if not QRNumber:
            return Response({"error": "CartQRNumber is Required"}, status=status.HTTP_400_BAD_REQUEST)
        cart=VirtualCart.objects.update(client=self.request.user, isActive=True,
            qrCode=QRNumber
        )

        if not cart:
            return Response({"error": "cart not found"}, status=status.HTTP_404_NOT_FOUND)
        cart=VirtualCart.objects.filter(client=self.request.user, isActive=True).first()
        return Response(VirtualCartSerializerData(cart).data, status=status.HTTP_200_OK)


class EsyCartVirtualCartCheckIn(APIView):
    def post(self, request):
        EasyCartdata=getEasyCart(request)
        try:
            if EasyCartdata.status_code:
                return EasyCartdata
        except:
            pass
        QRNumber = request.data.get('CartQRNumber')
        beginningWeight=request.data.get('beginningWeight')
        location=request.data.get('location')
        if not QRNumber:
            return Response({"error": "CartQRNumber is Required"}, status=status.HTTP_400_BAD_REQUEST)
        if not beginningWeight:
            return Response({"error": "beginningWeight is Required"}, status=status.HTTP_400_BAD_REQUEST)
        cart=VirtualCart.objects.filter(qrCode=QRNumber).first()
        if not cart:
            return Response({"error": "cart not found"}, status=status.HTTP_404_NOT_FOUND)
        if not cart.isActive:
            return Response({"error": "cart is inactive"}, status=status.HTTP_404_NOT_FOUND)
        # print(EasyCartdata.cartId)
        user=generate_custom_jwt(EasyCart=EasyCartdata.cartId,user=cart.client,access_time=access_time ,refresh_time=refresh_time)
        if user:
            update = EasyCart.objects.filter(cartId=EasyCartdata.cartId).update(
                lastUsedBy=cart.client,
                cartStatus='in_use',
                location=location,
                VirtualCart=cart,
                beginningWeight=beginningWeight,
                lastUsedAt=now()
            )
            if not update:
                return Response({"error": "Error in Easy Cart"}, status=status.HTTP_404_NOT_FOUND)

            return Response(user, status=status.HTTP_200_OK)



class EasyCartItems(APIView):
    authentication_classes=[CustomAuthentication]
    permission_classes=[IsClientUser]
    def get(self,request):
        EasyCartID=request.auth.get('EasyCart')
        if not EasyCartID:
            return Response({"error": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        EasyCartdata=EasyCart.objects.get(cartId=EasyCartID)
        if not EasyCartdata:
            return Response({"error": "Easy cart not found"}, status=status.HTTP_404_NOT_FOUND)
        cart=VirtualCart.objects.filter(client=EasyCartdata.lastUsedBy)
        if not cart :
            return Response({"error": "You dont have items"}, status=status.HTTP_404_NOT_FOUND)
        EasyCartItems=EasyCartVirtualCart.objects.filter(easyCart=EasyCartID)
        if not EasyCartItems:
            EasyCartItems="empty"
        else:
            EasyCartItems=EasyCartVirtualCartSerializer(EasyCartItems, many=True).data

        data={
            "EasyCartVirtualItems":VirtualCartSerializer(cart,many=True).data,
            "EasyCartItems":EasyCartItems,
        }
        return Response(data,status=status.HTTP_200_OK)

    def post(self, request):
        EasyCartID = request.auth.get('EasyCart')
        if not EasyCartID:
            return Response({"error": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        EasyCartObj = get_object_or_404(EasyCart, cartId=EasyCartID)
        client_obj = EasyCartObj.lastUsedBy
        VirtualCartObj = get_object_or_404(VirtualCart, client=client_obj)

        EasyCartVirtualCartObj, _ = EasyCartVirtualCart.objects.get_or_create(
            easyCart=EasyCartObj,
            client=client_obj
        )

        qr_number = request.data.get('QRNumber')
        quantity = request.data.get('quantity')

        if not qr_number or not quantity:
            return Response({"error": "QRNumber and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except:
            return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, QRNumber=qr_number)

        try:
            virtual_item = VirtualCartItem.objects.get(cart=VirtualCartObj, product=product)
        except VirtualCartItem.DoesNotExist:
            virtual_item = None

        if virtual_item:
            # حساب الكمية اللي هتنقص فعلاً من الكارت الافتراضية
            actual_removed_quantity = min(quantity, virtual_item.quantity)
            removed_price = actual_removed_quantity * product.ProductPrice * (1 - product.ProductDiscount / 100)
            removed_weight = actual_removed_quantity * product.ProductWeight

            if quantity == virtual_item.quantity:
                virtual_item.delete()
            elif quantity > virtual_item.quantity:
                virtual_item.delete()
            else:
                virtual_item.quantity -= quantity
                virtual_item.save()

            # قلل القيم من الكارت الافتراضية
            VirtualCartObj.totalQuantity -= actual_removed_quantity
            VirtualCartObj.totalPrice -= removed_price
            VirtualCartObj.totalWeight -= removed_weight
            VirtualCartObj.save()

            easy_item, created = EasyCartVirtualCartItem.objects.get_or_create(
                cart=EasyCartVirtualCartObj,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                easy_item.quantity += quantity
                easy_item.save()

        else:
            # المنتج مش موجود في الكارت الافتراضية → ضيفه فقط في الكارت الذكية
            easy_item, created = EasyCartVirtualCartItem.objects.get_or_create(
                cart=EasyCartVirtualCartObj,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                easy_item.quantity += quantity
                easy_item.save()
            # ومش بنعدل على VirtualCartObj في الحالة دي

        easy_cart_items_data = EasyCartVirtualCartSerializer(
            [EasyCartVirtualCartObj], many=True
        ).data

        virtual_cart_data = VirtualCartSerializer(
            [VirtualCartObj], many=True
        ).data

        data = {
            "EasyCartVirtualItems": virtual_cart_data,
            "EasyCartItems": easy_cart_items_data,
        }

        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request):
        EasyCartID = request.auth.get('EasyCart')
        if not EasyCartID:
            return Response({"error": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        EasyCartObj = get_object_or_404(EasyCart, cartId=EasyCartID)
        client_obj = EasyCartObj.lastUsedBy
        VirtualCartObj = get_object_or_404(VirtualCart, client=client_obj)

        EasyCartVirtualCartObj, _ = EasyCartVirtualCart.objects.get_or_create(
            easyCart=EasyCartObj,
            client=client_obj
        )

        qr_number = request.data.get('QRNumber')
        quantity = request.data.get('quantity')

        if not qr_number or not quantity:
            return Response({"error": "QRNumber and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except:
            return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, QRNumber=qr_number)

        try:
            easy_item = EasyCartVirtualCartItem.objects.get(cart=EasyCartVirtualCartObj, product=product)
        except EasyCartVirtualCartItem.DoesNotExist:
            return Response({"error": "Product not found in EasyCart."}, status=status.HTTP_404_NOT_FOUND)

        # حساب الكمية اللي هتنقص فعلاً من الكارت الذكية
        actual_removed_quantity = min(quantity, easy_item.quantity)

        if quantity >= easy_item.quantity:
            easy_item.delete()
        else:
            easy_item.quantity -= quantity
            easy_item.save()

        # تحديث أو إنشاء العنصر داخل VirtualCart
        virtual_item, created = VirtualCartItem.objects.get_or_create(
            cart=VirtualCartObj,
            product=product,
            defaults={'quantity': actual_removed_quantity}
        )
        if not created:
            virtual_item.quantity += actual_removed_quantity
            virtual_item.save()

        # تعديل الإجماليات بتاعة VirtualCart
        added_price = actual_removed_quantity * product.ProductPrice * (1 - product.ProductDiscount / 100)
        added_weight = actual_removed_quantity * product.ProductWeight

        VirtualCartObj.totalQuantity += actual_removed_quantity
        VirtualCartObj.totalPrice += added_price
        VirtualCartObj.totalWeight += added_weight
        VirtualCartObj.save()

        items = EasyCartVirtualCartItem.objects.filter(cart=EasyCartVirtualCartObj)
        EasyCartVirtualCartObj.totalQuantity = sum(item.quantity for item in items)
        EasyCartVirtualCartObj.totalPrice = sum(
            item.quantity * item.product.ProductPrice * (1 - item.product.ProductDiscount / 100) for item in items)
        EasyCartVirtualCartObj.totalWeight = sum(item.quantity * item.product.ProductWeight for item in items)
        EasyCartVirtualCartObj.save()

        # البيانات المرجعة
        easy_cart_items_data = EasyCartVirtualCartSerializer(
            [EasyCartVirtualCartObj], many=True
        ).data

        virtual_cart_data = VirtualCartSerializer(
            [VirtualCartObj], many=True
        ).data

        data = {
            "EasyCartVirtualItems": virtual_cart_data,
            "EasyCartItems": easy_cart_items_data,
        }

        return Response(data, status=status.HTTP_200_OK)


class EasyCartView(APIView):
    authentication_classes=[CustomAuthentication]
    permission_classes=[IsAdminOrWorker]
    def get(self, request, EasycartID):
        EasyCartdata = EasyCart.objects.filter(cartId=EasycartID).first()
        if not EasyCartdata:
            return Response({"error": "Easy Cart Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(EasyCartSerializer(EasyCartdata).data, status=status.HTTP_200_OK)
    def delete(self, request, EasycartID):
        EasyCartdata = EasyCart.objects.filter(cartId=EasycartID).first()
        if not EasyCartdata:
            return Response({"error": "Easy Cart Not found"}, status=status.HTTP_404_NOT_FOUND)
        EasyCartdata.cartStatus = "ready"
        EasyCartdata.VirtualCart = None
        EasyCartdata.lastUsedBy = None
        EasyCartdata.save(update_fields=["cartStatus", "VirtualCart", "lastUsedBy"])  # تحديث الحقل فقط
        if EasyCartdata.cartStatus == "ready":
            EasyCartd = EasyCart.objects.filter(cartId=EasycartID).first()
            return Response(EasyCartSerializer(EasyCartd).data, status=status.HTTP_200_OK)
        else:
            error = f"Cart is {EasyCartdata.cartStatus}"
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request,EasycartID):
        # تعديل كارت موجود
        cart_id = EasycartID
        battery = request.data.get('batteryPercentage')
        location = request.data.get('location')
        try:
            cart = EasyCart.objects.get(cartId=cart_id)
            if battery is not None:
                cart.batteryPercentage = battery
            if location is not None:
                cart.location = location
            cart.save()
            return Response({"message": "Cart updated"}, status=status.HTTP_200_OK)
        except EasyCart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

class EasyCartAdminItemsView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAdminOrWorker]
    def get(self, request, EasycartID):
        EasyCartdata = EasyCart.objects.filter(cartId=EasycartID).first()
        if not EasyCartdata:
            return Response({"error": "Easy Cart Not found"}, status=status.HTTP_404_NOT_FOUND)
        cartItems=EasyCartVirtualCart.objects.filter(easyCart=EasyCartdata).all()

        return Response(EasyCartVirtualCartSerializer(cartItems,many=True).data, status=status.HTTP_200_OK)


class CheckoutAPIView(APIView):
    authentication_classes=[CustomAuthentication]
    permission_classes=[IsClientUser]
    def post(self, request):
        user = request.user
        try:
            EasyCartID = request.auth.get('EasyCart')
            if not EasyCartID:
                return Response({"error": "Not Authorized"}, status=status.HTTP_401_UNAUTHORIZED)
            EasyCartVc=EasyCartVirtualCart.objects.filter(easyCart=EasyCartID).first()
            if not EasyCartVc :
                return Response({"error":"You must log in first or Easy Cart is empty"},status=status.HTTP_401_UNAUTHORIZED)

            if EasyCartVc.items.count() == 0:
                return Response({"detail": "Easy Cart is empty"}, status=400)
            if EasyCartVc.totalPrice >0:
                purchased_cart = PurchasedCart.objects.create(
                    client=user,
                    totalAmount=EasyCartVc.totalPrice,
                    totalWeight=EasyCartVc.totalWeight,
                    totalQuantity=EasyCartVc.totalQuantity,
                    # paymentMethod=request.data.get("paymentMethod", "Card NFC"),
                    paymentMethod="Card NFC",
                    nfcTransactionId=request.data.get("nfcTransactionId")
                )

                for item in EasyCartVc.items.all():
                    crate= PurchasedCartItem.objects.create(
                        cart=purchased_cart,
                        product=item.product,
                        quantity=item.quantity,
                        priceAtPurchase=item.product.ProductPrice,
                        purchasedAt=now()
                    )

                if crate:
                    Pdata=PurchasedCartSerializer(purchased_cart).data
                    if Pdata:
                        virtual_cart = VirtualCart.objects.get(client=user)
                        EasyCartdata = EasyCart.objects.filter(cartId=EasyCartID).first()
                        if not EasyCartdata:
                            return Response({"error": "Easy Cart Not found"}, status=status.HTTP_404_NOT_FOUND)
                        EasyCartdata.cartStatus = "ready"
                        EasyCartdata.VirtualCart = None
                        EasyCartdata.lastUsedBy = None
                        EasyCartdata.save(update_fields=["cartStatus", "VirtualCart", "lastUsedBy"])
                        virtual_cart.delete()
                        EasyCartVc.delete()
                        # print("comp")
                        # print(PurchasedCartSerializer(purchased_cart).data)
                        return Response({
                            "detail": "Transaction completed successfully",
                            "invoice":PurchasedCartSerializer(purchased_cart).data
                        })
                else:
                    return Response("error : Transaction fielded", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error:you must add items"})

        except VirtualCart.DoesNotExist:
            return Response({"detail": "Not Authorized"}, status=404)



class UserInvoicesAPIView(ListAPIView):
    serializer_class = PurchasedCartSerializer
    authentication_classes=[CustomAuthentication]
    permission_classes = [IsClientUser]
    def get_queryset(self):
        return PurchasedCart.objects.filter(client=self.request.user).order_by('-createdAt')


from rest_framework.permissions import IsAdminUser

class AllInvoicesAPIView(ListAPIView):
    serializer_class = AdminPurchasedCartSerializer
    authentication_classes=[CustomAuthentication]
    permission_classes = [IsAdminOrWorker]
    def get_queryset(self):
        return PurchasedCart.objects.all().order_by('-createdAt')



class EasyCartAPIView(APIView):
    authentication_classes=[CustomAuthentication]
    permission_classes = [IsAdminOrWorker]
    def get(self, request):
        cart=EasyCart.objects.all()
        serializer = EasyCartSerializer(cart, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    def post(self, request):
        # battery = request.data.get('batteryPercentage')
        battery=90
        location = request.data.get('location')
        if battery is None or location is None:
            return Response({"error": "batteryPercentage and location are required"}, status=status.HTTP_400_BAD_REQUEST)
        cart = EasyCart.objects.create(batteryPercentage=battery, location=location)
        return Response({"message": "Cart created", "id": cart.cartId}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        cart_id = request.data.get('cartId')
        try:
            cart = EasyCart.objects.get(cartId=cart_id)
            cart.delete()
            return Response({"message": "Cart deleted"}, status=status.HTTP_200_OK)
        except EasyCart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)



@csrf_exempt
@api_view(['POST'])
def refresh_token_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            refresh_token = data.get("refresh")

            if not refresh_token:
                return JsonResponse({"error": "Refresh token is required"}, status=400)

            # فك التشفير للتحقق من صحة التوكن
            decoded_payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])

            user_id = decoded_payload.get("user_id")
            user_role = decoded_payload.get("user_type")  # متسجل كده في generate_custom_jwt
            EasyCart = decoded_payload.get("EasyCart")

            # إنشاء Access Token جديد فقط بنفس البيلود
            jti_access = str(uuid.uuid4())
            current_time = datetime.utcnow()

            new_access_payload = {
                "token_type": "access",
                "jti": jti_access,
                "sub": str(user_id),
                "user_id": user_id,
                "user_type": user_role,
                "EasyCart": EasyCart,
                "exp": current_time + timedelta(minutes=access_time),
                "iat": current_time,
            }

            new_access_token = jwt.encode(new_access_payload, SECRET_KEY, algorithm="HS256")

            return JsonResponse({"access": new_access_token})

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Refresh token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid refresh token"}, status=401)

    return JsonResponse({"error": "Invalid request method"}, status=405)




class UpdateCartLocationWeightAPIView(APIView):
    def put(self, request, EasycartId):
        location = request.data.get("location")
        weight = request.data.get("weight")

        if location is None or weight is None:
            return Response(
                {"error": "location and weight are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            cart = EasyCart.objects.get(cartId=EasycartId)
            cart.location = location
            cart.weight = weight
            cart.save(update_fields=["location", "weight", "updatedAt"])
            return Response({"message": "Cart updated successfully"}, status=status.HTTP_200_OK)

        except EasyCart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)




@csrf_exempt
@api_view(['PUT'])
def cart(request):
    EasyCart.objects.create(batteryPercentage=50, location="Aisle 2")
    return Response("done", status=status.HTTP_200_OK)

