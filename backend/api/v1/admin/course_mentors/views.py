from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from courses.models import Course
from mentors.models import MentorCourseAssignment
from api.v1.auth.permissions import IsAdminRole

from api.v1.mentors.courses.serializers import (
    MentorCourseAssignmentSerializer,
    AssignMentorToCourseSerializer,
)

User = get_user_model()


class AdminCourseMentorListCreateView(APIView):
    permission_classes = [IsAdminRole]

    def get_course(self, course_id):
        try:
            return Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return None

    @extend_schema(
        summary="List assigned mentors of a course",
        parameters=[
            OpenApiParameter(
                name="course_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Course ID",
            ),
        ],
        responses={
            200: MentorCourseAssignmentSerializer(many=True),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Course not found"),
        },
        tags=["Admin - Course Mentors"],
    )
    def get(self, request, course_id):
        course = self.get_course(course_id)
        if not course:
            return Response(
                {"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND
            )
        assignments = MentorCourseAssignment.objects.filter(
            course=course, is_deleted=False
        )
        return Response(
            MentorCourseAssignmentSerializer(assignments, many=True).data,
            status=status.HTTP_200_OK,
        )
    
    @extend_schema(
        summary="Assign mentor to a course",
        parameters=[
            OpenApiParameter(
                name="course_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Course ID",
            ),
        ],
        request=AssignMentorToCourseSerializer,
        responses={
            201: MentorCourseAssignmentSerializer,
            400: OpenApiResponse(description="Invalid assignment data"),
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Course or mentor not found"),
            409: OpenApiResponse(description="Mentor already assigned"),
        },
        tags=["Admin - Course Mentors"],
    )
    def post(self, request, course_id):
        course = self.get_course(course_id)
        if not course:
            return Response(
                {"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = AssignMentorToCourseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        mentor_id = serializer.validated_data["mentor_id"]
        responsibility = serializer.validated_data.get("responsibility", "instructor")
        try:
            mentor = User.objects.get(id=mentor_id, role="mentor")
        except User.DoesNotExist:
            return Response(
                {"detail": "Mentor not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if MentorCourseAssignment.objects.filter(
            mentor=mentor, course=course, is_deleted=False
        ).exists():
            return Response(
                {"detail": "Mentor is already assigned to this course."},
                status=status.HTTP_409_CONFLICT,
            )
        assignment = MentorCourseAssignment.objects.create(
            mentor=mentor,
            course=course,
            responsibility=responsibility,
            is_active=True,
            assigned_by=request.user,
        )
        return Response(
            MentorCourseAssignmentSerializer(assignment).data,
            status=status.HTTP_201_CREATED,
        )


class AdminCourseMentorDetailView(APIView):
    permission_classes = [IsAdminRole]

    def get_assignment(self, course_id, mentor_id):
        try:
            course = Course.objects.get(id=course_id)
            mentor = User.objects.get(id=mentor_id, role="mentor")
            return MentorCourseAssignment.objects.get(
                mentor=mentor, course=course, is_deleted=False
            )
        except (Course.DoesNotExist, User.DoesNotExist, MentorCourseAssignment.DoesNotExist):
            return None

    @extend_schema(
        summary="Remove mentor from a course",
        parameters=[
            OpenApiParameter(
                name="course_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Course ID",
            ),
            OpenApiParameter(
                name="mentor_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Mentor ID",
            ),
        ],
        responses={
            204: None,
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Assignment not found"),
        },
        tags=["Admin - Course Mentors"],
    )
    def delete(self, request, course_id, mentor_id):
        assignment = self.get_assignment(course_id, mentor_id)
        if not assignment:
            return Response(
                {"detail": "Assignment not found."}, status=status.HTTP_404_NOT_FOUND
            )
        assignment.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Change mentor responsibility",
        parameters=[
            OpenApiParameter(
                name="course_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Course ID",
            ),
            OpenApiParameter(
                name="mentor_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Mentor ID",
            ),
        ],
        request=AssignMentorToCourseSerializer,
        responses={
            200: MentorCourseAssignmentSerializer,
            403: OpenApiResponse(description="Administrator access required"),
            404: OpenApiResponse(description="Assignment not found"),
        },
        tags=["Admin - Course Mentors"],
    )
    def patch(self, request, course_id, mentor_id):
        assignment = self.get_assignment(course_id, mentor_id)
        if not assignment:
            return Response(
                {"detail": "Assignment not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = AssignMentorToCourseSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if "responsibility" in serializer.validated_data:
            assignment.responsibility = serializer.validated_data["responsibility"]
        if "is_active" in serializer.validated_data:
            assignment.is_active = serializer.validated_data["is_active"]
        assignment.save()
        return Response(
            MentorCourseAssignmentSerializer(assignment).data, status=status.HTTP_200_OK
        )