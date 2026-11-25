from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsStudentRole

from courses.models import Lesson
from enrollments.models import Enrollment
from progress.models import LessonCompletion
from progress.services import (
    get_or_create_progress,
    increment_progress,
)


class LessonCompletionView(APIView):
    permission_classes = [IsStudentRole]

    @transaction.atomic
    def post(self, request):
        enrollment_id = request.data.get("enrollment")
        lesson_id = request.data.get("lesson")

        if not enrollment_id or not lesson_id:
            return Response(
                {
                    "detail": "Enrollment and Lesson are required."
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
                {"detail": "Enrollment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            lesson = Lesson.objects.select_related(
                "module",
                "module__course",
            ).get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response(
                {"detail": "Lesson not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Verify lesson belongs to enrolled course
        lesson_course_id = str(lesson.module.course.id)
        enrollment_course_id = str(enrollment.course.id)

        

        if lesson_course_id != enrollment_course_id:
            return Response(
                {
                    "detail": "Lesson does not belong to this course.",
                    
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Prevent duplicate completion
        completion, created = LessonCompletion.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson,
        )

        if not created:
            return Response(
                {
                    "detail": "Lesson already completed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        progress = get_or_create_progress(enrollment)

        increment_progress(
            progress,
            "completed_lessons",
        )

        return Response(
            {
                "message": "Lesson completed successfully.",
                "progress": str(progress.progress_percentage),
            },
            status=status.HTTP_201_CREATED,
        )