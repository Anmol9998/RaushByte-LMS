from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from progress.models import Progress

from .serializers import ProgressSerializer
from .permissions import IsAdminRole


class ProgressListCreateView(generics.ListCreateAPIView):
    serializer_class = ProgressSerializer

    def get_queryset(self):
        queryset = Progress.objects.select_related(
            "enrollment",
            "enrollment__student",
            "enrollment__course",
        )

        enrollment_id = self.request.query_params.get("enrollment_id")

        if enrollment_id:
            queryset = queryset.filter(
                enrollment_id=enrollment_id
            )

        return queryset.order_by("-last_accessed")

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class ProgressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Progress.objects.select_related(
        "enrollment",
        "enrollment__student",
        "enrollment__course",
    )

    serializer_class = ProgressSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]