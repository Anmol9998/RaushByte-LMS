from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from quizzes.models import Question
from .serializers import QuestionSerializer
from .permissions import IsAdminRole


class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.select_related("quiz").all().order_by("order")

        quiz_id = self.request.query_params.get("quiz_id")
        if quiz_id:
            queryset = queryset.filter(quiz_id=quiz_id)

        return queryset

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.select_related("quiz").all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]