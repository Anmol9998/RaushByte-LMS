from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAuthenticatedUser

from assignments.models import Assignment
from enrollments.models import Enrollment
from progress.models import AssignmentCompletion
from progress.services import (
    get_or_create_progress,
    increment_progress,
)


class AssignmentCompletionView(APIView):
    permission_classes = [IsAuthenticatedUser]

    @transaction.atomic
    def post(self, request):
        enrollment_id = request.data.get("enrollment")
        assignment_id = request.data.get("assignment")

        if not enrollment_id or not assignment_id:
            return Response(
                {
                    "detail": "Enrollment and Assignment are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            enrollment = Enrollment.objects.select_related(
                "student",
                "course",
            ).get(pk=enrollment_id)
        except Enrollment.DoesNotExist:
            return Response(
                {
                    "detail": "Enrollment not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            assignment = Assignment.objects.select_related(
                "module",
                "module__course",
            ).get(pk=assignment_id)
        except Assignment.DoesNotExist:
            return Response(
                {
                    "detail": "Assignment not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        assignment_course_id = str(assignment.module.course.id)
        enrollment_course_id = str(enrollment.course.id)

        if assignment_course_id != enrollment_course_id:
            return Response(
                {
                    "detail": "Assignment does not belong to this course."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        completion, created = AssignmentCompletion.objects.get_or_create(
            enrollment=enrollment,
            assignment=assignment,
        )

        if not created:
            return Response(
                {
                    "detail": "Assignment already completed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        progress = get_or_create_progress(enrollment)

        increment_progress(
            progress,
            "completed_assignments",
        )

        return Response(
            {
                "message": "Assignment completed successfully.",
                "progress": str(progress.progress_percentage),
            },
            status=status.HTTP_201_CREATED,
        )