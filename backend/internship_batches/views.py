from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import InternshipBatch
from .serializers import InternshipBatchSerializer
from .permissions import IsAdminRole


class InternshipBatchListCreateView(generics.ListCreateAPIView):
    queryset = InternshipBatch.objects.all().order_by("-created_at")
    serializer_class = InternshipBatchSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)


class InternshipBatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InternshipBatch.objects.all()
    serializer_class = InternshipBatchSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]