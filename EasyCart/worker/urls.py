#
# from django.urls import path
# from .views import *
# from . import views
#
# from django.conf.urls.static import static
# from django.conf import settings
# from .views import (
#     AdminLoginView, AdminCreateWorkerView, AdminCreateAdminView,
#     AdminUpdateProfileView, AdminManageJobsView, WorkerLoginView,
#     WorkerUpdateProfileView, LogoutView
# )
# urlpatterns = [
#     #APIS
#     # path('',views.worker,name= "worker"),
#     # path('login',views.workerlogin,name= "workerlogin"),
#     # path('worker/register/', WorkerRegisterView.as_view(), name='worker-register'),
#     # path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
#     # path('login/', WorkerLoginView.as_view(), name='worker-login'),
#     # path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
#     path('getall/',views.getallWorkers,name= "getallworkers"),
#   # Admin URLs
#   path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
#   path('admin/create-worker/', AdminCreateWorkerView.as_view(), name='admin-create-worker'),
#   path('admin/create-admin/', AdminCreateAdminView.as_view(), name='admin-create-admin'),
#   path('admin/update-profile/', AdminUpdateProfileView.as_view(), name='admin-update-profile'),
#   path('admin/manage-jobs/', AdminManageJobsView.as_view(), name='admin-manage-jobs'),
#   path('admin/manage-jobs/<int:job_id>/', AdminManageJobsView.as_view(), name='admin-update-job'),
#
#   # Worker URLs
#   path('worker/login/', WorkerLoginView.as_view(), name='worker-login'),
#   path('worker/update-profile/', WorkerUpdateProfileView.as_view(), name='worker-update-profile'),
#
#   # Common Logout
#   path('logout/', LogoutView.as_view(), name='logout'),
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import (
    AdminLoginView,
    AdminCreateWorkerView,
    AdminCreateAdminView,
    AdminUpdateProfileView,
    AdminManageJobsView,
    WorkerLoginView,
    WorkerUpdateProfileView,

    WorkerProfileView,
    getallWorkers,

LogoutView

)

urlpatterns = [
    # Admin URLs
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/create-worker/', AdminCreateWorkerView.as_view(), name='admin-create-worker'),
    path('admin/create-admin/', AdminCreateAdminView.as_view(), name='admin-create-admin'),
    path('admin/update-profile/', AdminUpdateProfileView.as_view(), name='admin-update-profile'),
    path('admin/manage-jobs/', AdminManageJobsView.as_view(), name='admin-manage-jobs'),
    path('admin/manage-jobs/<int:job_id>/', AdminManageJobsView.as_view(), name='admin-update-job'),
    path('admin/get-all-workers/', getallWorkers, name='get-all-workers'),

    # Worker URLs
    path('worker/login/', WorkerLoginView.as_view(), name='worker-login'),
    path('worker/update-profile/', WorkerUpdateProfileView.as_view(), name='worker-update-profile'),
    path('worker/profile/', WorkerProfileView.as_view(), name='worker-profile'),

    # Common URLs
    # path('admin/logout/', AdminLogoutView.as_view(), name='logout'),
    # path('worker/logout/', WorkerLogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)