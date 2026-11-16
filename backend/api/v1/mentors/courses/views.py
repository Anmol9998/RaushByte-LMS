from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from mentors.models import MentorCourseAssignment
from .serializers import (
    MentorCourseSerializer,
    MentorCourseAssignmentSerializer,
    AssignMentorToCourseSerializer,
)
from .permissions import IsMentor, IsAssignedCourseMentor


@extend_schema_view(
    get=extend_schema(
        summary="List assigned courses",
        responses={
            200: MentorCourseSerializer(many=True),
            401: OpenApiResponse(description="Authentication required"),
            403: OpenApiResponse(description="User is not a mentor"),
        },
        tags=["Mentor Courses"],
    ),
)
class MentorAssignedCoursesView(generics.ListAPIView):
    permission_classes = [IsMentor]
    serializer_class = MentorCourseSerializer

    def get_queryset(self):
        user = self.request.user
        assignments = MentorCourseAssignment.objects.filter(
            mentor=user, is_deleted=False, is_active=True
        ).select_related("course")
        return [a.course for a in assignments]


@extend_schema_view(
    get=extend_schema(
        summary="View assigned course details",
        responses={
            200: MentorCourseSerializer,
            403: OpenApiResponse(description="Course not assigned to mentor"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Mentor Courses"],
    ),
    patch=extend_schema(
        summary="Update permitted course information",
        responses={
            200: MentorCourseSerializer,
            403: OpenApiResponse(description="Course not assigned to mentor"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Mentor Courses"],
    ),
)
class MentorCourseDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsMentor, IsAssignedCourseMentor]
    serializer_class = MentorCourseSerializer
    queryset = Course.objects.all()
    lookup_url_kwarg = "course_id"

    def get_object(self):
        course_id = self.kwargs.get(self.lookup_url_kwarg)
        try:
            return Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            from rest_framework.exceptions import NotFound

class MentorCourseModulesView(generics.RetrieveAPIView):
    permission_classes = [IsMentor, IsAssignedCourseMentor]
    queryset = Course.objects.all()
    lookup_url_kwarg = "course_id"

    @extend_schema(
        summary="View course modules",
        responses={
            200: OpenApiResponse(description="Course modules"),
            403: OpenApiResponse(description="Course not assigned to mentor"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Mentor Courses"],
    )
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        modules = getattr(course, "modules", None)
        if modules is None:
            return Response({"detail": "Course has no modules."}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            [
                {
                    "id": str(m.id),
                    "title": m.title,
                    "order": m.order,
                    "created_at": m.created_at,
                }
                for m in modules.all()
            ],
            status=status.HTTP_200_OK,
        )


class MentorCourseLessonsView(generics.RetrieveAPIView):
    permission_classes = [IsMentor, IsAssignedCourseMentor]
    queryset = Course.objects.all()
    lookup_url_kwarg = "course_id"

    @extend_schema(
        summary="View course lessons",
        responses={
            200: OpenApiResponse(description="Course lessons"),
            403: OpenApiResponse(description="Course not assigned to mentor"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Mentor Courses"],
    )
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        lessons = []
        for module in getattr(course, "modules", []).all() if hasattr(course, "modules") else []:
            for lesson in module.lessons.all():
                lessons.append(
                    {
                        "id": str(lesson.id),
                        "module_id": str(module.id),
                        "title": lesson.title,
                        "order": lesson.order,
                    }
                )
        return Response(lessons, status=status.HTTP_200_OK)


class MentorCourseStudentsView(generics.ListAPIView):
    permission_classes = [IsMentor, IsAssignedCourseMentor]
    queryset = Course.objects.all()
    lookup_url_kwarg = "course_id"

    @extend_schema(
        summary="View enrolled students of assigned course",
        responses={
            200: OpenApiResponse(description="Enrolled students"),
            403: OpenApiResponse(description="Course not assigned to mentor"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Mentor Courses"],
    )
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        enrollments = course.enrollments.filter(is_deleted=False, is_active=True).select_related("student")
        students = []
        for enrollment in enrollments:
            s = enrollment.student
            students.append(
                {
                    "id": str(s.id),
                    "username": s.username,
                    "email": s.email,
                    "first_name": s.first_name,
                    "last_name": s.last_name,
                    "enrolled_at": enrollment.created_at,
                }
            )
        return Response(students, status=status.HTTP_200_OK)


class MentorCourseStatisticsView(generics.RetrieveAPIView):
    permission_classes = [IsMentor, IsAssignedCourseMentor]
    queryset = Course.objects.all()
    lookup_url_kwarg = "course_id"

    @extend_schema(
        summary="View course statistics",
        responses={
            200: OpenApiResponse(description="Course statistics"),
            403: OpenApiResponse(description="Course not assigned to mentor"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Mentor Courses"],
    )
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        total_enrollments = course.enrollments.filter(is_deleted=False, is_active=True).count()
        return Response(
            {
                "course_id": str(course.id),
                "title": course.title,
                "total_enrolled_students": total_enrollments,
                "is_active": course.is_active,
            },
            status=status.HTTP_200_OK,
        )


class MentorCourseCurriculumView(generics.RetrieveAPIView):
    permission_classes = [IsMentor, IsAssignedCourseMentor]
    queryset = Course.objects.all()
    lookup_url_kwarg = "course_id"

    @extend_schema(
        summary="View complete course curriculum",
        responses={
            200: OpenApiResponse(description="Course curriculum"),
            403: OpenApiResponse(description="Course not assigned to mentor"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Mentor Courses"],
    )
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        curriculum = []
        for module in getattr(course, "modules", []).all() if hasattr(course, "modules") else []:
            curriculum.append(
                {
                    "module_id": str(module.id),
                    "module_title": module.title,
                    "lessons": [
                        {
                            "id": str(lesson.id),
                            "title": lesson.title,
                            "order": lesson.order,
                        }
                        for lesson in module.lessons.all()
                    ],
                }
            )
        return Response(
            {"course_id": str(course.id), "title": course.title, "curriculum": curriculum},
            status=status.HTTP_200_OK,
        )