from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VirtualCartViewSet ,VirtualCartCheckOut ,cart ,EsyCartVirtualCartCheckIn,EasyCartItems,EasyCartView,refresh_token_view,EasyCartAdminItemsView,CheckoutAPIView,UserInvoicesAPIView
from .views import AllInvoicesAPIView ,EasyCartAPIView,UpdateCartLocationWeightAPIView
urlpatterns = [
    path('Virtual/',VirtualCartViewSet.as_view() ,name='virtual_cart'),
    path('virtual/checkout/', VirtualCartCheckOut.as_view(), name='virtual_cart'),
    path('EsyCartCheckIn/', EsyCartVirtualCartCheckIn.as_view(), name='esy_cart'),
    path('EsyCart/<str:EasycartID>/', EasyCartView.as_view(), name='esy_cart'),
    path('EsyCart/<str:EasycartID>/items/', EasyCartAdminItemsView.as_view(), name='EasyCartAdminItemsView'),
    path('manageEsyCart/',EasyCartAPIView.as_view(), name='EasyCartAddItem'),
    path('EasyCartItems/', EasyCartItems.as_view(), name='easy_cart'),
    path('refreshtoken/', refresh_token_view, name='refresh_token'),
    path('EasyCartchechout/', CheckoutAPIView.as_view(), name='easy_cart'),
    path('myoldcart/',UserInvoicesAPIView.as_view(), name='mycart'),
    path('lastPurchased/',AllInvoicesAPIView.as_view(), name='lastPurchased'),
    path('cart/', cart, name='cart'),
    path('UpdateCart/<str:EasycartId>/', UpdateCartLocationWeightAPIView.as_view(), name='update_cart'),

]
