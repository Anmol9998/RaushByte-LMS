from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from quizzes.models import QuizAttempt


class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        attempt = QuizAttempt.objects.get(pk=pk)

        return Response(
            {
                "message": "Quiz submitted successfully."
            },
            status=status.HTTP_200_OK,
        )