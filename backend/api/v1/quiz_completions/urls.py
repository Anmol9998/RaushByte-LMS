from django.urls import path

from .views import QuizCompletionView

urlpatterns = [
    path(
        "",
        QuizCompletionView.as_view(),
        name="quiz-completion",
    ),
]