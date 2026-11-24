from django.db.models import Sum
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from quizzes.models import (
    QuizAttempt,
    StudentAnswer,
    QuizResult,
)
from .serializers import QuizAttemptSerializer
from .permissions import IsAdminRole


class QuizAttemptListCreateView(generics.ListCreateAPIView):
    serializer_class = QuizAttemptSerializer

    def get_queryset(self):
        queryset = QuizAttempt.objects.select_related(
            "student", "quiz"
        ).all().order_by("-started_at")

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
        "student", "quiz"
    ).all()
    serializer_class = QuizAttemptSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]

class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            attempt = QuizAttempt.objects.get(pk=pk)
        except QuizAttempt.DoesNotExist:
            return Response(
                {"detail": "Quiz attempt not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        answers = StudentAnswer.objects.filter(
            quiz_attempt=attempt
        ).select_related("question")

        total_questions = answers.count()

        correct_answers = answers.filter(
            is_correct=True
        ).count()

        wrong_answers = total_questions - correct_answers

        obtained_marks = (
            answers.aggregate(
                total=Sum("marks_obtained")
            )["total"] or 0
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

        return Response(
            {
                "message": "Quiz submitted successfully",
                "quiz_attempt": str(attempt.id),
                "result_id": str(result.id),
                "score": obtained_marks,
                "percentage": percentage,
                "status": status_result,
            },
            status=status.HTTP_200_OK,
        )