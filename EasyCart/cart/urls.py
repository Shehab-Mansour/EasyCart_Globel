from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VirtualCartViewSet ,VirtualCartCheckOut ,cart ,EsyCartVirtualCartCheckIn,EasyCartItems,EasyCartView,refresh_token_view,EasyCartAdminItemsView

urlpatterns = [
    path('Virtual/',VirtualCartViewSet.as_view() ,name='virtual_cart'),
    path('virtual/checkout/', VirtualCartCheckOut.as_view(), name='virtual_cart'),
    path('EsyCartCheckIn/', EsyCartVirtualCartCheckIn.as_view(), name='esy_cart'),
    path('EsyCart/<str:EasycartID>/', EasyCartView.as_view(), name='esy_cart'),
    path('EsyCart/<str:EasycartID>/items/', EasyCartAdminItemsView.as_view(), name='EasyCartAdminItemsView'),

    path('EasyCartItems/', EasyCartItems.as_view(), name='easy_cart'),
    path('refreshtoken/', refresh_token_view, name='refresh_token'),
    path('cart/', cart, name='cart'),

]
