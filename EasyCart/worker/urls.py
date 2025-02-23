
from django.urls import path
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #APIS
    path('',views.worker,name= "worker"),
    path('getall/',views.getallWorkers,name= "getallworkers"),
    path('job/', views.job, name="job"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
