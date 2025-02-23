
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    #API
    path('getclient/', views.getclient, name='getclient'),
    path('register/', views.register, name='register'),
    path('client/<str:clientUserName>/', views.userdetail, name='userdetail'),
    path('client/<str:clientUserName>/admin/', views.adminGetUserDetail, name='adminGetUserGetail'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
