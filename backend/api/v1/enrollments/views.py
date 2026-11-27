from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from enrollments.models import Enrollment

from .serializers import EnrollmentSerializer
from .permissions import IsAdminRole


class EnrollmentListCreateView(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        queryset = Enrollment.objects.select_related(
            "student",
            "course",
        ).all()

        student_id = self.request.query_params.get("student_id")
        course_id = self.request.query_params.get("course_id")
        status = self.request.query_params.get("status")

        if student_id:
            queryset = queryset.filter(student_id=student_id)

        if course_id:
            queryset = queryset.filter(course_id=course_id)

        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by("-enrolled_at")

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.select_related(
        "student",
        "course",
    ).all()

    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]