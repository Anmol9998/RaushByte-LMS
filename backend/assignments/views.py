from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Assignment
from .serializers import AssignmentSerializer
from .permissions import IsAdminRole


class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all().order_by("-created_at")
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]