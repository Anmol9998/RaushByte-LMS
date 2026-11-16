from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()


class MentorStudentsListView(generics.ListAPIView):
    permission_classes = []  # set dynamically below
    serializer_class = None

    def get_permissions(self):
        from api.v1.mentors.students.permissions import IsMentor

        return [IsMentor()]

    @extend_schema(
        summary="List all students assigned to mentor",
        responses={
            200: OpenApiResponse(description="Students assigned to mentor"),
            403: OpenApiResponse(description="User is not a mentor"),
        },
        tags=["Mentor Students"],
    )
    def get(self, request):
        from mentors.models import MentorCourseAssignment

        user = request.user
        assigned_course_ids = MentorCourseAssignment.objects.filter(
            mentor=user, is_deleted=False, is_active=True
        ).values_list("course_id", flat=True)

        student_ids = (
            __import__("courses.models", fromlist=["Enrollment"]).Enrollment.objects.filter(
                course_id__in=assigned_course_ids, is_deleted=False, is_active=True
            )
            .values_list("student_id", flat=True)
            .distinct()
        )
        students = User.objects.filter(id__in=student_ids, role="student")
        data = [
            {
                "id": str(s.id),
                "username": s.username,
                "email": s.email,
                "first_name": s.first_name,
                "last_name": s.last_name,
            }
            for s in students
        ]
        return Response(data, status=status.HTTP_200_OK)


class MentorStudentDetailView(generics.RetrieveAPIView):
    permission_classes = []  # set dynamically below
    serializer_class = None
    lookup_url_kwarg = "student_id"

    def get_permissions(self):
        from api.v1.mentors.students.permissions import IsMentor, IsStudentOfAssignedCourse

        return [IsMentor(), IsStudentOfAssignedCourse()]

    def get_object(self):
        student_id = self.kwargs.get(self.lookup_url_kwarg)
        try:
            return User.objects.get(id=student_id, role="student")
        except User.DoesNotExist:
            from rest_framework.exceptions import NotFound

            raise NotFound("Student not found.")

    @extend_schema(
        summary="View student details",
        parameters=[
            OpenApiParameter(
                name="student_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Student ID",
            ),
        ],
        responses={
            200: OpenApiResponse(description="Student details"),
            403: OpenApiResponse(description="Student not in mentor's courses"),
            404: OpenApiResponse(description="Student not found"),
        },
        tags=["Mentor Students"],
    )
    def get(self, request, *args, **kwargs):
        student = self.get_object()
        return Response(
            {
                "id": str(student.id),
                "username": student.username,
                "email": student.email,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "role": student.role,
                "is_active": student.is_active,
            },
            status=status.HTTP_200_OK,
        )