from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from assignments.models import Assignment
from .serializers import AssignmentSerializer
from .permissions import IsAdminRole


class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        queryset = Assignment.objects.select_related("module", "mentor").all().order_by("-created_at")

        module_id = self.request.query_params.get("module_id")
        if module_id:
            queryset = queryset.filter(module_id=module_id)

        return queryset

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.select_related("module", "mentor").all()
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]