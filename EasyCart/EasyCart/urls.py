from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('', include("home.urls"), name="home"),

    path('admin/', admin.site.urls),
    path('user/',include("User.urls") ,name= "user" ),
    path('product/',include("product.urls"),name= "product"),
    path('worker/',include("worker.urls"),name= "worker"),
    path('cart/', include("cart.urls"), name="cart"),

                  #API
    path('api/', include('rest_framework.urls')),
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
