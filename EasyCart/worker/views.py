from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from .serializer import LoginSerializer, WorkerPermissionSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import WorkerSerializer ,AdminSerializer,JobSerializer
from rest_framework_simplejwt.exceptions import TokenError
from .authentication import  CustomAuthentication ,getUserType
from .models import Worker, Job, Admin, WorkerPermission
from rest_framework_simplejwt.views import TokenRefreshView
from .permission import IsAdminUser, IsWorker


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    authentication_classes = [CustomAuthentication]
    def delete(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateView(generics.CreateAPIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAdminUser]
    def post(self, request):
        role = request.data.get('role')  # تحديد نوع المستخدم (Worker أو Admin)
        if role == "worker":
            JobName = request.data.get('WorkerJobTitle')
            job_id = get_object_or_404(Job, JobName=JobName).id
            request.data["WorkerJobTitle"] = job_id
            if not Job.objects.filter(id=job_id).exists():
                return Response({"error": "Invalid Job. Please select a valid job."},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = WorkerSerializer(data=request.data)
            if serializer.is_valid():
                worker = serializer.save(WorkerPassword=make_password(serializer.validated_data['WorkerUserName']))
                return Response({"message": "Worker created successfully."}, status=status.HTTP_201_CREATED)
        elif role == "admin":
            serializer = AdminSerializer(data=request.data)
            if serializer.is_valid():
                admin = serializer.save(Password=make_password(serializer.validated_data['UserName']))
                return Response({"message": "Admin created successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid role. Choose either 'Worker' or 'Admin'."},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self, request):
        usertype = getUserType(request)
        if usertype == 'admin' :  # Check if user is admin
            serializer = AdminSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif usertype == 'worker':  # Check if user is worker
            serializer = WorkerSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'Unauthorized'}, status=403)

class UpdateProfileView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user  # الحصول على المستخدم الحالي
        # تحديد نوع المستخدم (Worker أو Admin)
        if isinstance(user, Worker):
            restricted_fields = {"WorkerUserName", "WorkerSalary", "WorkerJobTitle"}
            serializer = WorkerSerializer(user, data=request.data, partial=True)
        elif isinstance(user, Admin):
            restricted_fields = {"UserName" ,"IsSuperAdmin"}
            serializer = AdminSerializer(user, data=request.data, partial=True)
        else:
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)
        for field in restricted_fields:
            request.data.pop(field, None)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully.",
                "updated_data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminManageJobsView(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Job added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 🔹 عرض كل الوظائف (Admin فقط)
class JobListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = "JobName"  # البحث يتم بناءً على JobName
    lookup_url_kwarg = "JobName"  # تحديد اسم البراميتر في الـ URL
    def get_object(self):
        JobName = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(Job, JobName=JobName)

# 🔹 إضافة أو تعديل صلاحيات الوظيفة (Admin فقط)
class WorkerPermissionView(generics.RetrieveAPIView,generics.CreateAPIView, generics.UpdateAPIView):
    queryset = WorkerPermission.objects.all()
    serializer_class = WorkerPermissionSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "job__JobName"  # البحث عن الوظيفة عبر JobName بدلاً من pk

    def get_object(self):
        """البحث عن صلاحيات الوظيفة باستخدام JobName"""
        JobName = self.kwargs.get("JobName")
        job = get_object_or_404(Job, JobName=JobName)
        permission, created = WorkerPermission.objects.get_or_create(JobName=job)  # إنشاء إذا لم يكن موجودًا
        return permission
    def update(self, request, *args, **kwargs):
        """تحديث الصلاحيات الخاصة بالوظيفة"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Permissions updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """إرجاع الصلاحيات الخاصة بالوظيفة عند طلب GET"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "permissions":serializer.data
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getallWorkers(request):
    workers = Worker.objects.select_related('WorkerJobTitle').all()
    serializer = WorkerSerializer(workers, many=True)
    return Response(serializer.data)
