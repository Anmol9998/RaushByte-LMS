from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from quizzes.models import StudentAnswer
from .serializers import StudentAnswerSerializer
from .permissions import IsAdminRole


class StudentAnswerListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentAnswerSerializer

    def get_queryset(self):
        queryset = StudentAnswer.objects.select_related(
            "quiz_attempt",
            "question",
            "selected_option",
        ).all().order_by("answered_at")

        quiz_attempt_id = self.request.query_params.get("quiz_attempt_id")
        question_id = self.request.query_params.get("question_id")

        if quiz_attempt_id:
            queryset = queryset.filter(quiz_attempt_id=quiz_attempt_id)

        if question_id:
            queryset = queryset.filter(question_id=question_id)

        return queryset

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class StudentAnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentAnswer.objects.select_related(
        "quiz_attempt",
        "question",
        "selected_option",
    ).all()

    serializer_class = StudentAnswerSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]