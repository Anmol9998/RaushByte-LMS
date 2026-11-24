from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from submissions.models import Submission
from .serializers import SubmissionSerializer
from .permissions import IsAdminRole


class SubmissionListCreateView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        queryset = Submission.objects.select_related(
            "assignment",
            "student",
            "reviewed_by",
        ).all().order_by("-submitted_at")

        assignment_id = self.request.query_params.get("assignment_id")
        if assignment_id:
            queryset = queryset.filter(assignment_id=assignment_id)

        student_id = self.request.query_params.get("student_id")
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        return queryset

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class SubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.select_related(
        "assignment",
        "student",
        "reviewed_by",
    ).all()

    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]