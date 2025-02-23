from django.urls import path , include,re_path
from . import views

urlpatterns = [
    path('', views.products, name='product'),
    path('getall/', views.getallproducts, name='getallproducts'),
    path('add/', views.newproduct, name='newproduct'),
    path('categories/',views.categories, name='categories'),
    # path('rate',views.RateView.as_view(), name='rate'),
    path('rate/', views.rate, name='rate'),
    path('rate/<str:QRNumber>/', views.getAllProductRates, name='getAllProductRates'),
    path('rate/for/<str:clientUserName>/', views.getAllClientRates, name='getAllClientRates'),
    path('view/for/client/', views.getAllProudactThatViewByClient, name='getAllProudactThatViewByClient'),
    path('view/<str:QRNumber>/', views.getAllProudactView, name='getAllProudactView'),

    path('categories/<str:CategoryName>/', views.categorydetails, name='categorydetails'),
    path('in/<str:CategoryName>/', views.getProductsInCategory, name='getProductsInCategory'),
    path('<str:QRNumber>/', views.productdetails, name='productdetails'),

]