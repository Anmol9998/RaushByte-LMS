
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from courses.models import Enrollment
from .serializers import EnrollmentSerializer
from api.v1.auth.permissions import IsStudentRole


class EnrollmentListCreateView(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudentRole]

    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user
        ).select_related("course")

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]

        if not course.is_active:
            raise ValidationError(
                {"course": "This course is not available for enrollment."}
            )

        if Enrollment.objects.filter(
            student=self.request.user,
            course=course,
        ).exists():
            raise ValidationError(
                {"course": "You are already enrolled in this course."}
            )

        serializer.save(student=self.request.user)
