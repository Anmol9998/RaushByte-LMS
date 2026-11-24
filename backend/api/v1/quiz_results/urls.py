from django.urls import path

from .views import (
    QuizResultListCreateView,
    QuizResultDetailView,
)

urlpatterns = [
    path(
        "",
        QuizResultListCreateView.as_view(),
        name="quiz-result-list-create",
    ),
    path(
        "<str:pk>/",
        QuizResultDetailView.as_view(),
        name="quiz-result-detail",
    ),
]