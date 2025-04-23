from django.urls import path , include,re_path
from . import views
from .views import CategoriesView, MyWishlistView, AllWishlistsView, UserWishlistView, StatisticsView, CommentsListView, \
    CategoriesWithProductCountView, CategorySalesGraphAPIView, ProductCategorySearchAPIView, SearchHistoryListAPIView, \
    bar_chart_top_4_categories_last_4_months, sales_last_12_months_chart

urlpatterns = [
    # path('', views.products, name='product'),
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

    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('statistics/feedback/', CommentsListView.as_view(), name='statistics'),
    path('statistics/pie_chart/', CategoriesWithProductCountView.as_view(), name='statistics'),
    path('statistics/scatter/', CategorySalesGraphAPIView.as_view(), name='statistics'),
    path('statistics/bar_chart/', bar_chart_top_4_categories_last_4_months, name='statistics'),
    path('statistics/line_chart/', sales_last_12_months_chart, name='statistics'),

    path('search/', ProductCategorySearchAPIView.as_view(), name='search'),
    path('searchhistory/', SearchHistoryListAPIView.as_view(), name='search'),


    path('in/<str:CategoryName>/', views.getProductsInCategory, name='getProductsInCategory'),
    path('edit/<str:QRNumber>/', views.editproduct, name='editproduct'),

    path('wishlist/getmywish/', MyWishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<str:qr_number>/', MyWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<str:qr_number>/', MyWishlistView.as_view(), name='remove_from_wishlist'),
    path('wishlist/all/', AllWishlistsView.as_view(), name='all_wishlists'),
    path('wishlist/user/<str:clientUserName>/', UserWishlistView.as_view(), name='user_wishlist'),
    path('<str:QRNumber>/', views.productdetails, name='productdetails'),

]