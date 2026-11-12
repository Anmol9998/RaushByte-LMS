from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import generics, status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.auth.serializers import AdminLoginSerializer, UserSerializer
from api.v1.auth.permissions import IsAdminRole

User = get_user_model()


class AdminLoginView(APIView):
    permission_classes = []

    @extend_schema(
        summary="Log in an administrator",
        description="Authenticates an administrator and returns JWT tokens and profile details.",
        request=AdminLoginSerializer,
        responses={
            200: inline_serializer(
                name="AdminLoginResponse",
                fields={
                    "refresh": serializers.CharField(),
                    "access": serializers.CharField(),
                    "user": inline_serializer(
                        name="AdminLoginUser",
                        fields={
                            "id": serializers.CharField(),
                            "username": serializers.CharField(),
                            "email": serializers.EmailField(),
                            "role": serializers.CharField(),
                            "first_name": serializers.CharField(),
                            "last_name": serializers.CharField(),
                            "is_staff": serializers.BooleanField(),
                            "is_superuser": serializers.BooleanField(),
                            "is_admin": serializers.BooleanField(),
                        },
                    ),
                },
            ),
            400: OpenApiResponse(description="Invalid login details"),
            401: OpenApiResponse(description="Invalid email or password"),
        },
        tags=["Administration"],
    )
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class AdminDashboardSummaryView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(
        summary="Get the admin dashboard summary",
        responses={
            200: inline_serializer(
                name="AdminDashboardSummary",
                fields={
                    "total_students": serializers.IntegerField(),
                    "total_mentors": serializers.IntegerField(),
                    "total_admins": serializers.IntegerField(),
                    "active_courses": serializers.IntegerField(),
                    "internship_batches": serializers.IntegerField(),
                },
            ),
            403: OpenApiResponse(description="Administrator access required"),
        },
        tags=["Administration"],
    )
    def get(self, request):
        return Response(
            {
                "total_students": User.objects.filter(role="student").count(),
                "total_mentors": User.objects.filter(role="mentor").count(),
                "total_admins": User.objects.filter(role="admin").count(),
                "active_courses": 0,
                "internship_batches": 0,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema_view(
    get=extend_schema(
        summary="List users",
        responses={
            200: UserSerializer(many=True),
            403: OpenApiResponse(description="Administrator access required"),
        },
        tags=["Users"],
    ),
    post=extend_schema(
        summary="Create a user",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiResponse(description="Invalid user details"),
            403: OpenApiResponse(description="Administrator access required"),
        },
        tags=["Users"],
    ),
)
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]


@extend_schema_view(
    get=extend_schema(
        summary="Get a user",
        responses={
            200: UserSerializer,
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="User not found"),
        },
        tags=["Users"],
    ),
    put=extend_schema(
        summary="Replace a user",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Invalid user details"),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="User not found"),
        },
        tags=["Users"],
    ),
    patch=extend_schema(
        summary="Update a user",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Invalid user details"),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="User not found"),
        },
        tags=["Users"],
    ),
    delete=extend_schema(
        summary="Delete a user",
        responses={
            204: None,
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="User not found"),
        },
        tags=["Users"],
    ),
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]