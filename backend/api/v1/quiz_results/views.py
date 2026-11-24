from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from quizzes.models import QuizResult
from .serializers import QuizResultSerializer
from .permissions import IsAdminRole


class QuizResultListCreateView(generics.ListCreateAPIView):
    serializer_class = QuizResultSerializer

    def get_queryset(self):
        queryset = QuizResult.objects.select_related(
            "quiz_attempt",
            "quiz_attempt__student",
            "quiz_attempt__quiz",
        ).all().order_by("-completed_at")

        quiz_attempt_id = self.request.query_params.get("quiz_attempt_id")

        if quiz_attempt_id:
            queryset = queryset.filter(quiz_attempt_id=quiz_attempt_id)

        return queryset

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class QuizResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizResult.objects.select_related(
        "quiz_attempt",
        "quiz_attempt__student",
        "quiz_attempt__quiz",
    ).all()

    serializer_class = QuizResultSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]