from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from enrollments.models import Enrollment
from progress.services import (
    get_or_create_progress,
    increment_progress,
)
from quizzes.models import (
    QuizAttempt,
    StudentAnswer,
    QuizResult,
)

from .permissions import IsAdminRole
from .serializers import QuizAttemptSerializer


class QuizAttemptListCreateView(generics.ListCreateAPIView):
    serializer_class = QuizAttemptSerializer

    def get_queryset(self):
        queryset = (
            QuizAttempt.objects.select_related(
                "student",
                "quiz",
            )
            .all()
            .order_by("-started_at")
        )

        student_id = self.request.query_params.get("student_id")
        quiz_id = self.request.query_params.get("quiz_id")

        if student_id:
            queryset = queryset.filter(student_id=student_id)

        if quiz_id:
            queryset = queryset.filter(quiz_id=quiz_id)

        return queryset

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class QuizAttemptDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizAttempt.objects.select_related(
        "student",
        "quiz",
    ).all()

    serializer_class = QuizAttemptSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        attempt = get_object_or_404(
            QuizAttempt.objects.select_related(
                "student",
                "quiz",
                "quiz__module",
                "quiz__module__course",
            ),
            pk=pk,
        )

        if attempt.status == "submitted":
            return Response(
                {
                    "detail": "This quiz has already been submitted."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        answers = (
            StudentAnswer.objects.filter(
                quiz_attempt=attempt
            )
            .select_related(
                "question",
                "selected_option",
            )
        )

        total_questions = answers.count()

        if total_questions == 0:
            return Response(
                {
                    "detail": "No answers found for this quiz attempt."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        correct_answers = answers.filter(
            is_correct=True
        ).count()

        wrong_answers = total_questions - correct_answers

        obtained_marks = (
            answers.aggregate(
                total=Sum("marks_obtained")
            )["total"]
            or 0
        )

        total_marks = sum(
            answer.question.marks
            for answer in answers
        )

        percentage = (
            (obtained_marks / total_marks) * 100
            if total_marks > 0
            else 0
        )

        status_result = (
            "passed"
            if percentage >= 40
            else "failed"
        )

        attempt.status = "submitted"
        attempt.score = obtained_marks
        attempt.submitted_at = timezone.now()
        attempt.save()

        result, created = QuizResult.objects.update_or_create(
            quiz_attempt=attempt,
            defaults={
                "total_questions": total_questions,
                "correct_answers": correct_answers,
                "wrong_answers": wrong_answers,
                "total_marks": total_marks,
                "obtained_marks": obtained_marks,
                "percentage": percentage,
                "status": status_result,
            },
        )

        enrollment = get_object_or_404(
            Enrollment,
            student=attempt.student,
            course=attempt.quiz.module.course,
        )

        progress = get_or_create_progress(enrollment)

        if created:
            increment_progress(
                progress,
                "completed_quizzes",
            )

        return Response(
            {
                "message": "Quiz submitted successfully.",
                "quiz_attempt": str(attempt.id),
                "result_id": str(result.id),
                "student": (
                    attempt.student.get_full_name()
                    or attempt.student.username
                ),
                "course": attempt.quiz.module.course.title,
                "quiz": attempt.quiz.title,
                "total_questions": total_questions,
                "correct_answers": correct_answers,
                "wrong_answers": wrong_answers,
                "total_marks": total_marks,
                "obtained_marks": obtained_marks,
                "percentage": percentage,
                "status": status_result,
            },
            status=status.HTTP_200_OK,
        )