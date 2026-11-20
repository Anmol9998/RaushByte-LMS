from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view

from internship_batches.models import InternshipBatch
from .permissions import IsAdminRole
from .serializers import InternshipBatchSerializer


@extend_schema_view(
    get=extend_schema(
        summary="List internship batches",
        responses={
            200: InternshipBatchSerializer(many=True),
            401: OpenApiResponse(description="Authentication required"),
        },
        tags=["Internship Batches"],
    ),
    post=extend_schema(
        summary="Create an internship batch",
        request=InternshipBatchSerializer,
        responses={
            201: InternshipBatchSerializer,
            400: OpenApiResponse(description="Invalid internship batch data"),
            403: OpenApiResponse(description="Administrator access required"),
        },
        tags=["Internship Batches"],
    ),
)
class InternshipBatchListCreateView(generics.ListCreateAPIView):
    queryset = InternshipBatch.objects.select_related("course", "mentor").order_by(
        "-created_at"
    )
    serializer_class = InternshipBatchSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="Get an internship batch",
        responses={
            200: InternshipBatchSerializer,
            401: OpenApiResponse(description="Authentication required"),
            404: OpenApiResponse(description="Internship batch not found"),
        },
        tags=["Internship Batches"],
    ),
    put=extend_schema(
        summary="Replace an internship batch",
        request=InternshipBatchSerializer,
        responses={
            200: InternshipBatchSerializer,
            400: OpenApiResponse(description="Invalid internship batch data"),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Internship batch not found"),
        },
        tags=["Internship Batches"],
    ),
    patch=extend_schema(
        summary="Update an internship batch",
        request=InternshipBatchSerializer,
        responses={
            200: InternshipBatchSerializer,
            400: OpenApiResponse(description="Invalid internship batch data"),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Internship batch not found"),
        },
        tags=["Internship Batches"],
    ),
    delete=extend_schema(
        summary="Delete an internship batch",
        responses={
            204: None,
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Internship batch not found"),
        },
        tags=["Internship Batches"],
    ),
)
class InternshipBatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InternshipBatch.objects.select_related("course", "mentor")
    serializer_class = InternshipBatchSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]