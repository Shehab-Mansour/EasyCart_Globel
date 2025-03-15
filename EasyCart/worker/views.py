
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Admin, Worker, Job,AdminToken,WorkerToken
from .serializer import AdminSerializer, WorkerSerializer, JobSerializer
from django.utils.timezone import now, timedelta
from .permission import IsAdminRole
from .models import WorkerToken
from worker.authentication import WorkerTokenAuthentication

class WorkerProfileView(APIView):
    authentication_classes = [WorkerTokenAuthentication]  # 🔥 المصادقة بالتوكن المخصص

    def get(self, request):
        worker = request.user  # 🔥 الآن `request.user` يحتوي على العامل الصحيح
        return Response({
            'username': worker.WorkerUserName,
            'role': request.auth.role,  # `request.auth` يحتوي على التوكن
            'job_title': worker.WorkerJobTitle.JobName if worker.WorkerJobTitle else "N/A",
            'email': worker.WorkerEmail,
            'phone': worker.WorkerPhone
        })



class AdminLoginView(APIView):
    def post(self, request):
        username = request.data.get('UserName')
        password = request.data.get('Password')
        admin = Admin.objects.filter(UserName=username).first()

        if admin and check_password(password, admin.Password):
            refresh = RefreshToken.for_user(admin)

            # تحديد الدور المناسب
            role = 'super_admin' if admin.IsSuperAdmin else 'manager'
            send=refresh.access_token

            # إنشاء AdminToken وتخزينه في قاعدة البيانات
            AdminToken.objects.create(
                admin=admin,
                token=str(send),
                role=role,
                expires_at=now() + timedelta(days=7)  # صلاحية 7 أيام
            )

            return Response({
                'access': str(send),
                'refresh': str(refresh),
                'role': role
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#
# class WorkerLoginView(APIView):
#     def post(self, request):
#         username = request.data.get('WorkerUserName')
#         password = request.data.get('WorkerPassword')
#
#         # البحث عن العامل في قاعدة البيانات
#         worker = Worker.objects.filter(WorkerUserName=username).first()
#
#         if worker and check_password(password, worker.WorkerPassword):
#             # توليد JWT Token
#             refresh = RefreshToken.for_user(worker)
#
#             # تحديد الدور تلقائيًا
#             role = 'supervisor' if worker.IsSupervisor else 'basic_worker'
#
#             # إنشاء WorkerToken وتخزينه في قاعدة البيانات
#             WorkerToken.objects.create(
#                 worker=worker,
#                 token=str(refresh.access_token),
#                 role=role,
#                 expires_at=now() + timedelta(days=7)  # صلاحية 7 أيام
#             )
#
#             return Response({
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#                 'role': role
#             }, status=status.HTTP_200_OK)
#
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class WorkerLoginView(APIView):
    def post(self, request):
        username = request.data.get('WorkerUserName')
        password = request.data.get('WorkerPassword')

        # البحث عن العامل في قاعدة البيانات
        worker = Worker.objects.filter(WorkerUserName=username).first()

        if worker and check_password(password, worker.WorkerPassword):
            # ✅ توليد توكنات JWT يدويًا
            refresh = RefreshToken()
            refresh.payload['worker_id'] = worker.id  # ⬅️ إضافة worker_id داخل الـ JWT
            send=refresh.access_token

            # ✅ تحديد الدور تلقائيًا
            role = 'supervisor' if worker.IsSupervisor else 'basic_worker'

            # ✅ إنشاء WorkerToken وتخزينه في قاعدة البيانات
            WorkerToken.objects.create(
                worker=worker,
                token=str(send),
                role=role,
                expires_at=now() + timedelta(days=7)  # صلاحية 7 أيام
            )

            return Response({
                'access': str(send),
                'refresh': str(refresh),
                'role': role
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AdminCreateWorkerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        JobName = request.data.get('WorkerJobTitle')
        job_id= get_object_or_404(Job, JobName=JobName).id
        request.data["WorkerJobTitle"]=job_id

        # تحقق من وجود الوظيفة
        if not Job.objects.filter(id=job_id).exists():
            return Response({"error": "Invalid Job. Please select a valid job."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            worker = serializer.save(WorkerPassword=make_password(serializer.validated_data['WorkerUserName']))
            return Response({"message": "Worker created successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreateAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save(Password=make_password(serializer.validated_data['UserName']))
            return Response({"message": "Admin created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        admin = request.user
        serializer = AdminSerializer(admin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminManageJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Job added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, job_id):
        job = Job.objects.get(id=job_id)
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Job updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#
# class WorkerLoginView(APIView):
#     def post(self, request):
#         username = request.data.get('WorkerUserName')
#         password = request.data.get('WorkerPassword')
#
#         # البحث عن العامل في قاعدة البيانات
#         worker = Worker.objects.filter(WorkerUserName=username).first()
#
#         if worker and check_password(password, worker.WorkerPassword):
#             # توليد JWT Token
#             refresh = RefreshToken.for_user(worker)
#
#             # تحديد الدور تلقائيًا
#             role = 'supervisor' if worker.IsSupervisor else 'basic_worker'
#
#             # إنشاء WorkerToken وتخزينه في قاعدة البيانات
#             WorkerToken.objects.create(
#                 worker=worker,
#                 token=str(refresh.access_token),
#                 role=role,
#                 expires_at=now() + timedelta(days=7)  # صلاحية 7 أيام
#             )
#
#             return Response({
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#                 'role': role
#             }, status=status.HTTP_200_OK)
#
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class WorkerUpdateProfileView(APIView):

    authentication_classes = [WorkerTokenAuthentication]


    def post(self, request):
        print(request.data)
        worker = Worker.objects.filter(id=request.user.id).first()  # جلب العامل بناءً على ID

        if not worker:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WorkerSerializer(worker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class LogoutView(APIView):
#     authentication_classes = [WorkerTokenAuthentication]
#     print(WorkerTokenAuthentication)
#     if WorkerTokenAuthentication:
#         permission_classes = [IsAuthenticated]
#
#
#     def delete(self, request):
#         try:
#             refresh_token = request.data.get('refresh')
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#
#             if hasattr(request.user, 'worker'):
#                 WorkerToken.objects.filter(token=str(token.access_token)).delete()
#             elif hasattr(request.user, 'admin'):
#                 AdminToken.objects.filter(token=str(token.access_token)).delete()
#
#             return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
#
# #
# class AdminLogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def delete(self, request):
#         try:
#             auth_header = request.headers.get('Authorization')
#
#             if not auth_header or not auth_header.startswith('Bearer '):
#                 return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
#
#             token = auth_header.split(' ')[1]
#
#             # حذف التوكن من جدول التوكنات
#             deleted_count = AdminToken.objects.filter(token=str(token)).delete()[0]
#             if deleted_count == 0:
#                 return Response({"warning": "Token not found in database, but blacklisted."}, status=status.HTTP_200_OK)
#
#             return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
#
#         except TokenError as e:
#             return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
#
# class WorkerLogoutView(APIView):
#     authentication_classes = [WorkerTokenAuthentication]
#
#     def delete(self, request):
#         try:
#             auth_header = request.headers.get('Authorization')
#
#             if not auth_header or not auth_header.startswith('Bearer '):
#                 return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
#
#             token = auth_header.split(' ')[1]
#
#             # حذف التوكن من جدول التوكنات
#             deleted_count = WorkerToken.objects.filter(token=str(token)).delete()[0]
#             if deleted_count == 0:
#                 return Response({"warning": "Token not found in database, but blacklisted."}, status=status.HTTP_200_OK)
#
#             return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
#
#         except TokenError as e:
#             return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


# class WorkerProfileView(APIView):
#     permission_classes = [IsAuthenticated]
#     # print(IsAuthenticated)
#     print("in this")
#
#     def get(self, request):
#         # print(request.user)
#         return Response({
#                 'username': request.user.UserName,
#                 'role': request.auth.role,
#                 'job_title': request.user.WorkerJobTitle.JobTitleName if request.user.WorkerJobTitle else "N/A",
#                 'email': request.user.WorkerEmail,
#                 'phone': request.user.WorkerPhone
#             })

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminRole])
def getallWorkers(request):
    workers = Worker.objects.select_related('WorkerJobTitle').all()
    serializer = WorkerSerializer(workers, many=True)
    return Response(serializer.data)





class LogoutView(APIView):
    authentication_classes = []
    permission_classes=[]
    def delete(self, request):
        if not request.user or not request.user.is_authenticated:
            # محاولة المصادقة باستخدام WorkerTokenAuthentication
            auth = WorkerTokenAuthentication()
            try:
                user, token = auth.authenticate(request)  # المصادقة
                request.user = user  # تعيين المستخدم يدويًا
            except AuthenticationFailed:
                try:
                    auth_header = request.headers.get('Authorization')

                    if not auth_header or not auth_header.startswith('Bearer '):
                        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

                    token = auth_header.split(' ')[1]

                    # حذف التوكن من جدول التوكنات
                    deleted_count = AdminToken.objects.filter(token=str(token)).delete()[0]
                    if deleted_count == 0:
                        return Response({"warning": "Token not found in database, but blacklisted."},
                                        status=status.HTTP_200_OK)

                    return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)

                except TokenError as e:
                    return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        # متابعة تنفيذ تسجيل الخروج
            try:
                auth_header = request.headers.get('Authorization')
                if not auth_header or not auth_header.startswith('Bearer '):
                    return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
                token = auth_header.split(' ')[1]
                # حذف التوكن من قاعدة البيانات
                deleted_count = WorkerToken.objects.filter(token=str(token)).delete()[0]
                if deleted_count == 0:
                    return Response({"warning": "Token not found in database, but blacklisted."}, status=status.HTTP_200_OK)

                return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)

            except TokenError:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
