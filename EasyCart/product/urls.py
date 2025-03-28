from django.urls import path , include,re_path
from . import views
from .views import CategoriesView, MyWishlistView, AllWishlistsView, UserWishlistView

urlpatterns = [
    path('', views.products, name='product'),
    path('getall/', views.getallproducts, name='getallproducts'),
    path('add/', views.newproduct, name='newproduct'),
    path('categories/',CategoriesView.as_view(), name='categories'),
    path('categories/create/',views.categoryadd, name='addcategory'),
    # path('rate',views.RateView.as_view(), name='rate'),
    path('rate/', views.rate, name='rate'),
    path('rate/<str:QRNumber>/', views.getAllProductRates, name='getAllProductRates'),
    path('rate/get/myrates/', views.getAllClientRates, name='getAllClientRates'),
    path('view/for/<str:clientUserName>/', views.getAllProudactThatViewByClient, name='getAllProudactThatViewByClient'),
    path('view/<str:QRNumber>/', views.getAllProudactView, name='getAllProudactView'),
    path('lastview/', views.getlastview, name='lastview'),

    path('categories/<str:CategoryName>/', views.categoryedite, name='categorydetails'),
    path('categories/<str:CategoryName>/details/', views.categorydetails, name='categorydetails'),

    path('in/<str:CategoryName>/', views.getProductsInCategory, name='getProductsInCategory'),
    path('<str:QRNumber>/', views.productdetails, name='productdetails'),
    path('edit/<str:QRNumber>/', views.editproduct, name='editproduct'),

    path('wishlist/getmywish/', MyWishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<str:qr_number>/', MyWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<str:qr_number>/', MyWishlistView.as_view(), name='remove_from_wishlist'),
    path('wishlist/all/', AllWishlistsView.as_view(), name='all_wishlists'),
    path('wishlist/user/<str:clientUserName>/', UserWishlistView.as_view(), name='user_wishlist'),

]