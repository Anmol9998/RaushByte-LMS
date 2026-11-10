from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import UserSerializer
from .permissions import IsAdminRole

User = get_user_model()


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Registration successful",
                    "user_id": str(user.id),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class AdminDashboardSummaryView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        total_students = User.objects.filter(role="student").count()
        total_mentors = User.objects.filter(role="mentor").count()
        total_admins = User.objects.filter(role="admin").count()

        return Response(
            {
                "total_students": total_students,
                "total_mentors": total_mentors,
                "total_admins": total_admins,
                "active_courses": 0,
                "internship_batches": 0,
            },
            status=status.HTTP_200_OK,
        )

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]