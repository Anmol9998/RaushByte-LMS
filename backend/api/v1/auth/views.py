from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer





class RegisterView(APIView):
    permission_classes = []

    @extend_schema(
        summary="Register a new user",
        description="Creates a new LMS user account.",
        request=RegisterSerializer,
        responses={
            201: inline_serializer(
                name="RegisterResponse",
                fields={
                    "message": serializers.CharField(),
                    "user_id": serializers.CharField(),
                },
            ),
            400: OpenApiResponse(description="Invalid registration details"),
        },
        tags=["Authentication"],
    )
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

    @extend_schema(
        summary="Log in a user",
        description="Authenticates a user and returns JWT tokens and profile details.",
        request=LoginSerializer,
        responses={
            200: inline_serializer(
                name="LoginResponse",
                fields={
                    "refresh": serializers.CharField(),
                    "access": serializers.CharField(),
                    "user": inline_serializer(
                        name="LoginUser",
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
        tags=["Authentication"],
    )
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