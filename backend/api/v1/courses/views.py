from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view

from courses.models import Course
from .serializers import CourseSerializer
from .permissions import IsAdminRole


@extend_schema_view(
    get=extend_schema(
        summary="List courses",
        responses={
            200: CourseSerializer(many=True),
            401: OpenApiResponse(description="Authentication required"),
        },
        tags=["Courses"],
    ),
    post=extend_schema(
        summary="Create a course",
        request=CourseSerializer,
        responses={
            201: CourseSerializer,
            400: OpenApiResponse(description="Invalid course data"),
            403: OpenApiResponse(description="Administrator access required"),
        },
        tags=["Courses"],
    ),
)
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all().order_by("-created_at")
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="Get a course",
        responses={
            200: CourseSerializer,
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Courses"],
    ),
    put=extend_schema(
        summary="Replace a course",
        request=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: OpenApiResponse(description="Invalid course data"),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Courses"],
    ),
    patch=extend_schema(
        summary="Update a course",
        request=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: OpenApiResponse(description="Invalid course data"),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Courses"],
    ),
    delete=extend_schema(
        summary="Delete a course",
        responses={
            204: None,
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Courses"],
    ),
)
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]