from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from internship_batches.models import InternshipBatch
from .permissions import IsAdminRole
from .serializers import InternshipBatchSerializer


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


class InternshipBatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InternshipBatch.objects.select_related("course", "mentor")
    serializer_class = InternshipBatchSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]