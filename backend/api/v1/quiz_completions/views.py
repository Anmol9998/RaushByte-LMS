from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAuthenticatedUser

from quizzes.models import Quiz
from enrollments.models import Enrollment
from progress.models import QuizCompletion
from progress.services import (
    get_or_create_progress,
    increment_progress,
)


class QuizCompletionView(APIView):
    permission_classes = [IsAuthenticatedUser]

    @transaction.atomic
    def post(self, request):
        enrollment_id = request.data.get("enrollment")
        quiz_id = request.data.get("quiz")

        if not enrollment_id or not quiz_id:
            return Response(
                {
                    "detail": "Enrollment and Quiz are required."
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
            quiz = Quiz.objects.select_related(
                "module",
                "module__course",
            ).get(pk=quiz_id)
        except Quiz.DoesNotExist:
            return Response(
                {
                    "detail": "Quiz not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        quiz_course_id = str(quiz.module.course.id)
        enrollment_course_id = str(enrollment.course.id)

        if quiz_course_id != enrollment_course_id:
            return Response(
                {
                    "detail": "Quiz does not belong to this course."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        completion, created = QuizCompletion.objects.get_or_create(
            enrollment=enrollment,
            quiz=quiz,
        )

        if not created:
            return Response(
                {
                    "detail": "Quiz already completed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        progress = get_or_create_progress(enrollment)

        increment_progress(
            progress,
            "completed_quizzes",
        )

        return Response(
            {
                "message": "Quiz completed successfully.",
                "progress": str(progress.progress_percentage),
            },
            status=status.HTTP_201_CREATED,
        )