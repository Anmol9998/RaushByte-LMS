from django.urls import path

from .views import (
    QuizAttemptListCreateView,
    QuizAttemptDetailView,
    SubmitQuizView,
)
from .submit import SubmitQuizView

urlpatterns = [
    path("", QuizAttemptListCreateView.as_view(), name="quiz-attempt-list-create"),
    path("<str:pk>/", QuizAttemptDetailView.as_view(), name="quiz-attempt-detail"),
    path("<str:pk>/submit/", SubmitQuizView.as_view(), name="submit-quiz",
),
]