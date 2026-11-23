from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from quizzes.models import Option
from .serializers import OptionSerializer
from .permissions import IsAdminRole


class OptionListCreateView(generics.ListCreateAPIView):
    serializer_class = OptionSerializer

    def get_queryset(self):
        queryset = Option.objects.select_related("question").all().order_by("order")

        question_id = self.request.query_params.get("question_id")
        if question_id:
            queryset = queryset.filter(question_id=question_id)

        return queryset

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]


class OptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Option.objects.select_related("question").all()
    serializer_class = OptionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminRole()]